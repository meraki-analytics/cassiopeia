from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.spectator import CurrentGameInfoData

from ..dto.spectator import CurrentGameInfoDto, FeaturedGamesDto

T = TypeVar("T")
F = TypeVar("F")


class SpectatorTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(CurrentGameInfoDto, CurrentGameInfoData)
    def profile_icon_dto_to_data(self, value: CurrentGameInfoDto, context: PipelineContext = None) -> CurrentGameInfoData:
        data = deepcopy(value)
        return CurrentGameInfoData(data)

    @transform.register(FeaturedGamesDto, CurrentGameInfoData)
    def profile_icon_dto_to_data(self, value: FeaturedGamesDto, context: PipelineContext = None) -> CurrentGameInfoData:
        data = deepcopy(value)
        return CurrentGameInfoData(data)
