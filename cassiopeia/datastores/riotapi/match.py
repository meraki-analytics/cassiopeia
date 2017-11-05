from time import time
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator, Union
import datetime
import copy

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Season, Queue, SEASON_IDS, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, MatchListDtoGenerator, TimelineDto
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
            for id in query["ids"]:
                url = "https://{platform}.api.riotgames.com/lol/match/v3/matches/{id}".format(platform=query["platform"].value.lower(), id=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "matches/id"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error
                
                for participant in data["participants"]:
                    participant.setdefault("runes", [])
                    participant.setdefault("masteries", [])
                for p in data["participantIdentities"]:
                    aid = p.get("player", {}).get("currentAccountId", None)
                    if aid == 0:
                        p["player"]["bot"] = True

                data["gameId"] = id
                data["region"] = query["platform"].region.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get.register(MatchListDto)
    @validate_query(_validate_get_match_list_query, convert_region_to_platform)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        params = {}

        if "beginIndex" in query:
            params["beginIndex"] = query["beginIndex"]

        if "endIndex" in query:
            params["endIndex"] = query["endIndex"]

        if "beginTime" in query:
            params["beginTime"] = query["beginTime"]

        if "endTime" in query:
            params["endTime"] = query["endTime"]

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
        if "beginIndex" in query:
            data["beginIndex"] = query["beginIndex"]
        if "endIndex" in query:
            data["endIndex"] = query["endIndex"]
        data["season"] = seasons
        data["champion"] = champions
        data["queue"] = queues
        for match in data["matches"]:
            match["accountId"] = query["account.id"]
            match["region"] = data["region"]
        return MatchListDto(data)

    _validate_get_match_list_generator_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").as_(int).also. \
        can_have("endIndex").as_(int).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable)

    @get.register(MatchListDtoGenerator)
    @validate_query(_validate_get_match_list_generator_query, convert_region_to_platform)
    def get_match_list_generator(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDtoGenerator:
        original_query = copy.deepcopy(query)
        begin_time = original_query.get("beginTime", None)
        end_time = original_query.get("endTime", None)
        begin_index = original_query.get("beginIndex", None)
        end_index = original_query.get("endIndex", None)

        if begin_time is not None:
            begin_time = datetime.datetime.fromtimestamp(begin_time / 1000)
        if end_time is not None:
            end_time = datetime.datetime.fromtimestamp(end_time / 1000)

        # Create the generator that will populate the match history object.
        now = datetime.datetime.now() - datetime.timedelta(seconds=30)
        def generate_matchlists(begin_index: Union[int, None] = None, end_index: Union[int, None] = None, begin_time: Union[datetime.datetime, None] = None, end_time: Union[datetime.datetime, None] = None):
            # Shouldn't this be done in the Riot API data source? No, because it doesn't supply convenience data like this.

            assert (begin_time is None and end_time is None) or (begin_time is not None and end_time is not None)
            assert (begin_index is None and end_index is None) or (begin_index is not None and end_index is not None)
            if begin_time is None and begin_index is None:
                begin_index = 0

            number_of_requested_matches = float("inf") if end_index is None else end_index - begin_index
            number_of_initial_matches_to_skip = 0

            index_interval_size = 100
            datetime_interval_size = datetime.timedelta(days=7)

            # There is one weird special case that occurs when all of these are true:
            # 1) beginTime is after the summoner's most recent match
            # 2) beginIndex > 0
            # 3) the endTime - beginTime range is more than one week
            if begin_time is not None and end_time is not None and begin_index is not None and \
                begin_time < now and \
                begin_index > 0 and \
                end_time - begin_time > datetime_interval_size:
                number_of_initial_matches_to_skip = begin_index
                begin_index = 0

            # Now we need to potentially break up the time interval into one-week periods, and the indexes into intervals of 100.
            # We stop looking for matches when we have the number of requested matches, or when the date interval is complete.
            pulled_matches = 0 - number_of_initial_matches_to_skip
            _begin_time = begin_time
            _end_time = end_time
            _begin_index = begin_index
            _end_index = end_index
            while pulled_matches < number_of_requested_matches and \
                (begin_time is None or end_time - _begin_time > datetime.timedelta(days=0)):
                if begin_time is not None and end_time is not None and _end_time - _begin_time > datetime_interval_size:
                    _end_time = _begin_time + datetime_interval_size
                if begin_index is not None and end_index is not None and _end_index - _begin_index > index_interval_size:
                    _end_index = _begin_index + index_interval_size
                if begin_time is not None and end_time is not None:
                    query["beginTime"] = int(_begin_time.timestamp() * 1000)
                    query["endTime"] = int(_end_time.timestamp() * 1000)
                elif begin_index is not None:
                    query["beginIndex"] = _begin_index
                    if end_index is not None:
                        query["endIndex"] = _end_index
                    else:
                        query["endIndex"] = _begin_index + index_interval_size
                try:
                    data = self.get_match_list(query=query)
                    #data = configuration.settings.pipeline.get(type=MatchListData, query=query)
                except NotFoundError:
                    data = []
                for matchdto in data["matches"]:
                    pulled_matches += 1
                    if pulled_matches > 0:
                        yield  matchdto
                    if pulled_matches == number_of_requested_matches:
                        break

                if _begin_index is not None and len(data) < index_interval_size:
                    # Stop because the API returned less data than we asked for, and so there isn't any more left
                    break
                _begin_time = _end_time
                _end_time = end_time
                if _begin_index is not None:
                    _begin_index = _begin_index + len(data)
                _end_index = end_index
                if number_of_requested_matches == float("inf") and begin_time is None and len(data) == 0:
                    # Stop because we ran out of data
                    break

        generator = generate_matchlists(begin_index, end_index, begin_time, end_time)
        result = {"generator": generator}

        # Create/add the metadata/kwargs
        if "seasons" in query:
            seasons = {Season(season) for season in query["seasons"]}
        else:
            seasons = set()

        if "champion.ids" in query:
            champions = {query["champion.ids"]}
        else:
            champions = set()

        if "queues" in query:
            queues = {Queue(queue) for queue in query["queues"]}
        else:
            queues = set()

        result["accountId"] = query["account.id"]
        result["region"] = query["platform"].region.value
        if "beginIndex" in query:
            result["beginIndex"] = query["beginIndex"]
        if "endIndex" in query:
            result["endIndex"] = query["endIndex"]
        result["season"] = seasons
        result["champion"] = champions
        result["queue"] = queues

        generator = MatchListDtoGenerator(result)
        generator._summoner = query.get("summoner", None)  # Tack the summoner on to the generator... See notes in transformers/match.py
        return generator


    _validate_get_many_match_list_query = Query. \
        has("account.ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("recent").with_default(False).also. \
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
            params = {}

            if "beginIndex" in query:
                params["beginIndex"] = query["beginIndex"]

            if "endIndex" in query:
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
                    if "beginIndex" in query:
                        data["beginIndex"] = query["beginIndex"]
                    if "endIndex" in query:
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
