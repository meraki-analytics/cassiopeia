from typing import Type, TypeVar, MutableMapping, Any
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.championmastery import ChampionMasteryData, ChampionMasteryListData
from ..dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionMasteryTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    @transform.register(ChampionMasteryDto, ChampionMasteryData)
    def champion_mastery_dto_to_data(self, value: ChampionMasteryDto, context: PipelineContext = None) -> ChampionMasteryData:
        data = deepcopy(value)
        return ChampionMasteryData(data)

    @transform.register(ChampionMasteryListDto, ChampionMasteryListData)
    def champion_mastery_list_dto_to_data(self, value: ChampionMasteryListDto, context: PipelineContext = None) -> ChampionMasteryListData:
        data = deepcopy(value)
        data["masteries"] = [self.champion_mastery_dto_to_data(c) for c in data["masteries"]]
        for c in data["masteries"]:
            c._update({"region": data["region"]})
        data = data["masteries"]
        return ChampionMasteryListData(data)
