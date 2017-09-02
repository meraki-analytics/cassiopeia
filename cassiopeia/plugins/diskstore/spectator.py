from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, DataSink, PipelineContext, Query

from cassiopeia.data import Platform, Region
from cassiopeia.dto.spectator import FeaturedGamesDto, CurrentGameInfoDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class SpectatorDiskService(SimpleKVDiskService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    ##################
    # Featured Games #
    ##################

    _validate_get_featured_games_query = Query. \
        has("platform").as_(Platform)

    @get.register(FeaturedGamesDto)
    def get_featured_games(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> FeaturedGamesDto:
        SpectatorDiskService._validate_get_featured_games_query(query, context)
        key = "{clsname}.{platform}".format(clsname=FeaturedGamesDto.__name__, platform=query["platform"].value)
        return FeaturedGamesDto(self._get(key))

    @put.register(FeaturedGamesDto)
    def put_featured_games(self, item: FeaturedGamesDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname=FeaturedGamesDto.__name__, platform=platform)
        self._put(key, item)

    ################
    # Current Game #
    ################

    _validate_get_current_game_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    @get.register(CurrentGameInfoDto)
    def get_current_game(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoDto:
        SpectatorDiskService._validate_get_current_game_query(query, context)
        key = "{clsname}.{platform}.{id}".format(clsname=CurrentGameInfoDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["summoner.id"])
        return CurrentGameInfoDto(self._get(key))

    @put.register(CurrentGameInfoDto)
    def put_current_game(self, item: CurrentGameInfoDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=CurrentGameInfoDto.__name__,
                                                 platform=platform,
                                                 id=item["summonerId"])
        self._put(key, item)
