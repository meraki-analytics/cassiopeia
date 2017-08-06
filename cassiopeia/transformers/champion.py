from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.champion import ChampionData, ChampionListData
from ..dto.champion import ChampionDto, ChampionListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(ChampionDto, ChampionData)
    def champion_dto_to_data(self, value: ChampionDto, context: PipelineContext = None) -> ChampionData:
        data = deepcopy(value)
        return ChampionData.from_dto(data)

    @transform.register(ChampionListDto, ChampionListData)
    def champion_list_dto_to_data(self, value: ChampionListDto, context: PipelineContext = None) -> ChampionListData:
        data = deepcopy(value)
        data["champions"] = [self.champion_dto_to_data(c) for c in data["champions"]]
        for c in data["champions"]:
            c._update({"region": data["region"]})
        data = data["champions"]
        return ChampionListData(data)
