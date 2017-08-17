from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.league import Leagues, LeaguePositionData, LeaguePositionsData, LeagueEntry, LeagueEntries, LeaguesListData, LeagueListData, League, ChallengerLeagueListData, ChallengerLeague, MasterLeagueListData, MasterLeague

from ..dto.league import LeaguesListDto, LeagueListDto, ChallengerLeagueListDto, MasterLeagueListDto, LeaguePositionDto, LeaguePositionsDto

T = TypeVar("T")
F = TypeVar("F")


class LeagueTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(LeaguePositionDto, LeaguePositionData)
    def league_position_dto_to_data(self, value: LeaguePositionDto, context: PipelineContext = None) -> LeaguePositionData:
        data = deepcopy(value)
        return LeaguePositionData.from_dto(data)

    @transform.register(LeaguePositionsDto, LeaguePositionsData)
    def league_positions_dto_to_data(self, value: LeaguePositionsDto, context: PipelineContext = None) -> LeaguePositionsData:
        data = deepcopy(value)
        data = [LeagueTransformer.league_position_dto_to_data(self, league) for league in data["positions"]]
        return LeaguePositionsData(data, summoner_id=value["summonerId"], region=value["region"])

    @transform.register(LeagueListDto, LeagueListData)
    def league_list_dto_to_data(self, value: LeagueListDto, context: PipelineContext = None) -> LeagueListData:
        data = deepcopy(value)
        return LeagueListData.from_dto(data)

    @transform.register(LeaguesListDto, LeaguesListData)
    def leagues_list_dto_to_data(self, value: LeaguesListDto, context: PipelineContext = None) -> LeaguesListData:
        data = deepcopy(value)
        for league in data["leagues"]:
            league["region"] = data["region"]
            league["summonerId"] = data["summonerId"]
            for entry in league["entries"]:
                entry["tier"] = league["tier"]
                entry["leagueName"] = league["name"]
                entry["queue"] = league["queue"]
                entry["region"] = league["region"]
        data = [LeagueTransformer.league_list_dto_to_data(self, league) for league in data["leagues"]]
        return LeaguesListData(data, summoner_id=value["summonerId"], region=value["region"])

    @transform.register(ChallengerLeagueListDto, ChallengerLeagueListData)
    def challenger_league_list_dto_to_data(self, value: ChallengerLeagueListDto, context: PipelineContext = None) -> ChallengerLeagueListData:
        data = deepcopy(value)
        return ChallengerLeagueListData.from_dto(data)

    @transform.register(MasterLeagueListDto, MasterLeagueListData)
    def master_league_list_dto_to_data(self, value: MasterLeagueListDto, context: PipelineContext = None) -> MasterLeagueListData:
        data = deepcopy(value)
        return MasterLeagueListData.from_dto(data)

    # Data to Core

    @transform.register(LeaguePositionData, LeagueEntry)
    def league_position_data_to_core(self, value: LeaguePositionData, context: PipelineContext = None) -> LeagueEntry:
        data = deepcopy(value)
        return LeagueEntry.from_data(data)

    @transform.register(LeaguePositionsData, LeagueEntries)
    def league_positions_data_to_core(self, value: LeaguePositionsData, context: PipelineContext = None) -> LeagueEntries:
        data = deepcopy(value)
        return LeagueEntries([LeagueTransformer.league_position_data_to_core(self, position) for position in data], summoner=value.summoner_id, region=value.region)

    @transform.register(LeagueListData, League)
    def league_list_data_to_core(self, value: LeagueListData, context: PipelineContext = None) -> League:
        data = deepcopy(value)
        return League.from_data(data)

    @transform.register(LeaguesListData, Leagues)
    def leagues_list_data_to_core(self, value: LeaguesListData, context: PipelineContext = None) -> Leagues:
        return Leagues([LeagueTransformer.league_list_data_to_core(self, league) for league in value], summoner=value.summoner_id, region=value.region)

    @transform.register(ChallengerLeagueListData, ChallengerLeague)
    def challenger_league_list_data_to_core(self, value: ChallengerLeagueListData, context: PipelineContext = None) -> ChallengerLeague:
        data = deepcopy(value)
        return ChallengerLeague.from_data(data)

    @transform.register(MasterLeagueListData, MasterLeague)
    def master_league_list_data_to_core(self, value: MasterLeagueListData, context: PipelineContext = None) -> MasterLeague:
        data = deepcopy(value)
        return MasterLeague.from_data(data)

    # Core to Dto

    @transform.register(LeagueEntry, LeaguePositionDto)
    def league_position_core_to_dto(self, value: LeagueEntry, context: PipelineContext = None) -> LeaguePositionDto:
        return value._data[LeaguePositionData]._dto

    @transform.register(LeagueEntries, LeaguePositionsDto)
    def league_positions_core_to_dto(self, value: LeagueEntries, context: PipelineContext = None) -> LeaguePositionsDto:
        return LeaguePositionsDto({"positions": set([LeagueTransformer.league_position_core_to_dto(self, position) for position in value]), "summonerId": value._LeagueEntries__summoner.id, "region": value.region})

    @transform.register(League, LeagueListDto)
    def league_list_core_to_dto(self, value: League, context: PipelineContext = None) -> LeaguesListDto:
        return value._data[LeagueListData]._dto

    @transform.register(Leagues, LeaguesListDto)
    def leagues_list_core_to_dto(self, value: Leagues, context: PipelineContext = None) -> LeaguesListDto:
        return LeaguesListDto({"leagues": set([LeagueTransformer.league_list_core_to_dto(self, league) for league in value]), "summonerId": value._Leagues__summoner.id, "region": value.region})

    @transform.register(ChallengerLeague, ChallengerLeagueListDto)
    def challenger_league_list_core_to_dto(self, value: ChallengerLeague, context: PipelineContext = None) -> ChallengerLeagueListDto:
        return value._data[ChallengerLeagueListData]._dto

    @transform.register(MasterLeague, MasterLeagueListDto)
    def master_league_list_core_to_dto(self, value: MasterLeague, context: PipelineContext = None) -> MasterLeagueListDto:
        return value._data[MasterLeagueListData]._dto
