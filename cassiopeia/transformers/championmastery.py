from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.championmastery import ChampionMasteryData, ChampionMasteryListData, ChampionMastery, ChampionMasteries
from ..dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto

T = TypeVar("T")
F = TypeVar("F")


class ChampionMasteryTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(ChampionMasteryDto, ChampionMasteryData)
    def champion_mastery_dto_to_data(self, value: ChampionMasteryDto, context: PipelineContext = None) -> ChampionMasteryData:
        data = deepcopy(value)
        return ChampionMasteryData.from_dto(data)

    @transform.register(ChampionMasteryListDto, ChampionMasteryListData)
    def champion_mastery_list_dto_to_data(self, value: ChampionMasteryListDto, context: PipelineContext = None) -> ChampionMasteryListData:
        data = deepcopy(value)
        data["masteries"] = [self.champion_mastery_dto_to_data(c) for c in data["masteries"]]
        for c in data["masteries"]:
            c._update({"region": data["region"]})
        data = data["masteries"]
        return ChampionMasteryListData(data, region=value["region"], summoner_id=value["summonerId"])

    # Data to Core

    @transform.register(ChampionMasteryData, ChampionMastery)
    def champion_mastery_data_to_core(self, value: ChampionMasteryData, context: PipelineContext = None) -> ChampionMastery:
        return ChampionMastery.from_data(value)

    @transform.register(ChampionMasteryListData, ChampionMasteries)
    def champion_mastery_list_data_to_core(self, value: ChampionMasteryListData, context: PipelineContext = None) -> ChampionMasteries:
        return ChampionMasteries([self.champion_mastery_data_to_core(cm) for cm in value], region=value.region, summoner=value.summoner_id)

    # Core to Dto

    @transform.register(ChampionMastery, ChampionMasteryDto)
    def champion_mastery_core_to_dto(self, value: ChampionMastery, context: PipelineContext = None) -> ChampionMasteryDto:
        return value._data[ChampionMasteryData]._dto

    @transform.register(ChampionMasteries, ChampionMasteryListDto)
    def champion_mastery_list_core_to_dto(self, value: ChampionMasteries, context: PipelineContext = None) -> ChampionMasteryListDto:
        return ChampionMasteryListDto({"masteries": [self.champion_mastery_core_to_dto(cm) for cm in value], "summonerId": value._ChampionMasteries__summoner.id, "region": value.region})
