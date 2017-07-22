from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.spectator import CurrentGameInfoData, FeaturedGamesData, CurrentMatch, FeaturedMatches
from ..dto.spectator import CurrentGameInfoDto, FeaturedGamesDto

T = TypeVar("T")
F = TypeVar("F")


class SpectatorTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Data

    @transform.register(CurrentGameInfoDto, CurrentGameInfoData)
    def current_game_dto_to_data(self, value: CurrentGameInfoDto, context: PipelineContext = None) -> CurrentGameInfoData:
        data = deepcopy(value)
        return CurrentGameInfoData(data)

    @transform.register(FeaturedGamesDto, FeaturedGamesData)
    def featured_games_dto_to_data(self, value: FeaturedGamesDto, context: PipelineContext = None) -> FeaturedGamesData:
        data = deepcopy(value)
        data = data["gameList"]
        return FeaturedGamesData(CurrentGameInfoData(game) for game in data)

    # Core

    @transform.register(CurrentGameInfoData, CurrentMatch)
    def current_game_data_to_core(self, value: CurrentGameInfoData, context: PipelineContext = None) -> CurrentMatch:
        return CurrentMatch(value)

    @transform.register(FeaturedGamesData, FeaturedMatches)
    def featured_games_data_to_core(self, value: FeaturedGamesData, context: PipelineContext = None) -> FeaturedMatches:
        return FeaturedMatches(CurrentMatch(game) for game in value)
