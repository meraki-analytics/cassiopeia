from typing import List

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ..configuration import settings
from ..data import Region, Platform, Tier, Division, Queue
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto.league import LeagueListDto, LeagueItemDto, MiniSeriesDto
from .summoner import Summoner


##############
# Data Types #
##############


class MiniSeriesData(DataObject):
    _dto_type = MiniSeriesDto
    _renamed = {}

    @property
    def wins(self) -> int:
        return self._dto["wins"]

    @property
    def losses(self) -> int:
        return self._dto["losses"]

    @property
    def target(self) -> int:
        return self._dto["target"]

    @property
    def progress(self) -> str:
        return self._dto["progress"]


class LeagueItemData(DataObject):
    _dto_type = LeagueItemDto
    _renamed = {"hot_streak": "hotStreak", "promos": "miniSeries", "summoner_id": "playerOrTeamId", "summoner_name": "playerOrTeamName", "league_points": "leaguePoints", "league_name": "leagueName", "queue": "queueType", "division": "rank"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def tier(self) -> str:
        return self._dto["tier"]

    @property
    def queue(self) -> str:
        return self._dto["queue"]

    @property
    def league_name(self) -> str:
        return self._dto["leagueName"]

    @property
    def division(self) -> str:
        return self._dto["rank"]

    @property
    def hot_streak(self) -> bool:
        return self._dto["hotStreak"]

    @property
    def promos(self) -> MiniSeriesData:
        return MiniSeriesData(self._dto["miniSeries"])

    @property
    def wins(self) -> int:
        return self._dto["wins"]

    @property
    def veteran(self) -> bool:
        return self._dto["veteran"]

    @property
    def losses(self) -> int:
        return self._dto["losses"]

    @property
    def summoner_id(self) -> int:
        return self._dto["playerOrTeamId"]

    @property
    def summoner_name(self) -> str:
        return self._dto["playerOrTeamName"]

    @property
    def inactive(self) -> bool:
        return self._dto["inactive"]

    @property
    def fresh_blood(self) -> bool:
        return self._dto["fresh_blood"]

    @property
    def league_points(self) -> int:
        return self._dto["leaguePoints"]


class LeagueListData(DataObject):
    _dto_type = LeagueListDto
    _renamed = {"league_name": "name"}

    @property
    def tier(self) -> str:
        return self._dto["tier"]

    @property
    def queue(self) -> str:
        return self._dto["queue"]

    @property
    def league_name(self) -> str:
        return self._dto["name"]

    @property
    def entries(self) -> List[LeagueItemData]:
        return self._dto["entries"]


##############
# Core Types #
##############


class MiniSeries(CassiopeiaObject):
    _data_types = {MiniSeriesData}
    # Technically wins, loses, and wins_required can all be calculated from progress, so we don't technically need to store those data.

    @property
    def wins(self) -> int:
        return self._data[MiniSeriesData].wins  # sum(self.progress)

    @property
    def loses(self) -> int:
        return self._data[MiniSeriesData].loses  # len(self._data[MiniSeriesData].progress) - sum(self.progress)

    @property
    def wins_required(self) -> int:
        """2 or 3 wins will be required for promotion."""
        return self._data[MiniSeriesData].target  # len(self._data[MiniSeriesData].progress)

    @lazy_property
    def progress(self) -> List[bool]:
        """A list of True/False for the number of games the played in the mini series indicating if the player won or lost."""
        return [True if p == "W" else False for p in self._data[MiniSeriesData].progress if p is not None]


@searchable({str: ["region", "platform", "queue", "tier", "division", "league_name", "summoner"], bool: ["hot_streak", "veteran", "fresh_blood"], Region: ["region"], Platform: ["platform"], Queue: ["queue"], Tier: ["tier"], Division: ["division"], Summoner: ["summoner"]})
class LeagueSummoner(DataObject):
    _data_types = {LeagueItemData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[LeagueItemData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def tier(self) -> Tier:
        return Tier(self._data[LeagueItemData].tier)

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def queue(self) -> Queue:
        return Queue(self._data[LeagueItemData].queue)

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def league_name(self) -> str:
        return self._data[LeagueItemData].league_name

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def division(self) -> Division:
        return Division(self._data[LeagueItemData].division)

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def hot_streak(self) -> bool:
        return self._data[LeagueItemData].hot_streak

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def promos(self) -> MiniSeries:
        return MiniSeries(self._data[LeagueItemData].promos)

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def wins(self) -> int:
        return self._data[LeagueItemData].wins

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def veteran(self) -> bool:
        return self._data[LeagueItemData].veteran

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def losses(self) -> int:
        return self._data[LeagueItemData].losses

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def summoner(self) -> Summoner:
        return Summoner(id=self._data[LeagueItemData].summoner_id, name=self._data[LeagueItemData].summoner_name)

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def fresh_blood(self) -> bool:
        return self._data[LeagueItemData].fresh_blood

    @CassiopeiaGhost.property(LeagueItemData)
    @ghost_load_on(KeyError)
    def league_points(self) -> int:
        return self._data[LeagueItemData].league_points


#class Leagues(DataObject):
#    _data_types = {LeagueListData}
#
#    def __getitem__(self, item):
#        return self.entries[item]
#
#    def __len__(self):
#        return len(self.entries)
#
#    # TODO This load will be complicated because we need to get a LeagueSummoner
#    def __load__(self):
#        raise NotImplemented
#
#    @CassiopeiaGhost.property(LeagueListData)
#    @ghost_load_on(KeyError)
#    def tier(self) -> Tier:
#        return self._data[LeagueListData].tier
#
#    @CassiopeiaGhost.property(LeagueListData)
#    @ghost_load_on(KeyError)
#    def queue(self) -> Queue:
#        return self._data[LeagueListData].queue
#
#    @CassiopeiaGhost.property(LeagueListData)
#    @ghost_load_on(KeyError)
#    def league_name(self) -> str:
#        return self._data[LeagueListData].league_name
#
#    @CassiopeiaGhost.property(LeagueListData)
#    @ghost_load_on(KeyError)
#    def entries(self) -> List[LeagueSummoner]:
#        return self._data[LeagueListData].entries
