from typing import Type, TypeVar, Mapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.staticdata.version import VersionListDto
from ...dto.spectator import CurrentGameInfoDto, FeaturedGamesDto

T = TypeVar("T")


def _get_default_version(query: Mapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: Mapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class SpectatorAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    ################
    # Current Game #
    ################

    _validate_get_current_game_query = Query. \
        has("platform").as_(Platform).also. \
        has("summonerId").as_(int)

    @get.register(CurrentGameInfoDto)
    def get_current_game(self, query: Mapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        SpectatorAPI._validate_get_current_game_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/{id}".format(platform=query["platform"].value.lower(), id=query["summonerId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "spectator/active-games/by-summoner"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return CurrentGameInfoDto(data)

    #################
    # Featured Game #
    #################

    _validate_get_featured_game_query = Query. \
        has("platform").as_(Platform)

    @get.register(CurrentGameInfoDto)
    def get_featured_game(self, query: Mapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        SpectatorAPI._validate_get_featured_game_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/spectator/v3/featured-games".format(platform=query["platform"].value.lower(), id=query["summonerId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "featured-games"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return CurrentGameInfoDto(data)
