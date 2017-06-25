from typing import Type, TypeVar, MutableMapping, Any
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.summoner import SummonerData
from ..dto.summoner import SummonerDto

T = TypeVar("T")
F = TypeVar("F")


class SummonerTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(SummonerDto, SummonerData)
    def summoner_dto_to_data(self, value: SummonerDto, context: PipelineContext = None) -> SummonerData:
        data = deepcopy(value)
        return SummonerData(data)
