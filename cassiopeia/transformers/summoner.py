from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.summoner import SummonerData, Summoner
from ..dto.summoner import SummonerDto

T = TypeVar("T")
F = TypeVar("F")


class SummonerTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(SummonerDto, SummonerData)
    def summoner_dto_to_data(self, value: SummonerDto, context: PipelineContext = None) -> SummonerData:
        data = deepcopy(value)
        data = SummonerData.from_dto(data)
        return data

    # Data to Core

    @transform.register(SummonerData, Summoner)
    def summoner_data_to_core(self, value: SummonerData, context: PipelineContext = None) -> Summoner:
        return Summoner.from_data(value)

    # Core to Dto

    @transform.register(Summoner, SummonerDto)
    def champion_mastery_core_to_dto(self, value: Summoner, context: PipelineContext = None) -> SummonerDto:
        return value._data[SummonerData]._dto
