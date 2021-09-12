from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator
import arrow
import datetime
import math

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query

from .common import RiotAPIService, APINotFoundError
from ...data import Continent, Region, Platform, MatchType, Queue, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, TimelineDto
from ..uniquekeys import convert_to_continent

T = TypeVar("T")


class MatchAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_match_query = Query. \
        has("continent").as_(Continent).or_("region").as_(Region).or_("platform").as_(Platform).also. \
        has("id").as_(str)

    @get.register(MatchDto)
    @validate_query(_validate_get_match_query, convert_to_continent)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchDto:
        continent = query["continent"]
        id = query["id"]
        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{id}"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(continent, "matches/id")
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
            # metadata = data["metadata"]
            data = data["info"]  # Drop the metadata
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["continent"] = continent.value
        data["matchId"] = query["id"]
        for p in data["participants"]:
            puuid = p.get("puuid", None)
            if puuid is None:  # TODO: Figure out what bots are marked as in match-v5
                p["bot"] = True
            else:
                p["bot"] = False
        return MatchDto(data)

    _validate_get_many_match_query = Query. \
        has("continent").as_(Continent).or_("region").as_(Region).or_("platform").as_(Platform).also. \
        has("ids").as_(Iterable)

    @get_many.register(MatchDto)
    @validate_query(_validate_get_many_match_query, convert_to_continent)
    def get_many_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchDto, None, None]:
        continent = query["continent"]

        def generator():
            for id in query["ids"]:
                url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{id}"
                try:
                    app_limiter, method_limiter = self._get_rate_limiter(continent, "matches/id")
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                    # metadata = data["metadata"]
                    data = data["info"]  # Drop the metadata
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                for p in data["participants"]:
                    puuid = p.get("puuid", None)
                    if puuid is None:  # TODO: Figure out what bots are marked as in match-v5
                        p["bot"] = True
                    else:
                        p["bot"] = False

                data["matchId"] = id
                data["continent"] = continent.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = Query. \
        has("continent").as_(Continent).or_("region").as_(Region).or_("platform").as_(Platform).also. \
        has("puuid").as_(str).also. \
        has("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        has("beginIndex").as_(int).also. \
        has("maxNumberOfMatches").as_(float).also. \
        can_have("queue").as_(Queue).also. \
        can_have("type").as_(MatchType)

    @get.register(MatchListDto)
    @validate_query(_validate_get_match_list_query, convert_to_continent)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        params = {}

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
            params["beginTime"] = begin_time.int_timestamp * 1000
            if "endTime" in query:
                params["endTime"] = min((begin_time + riot_date_interval).int_timestamp * 1000, query["endTime"])
            else:
                params["endTime"] = (begin_time + riot_date_interval).int_timestamp * 1000
        else:
            params["beginIndex"] = query["beginIndex"]
            params["endIndex"] = query["beginIndex"] + min(riot_index_interval, query["maxNumberOfMatches"])
            params["endIndex"] = int(params["endIndex"])

        queue = query.get("queue", None)
        if queue is not None:
            params["queue"] = QUEUE_IDS[queue]

        type = query.get("type", None)
        if type is not None:
            params["type"] = type

        continent: Continent = query["continent"]
        puuid: str = query["puuid"]

        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(continent, "matchlists/by-puuid/puuid")
            data = self._get(url, params, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError:
            data = []

        data = {
            "match_ids": data,
            "continent": continent.value,
            "puuid": puuid,
            "type": type,
            "queue": queue,
        }

        if calling_method == "by_index":
            data["beginIndex"] = params["beginIndex"]
            data["endIndex"] = params["endIndex"]
            data["maxNumberOfMatches"] = query["maxNumberOfMatches"]
        else:
            data["beginTime"] = params["beginTime"]
            data["endTime"] = params["endTime"]
        return MatchListDto(data)

    _validate_get_timeline_query = Query. \
        has("continent").as_(Continent).or_("region").as_(Region).or_("platform").as_(Platform).also. \
        has("id").as_(str)

    @get.register(TimelineDto)
    @validate_query(_validate_get_timeline_query, convert_to_continent)
    def get_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        continent = query["continent"]
        id = query["id"]
        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{id}/timeline"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(continent, "matches/id/timeline")
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
            # metadata = data["metadata"]
            data = data["info"]  # Drop the metadata
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["matchId"] = query["id"]
        data["continent"] = continent.value
        return TimelineDto(data)
