from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.tft_summoner import TFTSummonerData, TFTSummoner
from ..dto.tft_summoner import TFTSummonerDto

T = TypeVar("T")
F = TypeVar("F")


class TFTSummonerTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(TFTSummonerDto, TFTSummonerData)
    def tft_summoner_dto_to_data(self, value: TFTSummonerDto, context: PipelineContext = None) -> TFTSummonerData:
        return TFTSummonerData(**value)

    # Data to Core

    #@transform.register(SummonerData, Summoner)
    def summoner_data_to_core(self, value: TFTSummonerData, context: PipelineContext = None) -> TFTSummoner:
        return TFTSummoner.from_data(value)
