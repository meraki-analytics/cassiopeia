from time import time
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region, Season, Queue, SEASON_IDS, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, TimelineDto

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
        has("gameId").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(MatchDto)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI._validate_get_match_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/match/v3/matches/{id}".format(platform=query["platform"].value.lower(), id=query["gameId"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matches/id"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["gameId"] = query["gameId"]
        data["region"] = query["platform"].region.value
        return MatchDto(data)

    _validate_get_many_match_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(MatchDto)
    def get_many_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI._validate_get_many_match_query(query, context)

        def generator():
            for id in query["ids"]:
                url = "https://{platform}.api.riotgames.com/lol/match/v3/matches/{id}".format(platform=query["platform"].value.lower(), id=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matches/id"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["gameId"] = id
                data["region"] = query["platform"].region.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("recent").with_default(False).also. \
        can_have("startTime").with_default(0).also. \
        can_have("endTime").with_default(_get_current_time, supplies_type=int).also. \
        can_have("startIndex").as_(int).and_("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get.register(MatchListDto)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI._validate_get_match_list_query(query, context)

        if query["recent"]:
            url = "https://{platform}.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}/recent".format(platform=query["platform"].value.lower(), accountId=query["account.id"])
            try:
                data = self._get(url, {})
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["accountId"] = query["account.id"]
            data["region"] = query["platform"].region.value
            return MatchListDto(data)
        else:
            params = {
                "beginTime": query["startTime"],
                "endTime": query["endTime"]
            }

            if "startIndex" in query and "endIndex" in query:
                params["beginIndex"] = query["startIndex"]
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

            url = "https://{platform}.api.riotgames.com/lol/match/v3/matchlists/by-account/{accountId}".format(platform=query["platform"].value.lower(), accountId=query["account.id"])
            try:
                data = self._get(url, params, self._get_rate_limiter(query["platform"], "matchlists/by-account/accountId"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["accountId"] = query["account.id"]
            data["region"] = query["platform"].region.value
            data["startTime"] = query["startTime"]
            data["endTime"] = query["endTime"]
            if "seasons" in query:
                data["seasons"] = seasons
            if "champion.ids" in query:
                data["champion"] = params["champion"]
            if "queues" in query:
                params["queue"] = queues
            for match in data["matches"]:
                match["accountId"] = query["account.id"]
                match["region"] = data["region"]
            return MatchListDto(data)

    _validate_get_many_match_list_query = Query. \
        has("account.ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("recent").with_default(False).also. \
        can_have("startTime").with_default(0).also. \
        can_have("endTime").with_default(_get_current_time, supplies_type=int).also. \
        can_have("startIndex").as_(int).and_("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get_many.register(MatchListDto)
    def get_many_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MatchListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI._validate_get_many_match_list_query(query, context)

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
                "beginTime": query["startTime"],
                "endTime": query["endTime"]
            }

            if "startIndex" in query and "endIndex" in query:
                params["beginIndex"] = query["startIndex"]
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
                    data["startTime"] = query["startTime"]
                    data["endTime"] = query["endTime"]
                    if "seasons" in query:
                        data["seasons"] = seasons
                    if "champion.ids" in query:
                        data["champion"] = params["champion"]
                    if "queues" in query:
                        params["queue"] = queues
                    yield MatchListDto(data)

        return generator()

    _validate_get_timeline_query = Query. \
        has("matchId").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(TimelineDto)
    def get_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI._validate_get_timeline_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/match/v3/timelines/by-match/{id}".format(platform=query["platform"].value.lower(), id=query["matchId"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "timelines/by-match/id"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["matchId"] = query["matchId"]
        data["region"] = query["platform"].region.value
        return TimelineDto(data)

    validate_get_many_timeline_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(TimelineDto)
    def get_many_match_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[TimelineDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        MatchAPI.validate_get_many_timeline_query(query, context)

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
