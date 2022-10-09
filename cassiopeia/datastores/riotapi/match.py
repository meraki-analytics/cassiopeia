from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator
import arrow
import datetime
import math

from datapipelines import (
    DataSource,
    PipelineContext,
    Query,
    NotFoundError,
    validate_query,
)

from .common import RiotAPIService, APINotFoundError
from ...data import Continent, Region, Platform, MatchType, Queue, QUEUE_IDS
from ...dto.match import MatchDto, MatchListDto, TimelineDto
from ..uniquekeys import convert_region_to_platform, convert_to_continent

T = TypeVar("T")


class MatchAPI(RiotAPIService):
    @DataSource.dispatch
    def get(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> T:
        pass

    @DataSource.dispatch
    def get_many(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> Iterable[T]:
        pass

    _validate_get_match_query = (
        Query.has("region")
        .as_(Region)
        .or_("platform")
        .as_(Platform)
        .also.has("id")
        .as_(int)
    )

    @get.register(MatchDto)
    @validate_query(_validate_get_match_query, convert_region_to_platform)
    def get_match(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> MatchDto:
        platform: Platform = query["platform"]
        continent = platform.continent
        id = query["id"]
        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{platform.value}_{id}"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(
                continent, "matches/id"
            )
            data = self._get(
                url, {}, app_limiter=app_limiter, method_limiter=method_limiter
            )
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

    _validate_get_many_match_query = (
        Query.has("region")
        .as_(Region)
        .or_("platform")
        .as_(Platform)
        .also.has("ids")
        .as_(Iterable)
    )

    @get_many.register(MatchDto)
    @validate_query(_validate_get_many_match_query, convert_region_to_platform)
    def get_many_match(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> Generator[MatchDto, None, None]:
        platform: Platform = query["platform"]
        continent = platform.continent

        def generator():
            for id in query["ids"]:
                url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{platform.value}_{id}"
                try:
                    app_limiter, method_limiter = self._get_rate_limiter(
                        continent, "matches/id"
                    )
                    data = self._get(
                        url, {}, app_limiter=app_limiter, method_limiter=method_limiter
                    )
                    # metadata = data["metadata"]
                    data = data["info"]  # Drop the metadata
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                for p in data["participants"]:
                    puuid = p.get("puuid", None)
                    if (
                        puuid is None
                    ):  # TODO: Figure out what bots are marked as in match-v5
                        p["bot"] = True
                    else:
                        p["bot"] = False

                data["matchId"] = id
                data["continent"] = continent.value
                yield MatchDto(data)

        return generator()

    _validate_get_match_list_query = (
        Query.has("continent")
        .as_(Continent)
        .or_("region")
        .as_(Region)
        .or_("platform")
        .as_(Platform)
        .also.has("puuid")
        .as_(str)
        .also.can_have("startTime")
        .as_(int)
        .also.can_have("endTime")
        .as_(int)
        .also.has("start")
        .as_(int)
        .also.has("count")
        .as_(float)
        .also.can_have("queue")
        .as_(Queue)
        .also.can_have("type")
        .as_(MatchType)
    )

    @get.register(MatchListDto)
    @validate_query(_validate_get_match_list_query, convert_to_continent)
    def get_match_list(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> MatchListDto:
        params = {}

        riot_index_interval = 100

        start = query["start"]
        params["start"] = start

        count = query["count"]
        params["count"] = int(min(riot_index_interval, count))

        start_time = query.get("startTime", None)
        if start_time is not None:
            if isinstance(start_time, arrow.Arrow):
                start_time = start_time.int_timestamp
            params["startTime"] = start_time

        end_time = query.get("endTime", None)
        if end_time is not None:
            if isinstance(end_time, arrow.Arrow):
                end_time = end_time.int_timestamp
            params["endTime"] = end_time

        queue = query.get("queue", None)
        if queue is not None:
            params["queue"] = QUEUE_IDS[queue]

        type = query.get("type", None)
        if type is not None:
            params["type"] = MatchType(type).value

        continent: Continent = query["continent"]
        puuid: str = query["puuid"]
        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(
                continent, "matchlists/by-puuid/puuid"
            )
            data = self._get(
                url, params, app_limiter=app_limiter, method_limiter=method_limiter
            )
        except APINotFoundError:
            data = []

        data = {
            "match_ids": data,
            "continent": continent.value,
            "puuid": puuid,
            "type": type,
            "queue": queue,
            "start": start,
            "pulled_match_count": params["count"],
        }

        if start_time is not None:
            data["startTime"] = start_time

        if end_time is not None:
            data["endTime"] = end_time

        return MatchListDto(data)

    _validate_get_timeline_query = (
        Query.has("region")
        .as_(Region)
        .or_("platform")
        .as_(Platform)
        .also.has("id")
        .as_(int)
    )

    @get.register(TimelineDto)
    @validate_query(_validate_get_timeline_query, convert_region_to_platform)
    def get_match_timeline(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> TimelineDto:
        platform: Platform = query["platform"]
        continent: Continent = platform.continent
        id = query["id"]

        url = f"https://{continent.value.lower()}.api.riotgames.com/lol/match/v5/matches/{platform.value}_{id}/timeline"
        try:
            app_limiter, method_limiter = self._get_rate_limiter(
                continent, "matches/id/timeline"
            )
            data = self._get(
                url, {}, app_limiter=app_limiter, method_limiter=method_limiter
            )
            # metadata = data["metadata"]
            data = data["info"]  # Drop the metadata
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["matchId"] = query["id"]
        data["platform"] = platform.value
        return TimelineDto(data)
