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
        return SummonerData(**value)

    # Data to Core

    #@transform.register(SummonerData, Summoner)
    def summoner_data_to_core(self, value: SummonerData, context: PipelineContext = None) -> Summoner:
        return Summoner.from_data(value)
