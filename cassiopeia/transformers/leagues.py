from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.league import Leagues, LeaguesListData, LeagueListData, League

from ..dto.league import LeaguesListDto, LeagueListDto

T = TypeVar("T")
F = TypeVar("F")


class LeagueTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(LeagueListDto, LeagueListData)
    def league_dto_to_data(self, value: LeagueListDto, context: PipelineContext = None) -> LeagueListData:
        data = deepcopy(value)
        return LeagueListData.from_dto(data)

    @transform.register(LeaguesListDto, LeaguesListData)
    def leagues_dto_to_data(self, value: LeaguesListDto, context: PipelineContext = None) -> LeaguesListData:
        data = deepcopy(value)
        for league in data["leagues"]:
            league["region"] = data["region"]
            league["summonerId"] = data["summonerId"]
        data = [self.league_dto_to_data(league) for league in data["leagues"]]
        return LeaguesListData(data, summoner_id=value["summonerId"])

    # Data to Core

    @transform.register(LeagueListData, League)
    def league_data_to_core(self, value: LeagueListData, context: PipelineContext = None) -> League:
        data = deepcopy(value)
        return League.from_data(data)

    @transform.register(LeaguesListData, Leagues)
    def leagues_data_to_core(self, value: LeaguesListData, context: PipelineContext = None) -> Leagues:
        return Leagues([self.league_data_to_core(page) for page in value], summoner=value.summoner_id)

    # Core to Dto

    @transform.register(League, LeagueListDto)
    def league_core_to_dto(self, value: League, context: PipelineContext = None) -> LeaguesListDto:
        return value._data[LeaguesListData]._dto

    @transform.register(Leagues, LeaguesListDto)
    def leagues_core_to_dto(self, value: Leagues, context: PipelineContext = None) -> LeaguesListDto:
        return LeaguesListDto({"leagues": set([self.league_core_to_dto(page) for page in value]), "summonerId": value._Leagues__summoner.id})
