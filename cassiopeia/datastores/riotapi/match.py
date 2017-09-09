from time import time
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region, Season, Queue, SEASON_IDS, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, TimelineDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


def _get_current_time(query: MutableMapping[str, Any], context: PipelineContext = None) -> int:
    return int(time()) * 1000


class MatchAPI(RiotAPIService):
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
        url = "https://{platform}.api.riotgames.com/lol/match/v3/matches/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matches/id"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["gameId"] = query["id"]
        data["region"] = query["platform"].region.value
        for participant in data["participants"]:
            participant.setdefault("runes", [])
            participant.setdefault("masteries", [])
        return MatchDto(data)

    _validate_get_many_match_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(MatchDto)
    @validate_query(_validate_get_many_match_query, convert_region_to_platform)
    def get_many_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchDto, None, None]:
        def generator():
            for id in query["ids"]:
                url = "https://{platform}.api.riotgames.com/lol/match/v3/matches/{id}".format(platform=query["platform"].value.lower(), id=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matches/id"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error
                
                for participant in data["participants"]:
                    participant.setdefault("runes", [])
                    participant.setdefault("masteries", [])
 
                data["gameId"] = id
                data["region"] = query["platform"].region.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").with_default(0).also. \
        can_have("endIndex").with_default(100).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get.register(MatchListDto)
    @validate_query(_validate_get_match_list_query, convert_region_to_platform)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        params = {
            "beginIndex": query["beginIndex"],
            "endIndex": query["endIndex"]
        }

        if "beginIndex" in query and "endIndex" in query:
            params["beginIndex"] = query["beginIndex"]
            params["endIndex"] = query["endIndex"]

        if "seasons" in query:
            seasons = {Season(season) for season in query["seasons"]}
            params["season"] = {SEASON_IDS[season] for season in seasons}
        else:
            seasons = set()

        if "champion.ids" in query:
            champions = {query["champion.ids"]}
            params["champion"] = champions
        else:
            champions = set()

        if "queues" in query:
            queues = {Queue(queue) for queue in query["queues"]}
            params["queue"] = {QUEUE_IDS[queue] for queue in queues}
        else:
            queues = set()

        url = "https://{platform}.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}".format(platform=query["platform"].value.lower(), accountId=query["account.id"])
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "matchlists/by-account/accountId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["accountId"] = query["account.id"]
        data["region"] = query["platform"].region.value
        data["beginIndex"] = query["beginIndex"]
        data["endIndex"] = query["endIndex"]
        data["season"] = seasons
        data["champion"] = champions
        data["queue"] = queues
        for match in data["matches"]:
            match["accountId"] = query["account.id"]
            match["region"] = data["region"]
        return MatchListDto(data)

    _validate_get_many_match_list_query = Query. \
        has("account.ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("recent").with_default(False).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").with_default(0).also. \
        can_have("endIndex").with_default(100).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get_many.register(MatchListDto)
    @validate_query(_validate_get_many_match_list_query, convert_region_to_platform)
    def get_many_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchListDto, None, None]:
        if query["recent"]:
            def generator():
                for id in query["account.ids"]:
                    url = "https://{platform}.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}/recent".format(platform=query["platform"].value.lower(), accountId=id)
                    try:
                        data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matchlists/by-account/accountId/recent"))
                    except APINotFoundError as error:
                        raise NotFoundError(str(error)) from error

                    data["account.id"] = id
                    data["region"] = query["platform"].region.value
                    yield MatchListDto(data)
        else:
            params = {
                "beginIndex": query["beginIndex"],
                "endIndex": query["endIndex"]
            }

            if "beginIndex" in query and "endIndex" in query:
                params["beginIndex"] = query["beginIndex"]
                params["endIndex"] = query["endIndex"]

            if "seasons" in query:
                seasons = {Season(season) for season in query["seasons"]}
                params["season"] = {SEASON_IDS[season] for season in seasons}
            else:
                seasons = set()

            if "champion.ids" in query:
                params["champion"] = {query["champion.ids"]}

            if "queues" in query:
                queues = {Queue(queue) for queue in query["queues"]}
                params["queue"] = {QUEUE_IDS[queue] for queue in queues}
            else:
                queues = set()

            def generator():
                for id in query["account.ids"]:
                    url = "https://{platform}.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}".format(platform=query["platform"].value.lower(), accountId=id)
                    try:
                        data = self._get(url, params, self._get_rate_limiter(query["platform"], "matchlists/by-account/accountId"))
                    except APINotFoundError as error:
                        raise NotFoundError(str(error)) from error

                    data["account.id"] = id
                    data["region"] = query["platform"].region.value
                    data["beginIndex"] = query["beginIndex"]
                    data["endIndex"] = query["endIndex"]
                    if "seasons" in query:
                        data["seasons"] = seasons
                    if "champion.ids" in query:
                        data["champion"] = params["champion"]
                    if "queues" in query:
                        params["queue"] = queues
                    yield MatchListDto(data)

        return generator()

    _validate_get_timeline_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(TimelineDto)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        url = "https://{platform}.api.riotgames.com/lol/match/v3/timelines/by-match/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "timelines/by-match/id"))
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
        def generator():
            for id in query["ids"]:
                url = "https://{platform}.api.riotgames.com/lol/match/v3/timelines/by-match/{id}".format(platform=query["platform"].value.lower(), id=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "timelines/by-match/id"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["matchId"] = id
                data["region"] = query["platform"].region.value
                yield TimelineDto(data)

        return generator()
