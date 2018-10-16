from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.champion import ChampionRotationData, ChampionRotation
from ..dto.champion import ChampionRotationDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(ChampionRotationDto, ChampionRotationData)
    def champion_rotation_dto_to_data(self, value: ChampionRotationDto, context: PipelineContext = None) -> ChampionRotationData:
        return ChampionRotationData(**value)

    # Data to Core

    @transform.register(ChampionRotationData, ChampionRotation)
    def champion_rotation_data_to_core(self, value: ChampionRotationData, context: PipelineContext = None) -> ChampionRotation:
        return ChampionRotation.from_data(value, loaded_groups={ChampionRotationData})
