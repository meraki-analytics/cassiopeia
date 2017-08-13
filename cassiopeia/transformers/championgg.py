from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.championgg import GGChampionData, GGChampionListData
from ..dto.championgg import GGChampionDto, GGChampionListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionGGTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(GGChampionDto, GGChampionData)
    def champion_gg_dto_to_data(self, value: GGChampionDto, context: PipelineContext = None) -> GGChampionData:
        data = deepcopy(value)
        return GGChampionData.from_dto(data)

    @transform.register(GGChampionListDto, GGChampionListData)
    def champion_gg_list_dto_to_data(self, value: GGChampionListDto, context: PipelineContext = None) -> GGChampionListData:
        data = deepcopy(value)
        data["data"] = [self.champion_gg_dto_to_data(c) for c in data["data"]]
        for c in data["data"]:
            c._update({"region": data["region"]})
        data = data["data"]
        return GGChampionListData(data)