from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.league import Leagues, LeaguesListData, LeagueListData, League, ChallengerLeagueListData, ChallengerLeague, MasterLeagueListData, MasterLeague

from ..dto.league import LeaguesListDto, LeagueListDto, ChallengerLeagueListDto, MasterLeagueListDto

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
            for entry in league["entries"]:
                entry["tier"] = league["tier"]
                entry["leagueName"] = league["name"]
                entry["queue"] = league["queue"]
                entry["region"] = league["region"]
        data = [self.league_dto_to_data(league) for league in data["leagues"]]
        return LeaguesListData(data, summoner_id=value["summonerId"])

    @transform.register(ChallengerLeagueListDto, ChallengerLeagueListData)
    def challenger_league_dto_to_data(self, value: ChallengerLeagueListDto, context: PipelineContext = None) -> ChallengerLeagueListData:
        data = deepcopy(value)
        return ChallengerLeagueListData.from_dto(data)

    @transform.register(MasterLeagueListDto, MasterLeagueListData)
    def master_league_dto_to_data(self, value: MasterLeagueListDto, context: PipelineContext = None) -> MasterLeagueListData:
        data = deepcopy(value)
        return MasterLeagueListData.from_dto(data)

    # Data to Core

    @transform.register(LeagueListData, League)
    def league_data_to_core(self, value: LeagueListData, context: PipelineContext = None) -> League:
        data = deepcopy(value)
        return League.from_data(data)

    @transform.register(LeaguesListData, Leagues)
    def leagues_data_to_core(self, value: LeaguesListData, context: PipelineContext = None) -> Leagues:
        return Leagues([self.league_data_to_core(page) for page in value], summoner=value.summoner_id)

    @transform.register(ChallengerLeagueListData, ChallengerLeague)
    def challenger_league_data_to_core(self, value: ChallengerLeagueListData, context: PipelineContext = None) -> ChallengerLeague:
        data = deepcopy(value)
        return ChallengerLeague.from_data(data)

    @transform.register(MasterLeagueListData, MasterLeague)
    def master_league_data_to_core(self, value: MasterLeagueListData, context: PipelineContext = None) -> MasterLeague:
        data = deepcopy(value)
        return MasterLeague.from_data(data)

    # Core to Dto

    @transform.register(League, LeagueListDto)
    def league_core_to_dto(self, value: League, context: PipelineContext = None) -> LeaguesListDto:
        return value._data[LeagueListData]._dto

    @transform.register(Leagues, LeaguesListDto)
    def leagues_core_to_dto(self, value: Leagues, context: PipelineContext = None) -> LeaguesListDto:
        return LeaguesListDto({"leagues": set([self.league_core_to_dto(page) for page in value]), "summonerId": value._Leagues__summoner.id})

    @transform.register(ChallengerLeague, ChallengerLeagueListDto)
    def challenger_league_core_to_dto(self, value: ChallengerLeague, context: PipelineContext = None) -> ChallengerLeagueListDto:
        return value._data[ChallengerLeagueListData]._dto

    @transform.register(MasterLeague, MasterLeagueListDto)
    def master_league_core_to_dto(self, value: MasterLeague, context: PipelineContext = None) -> MasterLeagueListDto:
        return value._data[MasterLeagueListData]._dto
