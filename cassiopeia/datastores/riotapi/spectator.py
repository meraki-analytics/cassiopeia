from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.staticdata.version import VersionListDto
from ...dto.spectator import CurrentGameInfoDto, FeaturedGamesDto

T = TypeVar("T")


def _get_default_version(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class SpectatorAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    ################
    # Current Game #
    ################

    _validate_get_current_game_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    @get.register(CurrentGameInfoDto)
    def get_current_game(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        SpectatorAPI._validate_get_current_game_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/spectator/v3/active-games/by-summoner/{id}".format(platform=query["platform"].value.lower(), id=query["summoner.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "spectator/active-games/by-summoner"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return CurrentGameInfoDto(data)

    #################
    # Featured Game #
    #################

    _validate_get_featured_game_query = Query. \
        has("platform").as_(Platform)

    @get.register(FeaturedGamesDto)
    def get_featured_games(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> FeaturedGamesDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        SpectatorAPI._validate_get_featured_game_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/spectator/v3/featured-games".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "featured-games"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for game in data["gameList"]:
            game["region"] = data["region"]
        return FeaturedGamesDto(data)
