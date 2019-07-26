from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.league import LeagueEntry, LeagueEntries, LeagueEntriesData, LeagueSummonerEntries, LeagueSummonerEntriesData, League, ChallengerLeagueListData, ChallengerLeague, GrandmasterLeagueListData, GrandmasterLeague, MasterLeagueListData, MasterLeague, LeagueData, LeagueEntryData

from ..dto.league import LeagueDto, LeagueEntriesDto, LeagueSummonerEntriesDto, ChallengerLeagueListDto, GrandmasterLeagueListDto, MasterLeagueListDto, LeagueEntryDto

T = TypeVar("T")
F = TypeVar("F")


class LeagueTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Dto to Data

    @transform.register(LeagueDto, LeagueData)
    def league_dto_to_data(self, value: LeagueDto, context: PipelineContext = None) -> LeagueData:
        return LeagueData(**value)

    @transform.register(LeagueEntryDto, LeagueEntryData)
    def league_entry_dto_to_data(self, value: LeagueEntryDto, context: PipelineContext = None) -> LeagueEntryData:
        return LeagueEntryData(**value)

    @transform.register(LeagueSummonerEntriesDto, LeagueSummonerEntriesData)
    def leagues_summoner_entries_dto_to_data(self, value: LeagueSummonerEntriesDto, context: PipelineContext = None) -> LeagueSummonerEntriesData:
        data = deepcopy(value)
        for entry in data["entries"]:
            entry["region"] = data["region"]
        data = [LeagueTransformer.league_entry_dto_to_data(self, entry) for entry in data["entries"]]
        return LeagueSummonerEntriesData(data, summoner_id=value["summonerId"], region=value["region"])

    @transform.register(LeagueEntriesDto, LeagueEntriesData)
    def leagues_entries_dto_to_data(self, value: LeagueEntriesDto, context: PipelineContext = None) -> LeagueEntriesData:
        kwargs = {
            "region": value["region"],
            "queue": value["queue"],
            "tier": value["tier"],
            "division": value["division"],
            "page": value["page"]
        }
        return LeagueEntriesData([self.league_entry_dto_to_data(entry) for entry in value["entries"]], **kwargs)

    @transform.register(ChallengerLeagueListDto, ChallengerLeagueListData)
    def challenger_league_list_dto_to_data(self, value: ChallengerLeagueListDto, context: PipelineContext = None) -> ChallengerLeagueListData:
        return ChallengerLeagueListData(**value)

    @transform.register(GrandmasterLeagueListDto, GrandmasterLeagueListData)
    def grandmaster_league_list_dto_to_data(self, value: GrandmasterLeagueListDto, context: PipelineContext = None) -> GrandmasterLeagueListData:
        return GrandmasterLeagueListData(**value)

    @transform.register(MasterLeagueListDto, MasterLeagueListData)
    def master_league_list_dto_to_data(self, value: MasterLeagueListDto, context: PipelineContext = None) -> MasterLeagueListData:
        return MasterLeagueListData(**value)

    # Data to Core

    def league_data_to_core(self, value: LeagueData, context: PipelineContext = None) -> League:
        data = deepcopy(value)
        return League.from_data(data)

    @transform.register(LeagueEntryData, LeagueEntry)
    def league_entry_data_to_core(self, value: LeagueEntryData, context: PipelineContext = None) -> LeagueEntry:
        data = deepcopy(value)
        return LeagueEntry.from_data(data=data)

    @transform.register(LeagueEntriesData, LeagueEntries)
    def league_entries_data_to_core(self, value: LeagueEntriesData, context: PipelineContext = None) -> LeagueEntries:
        return LeagueEntries(*[LeagueTransformer.league_entry_data_to_core(self, entry) for entry in value], tier=value.tier, division=value.division, queue=value.queue, region=value.region)

    #@transform.register(ChallengerLeagueListData, ChallengerLeague)
    def challenger_league_list_data_to_core(self, value: ChallengerLeagueListData, context: PipelineContext = None) -> ChallengerLeague:
        data = deepcopy(value)
        return ChallengerLeague.from_data(data)

    #@transform.register(GrandmasterLeagueListData, GrandmasterLeague)
    def grandmaster_league_list_data_to_core(self, value: GrandmasterLeagueListData, context: PipelineContext = None) -> GrandmasterLeague:
        data = deepcopy(value)
        return GrandmasterLeague.from_data(data)

    #@transform.register(MasterLeagueListData, MasterLeague)
    def master_league_list_data_to_core(self, value: MasterLeagueListData, context: PipelineContext = None) -> MasterLeague:
        data = deepcopy(value)
        return MasterLeague.from_data(data)
