from typing import Type, TypeVar
from copy import deepcopy
from collections import defaultdict

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
        id = data[0]["championId"]
        reformatted = defaultdict(dict)
        for item in data:
            assert item["championId"] == id
            item.pop("championId")
            role = item.pop("role")
            elo = item.pop("elo")
            patch = item.pop("patch")
            for field in item.keys():
                reformatted[field][role] = item[field]
            reformatted["championId"] = id
            reformatted["elo"] = elo
            reformatted["patch"] = patch
        return GGChampionData.from_dto(reformatted)

    @transform.register(GGChampionListDto, GGChampionListData)
    def champion_gg_list_dto_to_data(self, value: GGChampionListDto, context: PipelineContext = None) -> GGChampionListData:
        data = deepcopy(value)
        reformatted =  {item["championId"]: [] for item in data["data"]}
        for item in data["data"]:
            reformatted[item["championId"]].append(item)
        data["data"] = [self.champion_gg_dto_to_data(item) for item in reformatted.values()]
        for c in data["data"]:
            c._update({"region": data["region"]})
        data = data["data"]
        return GGChampionListData(data)
