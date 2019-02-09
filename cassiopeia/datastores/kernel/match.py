from time import time
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator, Union
import arrow
import datetime
import math

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query

from .common import KernelSource, APINotFoundError
from ...data import Platform, Season, Queue, SEASON_IDS, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, TimelineDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


def _get_current_time(query: MutableMapping[str, Any], context: PipelineContext = None) -> int:
    return int(time()) * 1000


class MatchAPI(KernelSource):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_match_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(MatchDto)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "lol/match/v4/matches/{id}".format(id=query["id"])
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["gameId"] = query["id"]
        data["region"] = query["platform"].region.value
        for p in data["participantIdentities"]:
            aid = p.get("player", {}).get("currentAccountId", None)
            if aid == 0:
                p["player"]["bot"] = True
        return MatchDto(data)

    _validate_get_many_match_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(MatchDto)
    @validate_query(_validate_get_many_match_query, convert_region_to_platform)
    def get_many_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchDto, None, None]:
        def generator():
            parameters = {"platform": query["platform"].value}
            for id in query["ids"]:
                endpoint = "lol/match/v4/matches/{id}".format(id=id)
                try:
                    data = self._get(endpoint=endpoint, parameters=parameters)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error
                
                for participant in data["participants"]:
                    participant.setdefault("runes", [])
                for p in data["participantIdentities"]:
                    aid = p.get("player", {}).get("currentAccountId", None)
                    if aid == 0:
                        p["player"]["bot"] = True

                data["gameId"] = id
                data["region"] = query["platform"].region.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = Query. \
        has("accountId").as_(str).also. \
        has("platform").as_(Platform).also. \
        has("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        has("beginIndex").as_(int).also. \
        has("maxNumberOfMatches").as_(float).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get.register(MatchListDto)
    @validate_query(_validate_get_match_list_query, convert_region_to_platform)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        parameters = {"platform": query["platform"].value}

        riot_index_interval = 100
        riot_date_interval = datetime.timedelta(days=7)

        begin_time = query["beginTime"]  # type: arrow.Arrow
        end_time = query.get("endTime", arrow.now())  # type: arrow.Arrow
        if isinstance(begin_time, int):
            begin_time = arrow.get(begin_time / 1000)
        if isinstance(end_time, int):
            end_time = arrow.get(end_time / 1000)

        def determine_calling_method(begin_time, end_time) -> str:
            """Returns either "by_date" or "by_index"."""
            matches_per_date_interval = 10  # This is an assumption
            seconds_per_day = (60 * 60 * 24)
            riot_date_interval_in_days = riot_date_interval.total_seconds() / seconds_per_day  # in units of days
            npulls_by_date = (end_time - begin_time).total_seconds() / seconds_per_day / riot_date_interval_in_days
            npulls_by_index = (arrow.now() - begin_time).total_seconds() / seconds_per_day / riot_date_interval_in_days * matches_per_date_interval / riot_index_interval
            if math.ceil(npulls_by_date) < math.ceil(npulls_by_index):
                by = "by_date"
            else:
                by = "by_index"
            return by

        calling_method = determine_calling_method(begin_time, end_time)

        if calling_method == "by_date":
            parameters["beginTime"] = begin_time.timestamp * 1000
            if "endTime" in query:
                parameters["endTime"] = min((begin_time + riot_date_interval).timestamp * 1000, query["endTime"])
            else:
                parameters["endTime"] = (begin_time + riot_date_interval).timestamp * 1000
        else:
            parameters["beginIndex"] = query["beginIndex"]
            parameters["endIndex"] = query["beginIndex"] + min(riot_index_interval, query["maxNumberOfMatches"])
            parameters["endIndex"] = int(parameters["endIndex"])

        if "seasons" in query:
            seasons = {Season(season) for season in query["seasons"]}
            parameters["season"] = {SEASON_IDS[season] for season in seasons}
        else:
            seasons = set()

        if "champion.ids" in query:
            champions = query["champion.ids"]
            parameters["champion"] = champions
        else:
            champions = set()

        if "queues" in query:
            queues = {Queue(queue) for queue in query["queues"]}
            parameters["queue"] = {QUEUE_IDS[queue] for queue in queues}
        else:
            queues = set()

        endpoint = "lol/match/v4/matchlists/by-account/{accountId}".format(accountId=query["accountId"])
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError:
            data = {"matches": []}

        data["accountId"] = query["accountId"]
        data["region"] = query["platform"].region.value
        data["season"] = seasons
        data["champion"] = champions
        data["queue"] = queues
        if calling_method == "by_index":
            data["beginIndex"] = parameters["beginIndex"]
            data["endIndex"] = parameters["endIndex"]
            data["maxNumberOfMatches"] = query["maxNumberOfMatches"]
        else:
            data["beginTime"] = parameters["beginTime"]
            data["endTime"] = parameters["endTime"]
        for match in data["matches"]:
            match["accountId"] = query["accountId"]
            match["region"] = Platform(match["platformId"]).region.value
        return MatchListDto(data)

    _validate_get_many_match_list_query = Query. \
        has("accountIds").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get_many.register(MatchListDto)
    @validate_query(_validate_get_many_match_list_query, convert_region_to_platform)
    def get_many_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchListDto, None, None]:
        parameters = {"platform": query["platform"].value}

        if "beginIndex" in query:
            parameters["beginIndex"] = query["beginIndex"]

        if "endIndex" in query:
            parameters["endIndex"] = query["endIndex"]

        if "seasons" in query:
            seasons = {Season(season) for season in query["seasons"]}
            parameters["season"] = {SEASON_IDS[season] for season in seasons}
        else:
            seasons = set()

        if "champion.ids" in query:
            parameters["champion"] = {query["champion.ids"]}

        if "queues" in query:
            queues = {Queue(queue) for queue in query["queues"]}
            parameters["queue"] = {QUEUE_IDS[queue] for queue in queues}
        else:
            queues = set()

        def generator():
            for id in query["accountIds"]:
                endpoint = "lol/match/v4/matchlists/by-account/{accountId}".format(accountId=id)
                try:
                    data = self._get(endpoint=endpoint, parameters=parameters)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["accountId"] = id
                data["region"] = query["platform"].region.value
                if "beginIndex" in query:
                    data["beginIndex"] = query["beginIndex"]
                if "endIndex" in query:
                    data["endIndex"] = query["endIndex"]
                if "seasons" in query:
                    data["seasons"] = seasons
                if "champion.ids" in query:
                    data["champion"] = parameters["champion"]
                if "queues" in query:
                    parameters["queue"] = queues
                yield MatchListDto(data)

        return generator()

    _validate_get_timeline_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(TimelineDto)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "lol/match/v4/timelines/by-match/{id}".format(id=query["id"])
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["matchId"] = query["id"]
        data["region"] = query["platform"].region.value
        return TimelineDto(data)

    _validate_get_many_timeline_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(TimelineDto)
    @validate_query(_validate_get_many_timeline_query, convert_region_to_platform)
    def get_many_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[TimelineDto, None, None]:
        parameters = {"platform": query["platform"].value}
        def generator():
            for id in query["ids"]:
                endpoint = "lol/match/v4/timelines/by-match/{id}".format(id=id)
                try:
                    data = self._get(endpoint=endpoint, parameters=parameters)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["matchId"] = id
                data["region"] = query["platform"].region.value
                yield TimelineDto(data)

        return generator()
