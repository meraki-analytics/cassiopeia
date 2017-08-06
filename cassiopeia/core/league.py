from typing import List, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy_property, lazy
from merakicommons.container import searchable, SearchableList

from ..configuration import settings
from ..data import Region, Platform, Tier, Division, Queue
from .common import CoreData, DataObjectList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList
from ..dto.league import LeaguesListDto, LeagueListDto, LeagueItemDto, MiniSeriesDto
from .summoner import Summoner


##############
# Data Types #
##############


class MiniSeriesData(CoreData):
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


class LeagueItemData(CoreData):
    _dto_type = LeagueItemDto
    _renamed = {"hot_streak": "hotStreak", "promos": "miniSeries", "summoner_id": "playerOrTeamId", "summoner_name": "playerOrTeamName", "league_points": "leaguePoints", "name": "leagueName", "queue": "queueType", "division": "rank", "fresh_blood": "freshBlood"}

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
    def name(self) -> str:
        return self._dto["leagueName"]

    @property
    def division(self) -> str:
        return self._dto["rank"]

    @property
    def hot_streak(self) -> bool:
        return self._dto["hotStreak"]

    @property
    def promos(self) -> MiniSeriesData:
        return MiniSeriesData.from_dto(self._dto["miniSeries"])

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
        return int(self._dto["playerOrTeamId"])

    @property
    def summoner_name(self) -> str:
        return self._dto["playerOrTeamName"]

    @property
    def inactive(self) -> bool:
        return self._dto["inactive"]

    @property
    def fresh_blood(self) -> bool:
        return self._dto["freshBlood"]

    @property
    def league_points(self) -> int:
        return self._dto["leaguePoints"]


class LeagueListData(CoreData):
    _dto_type = LeagueListDto
    _renamed = {}

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
    def name(self) -> str:
        return self._dto["name"]

    @property
    def entries(self) -> List[LeagueItemData]:
        return [LeagueItemData.from_dto(entry) for entry in self._dto["entries"]]


class LeaguesListData(DataObjectList):
    _dto_type = LeaguesListDto
    _renamed = {"summoner_id": "summonerId"}

    @property
    def summoner_id(self) -> str:
        return self._dto["summonerId"]

    @property
    def region(self) -> str:
        return self._dto["region"]


class ChallengerLeagueListData(LeagueListData):
    pass


class MasterLeagueListData(LeagueListData):
    pass


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


@searchable({str: ["division", "name", "summoner"], bool: ["hot_streak", "veteran", "fresh_blood"], Division: ["division"], Summoner: ["summoner"]})
class LeagueEntry(CassiopeiaObject):
    _data_types = {LeagueItemData}

    def __init__(self, *, region: Union[Region, str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[LeagueItemData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @lazy_property
    def tier(self) -> Tier:
        return Tier(self._data[LeagueItemData].tier)

    @lazy_property
    def queue(self) -> Queue:
        return Queue(self._data[LeagueItemData].queue)

    @property
    def name(self) -> str:
        return self._data[LeagueItemData].name

    @lazy_property
    def division(self) -> Division:
        return Division(self._data[LeagueItemData].division)

    @property
    def hot_streak(self) -> bool:
        return self._data[LeagueItemData].hot_streak

    @lazy_property
    def promos(self) -> MiniSeries:
        return MiniSeries.from_data(self._data[LeagueItemData].promos)

    @property
    def wins(self) -> int:
        return self._data[LeagueItemData].wins

    @property
    def veteran(self) -> bool:
        return self._data[LeagueItemData].veteran

    @property
    def losses(self) -> int:
        return self._data[LeagueItemData].losses

    @lazy_property
    def summoner(self) -> Summoner:
        return Summoner(id=self._data[LeagueItemData].summoner_id, name=self._data[LeagueItemData].summoner_name)

    @property
    def fresh_blood(self) -> bool:
        return self._data[LeagueItemData].fresh_blood

    @property
    def league_points(self) -> int:
        return self._data[LeagueItemData].league_points


@searchable({str: ["tier", "queue", "name"], Queue: ["queue"], Tier: ["tier"]})
class League(CassiopeiaObject):
    _data_types = {LeagueListData}

    def __getitem__(self, item):
        return self.entries[item]

    def __len__(self):
        return len(self.entries)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LeaguesListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @lazy_property
    def tier(self) -> Tier:
        return Tier(self._data[LeagueListData].tier)

    @lazy_property
    def queue(self) -> Queue:
        return Queue(self._data[LeagueListData].queue)

    @property
    def name(self) -> str:
        return self._data[LeagueListData].name

    @lazy_property
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[LeagueListData].entries])


class Leagues(CassiopeiaGhostList):
    _data_types = {LeaguesListData}

    def __init__(self, *args, summoner: Union[Summoner, int, str], region: Union[Region, str] = None):
        super().__init__(*args, region=region)
        if isinstance(summoner, str):
            summoner = Summoner(name=summoner)
        elif isinstance(summoner, int):
            summoner = Summoner(id=summoner)
        self.__summoner = summoner

    def __get_query__(self):
        return {"summoner.id": self.__summoner.id, "region": self.region, "platform": self.platform}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        self.clear()
        from ..transformers.leagues import LeagueTransformer
        SearchableList.__init__(self, [LeagueTransformer.league_data_to_core(None, i) for i in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LeaguesListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def fives(self):
        return self[Queue.ranked_solo]

    @property
    def flex(self):
        return self[Queue.flex]

    @property
    def threes(self):
        return self[Queue.ranked_threes]


class ChallengerLeague(League, CassiopeiaGhost):
    _data_types = {ChallengerLeagueListData}

    def __init__(self, *, queue: Union[Queue, str, int] = None, region: Union[Region, str] = None):
        kwargs = {"region": region}
        if isinstance(queue, int):
            kwargs["queue"] = Queue.from_id(queue)
        elif isinstance(queue, str):
            kwargs["queue"] = Queue(queue)
        elif isinstance(queue, Queue):
            kwargs["queue"] = queue
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "queue": self.queue}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ChallengerLeagueListData].region)

    @lazy_property
    def tier(self) -> Tier:
        return Tier.challenger

    @lazy_property
    def queue(self) -> Queue:
        return Queue(self._data[ChallengerLeagueListData].queue)

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[ChallengerLeagueListData].name

    @CassiopeiaGhost.property(ChallengerLeagueListData)
    @ghost_load_on(KeyError)
    @lazy
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[ChallengerLeagueListData].entries])


class MasterLeague(League, CassiopeiaGhost):
    _data_types = {MasterLeagueListData}

    def __init__(self, *, queue: Union[Queue, str, int] = None, region: Union[Region, str] = None):
        kwargs = {"region": region}
        if isinstance(queue, int):
            kwargs["queue"] = Queue.from_id(queue)
        elif isinstance(queue, str):
            kwargs["queue"] = Queue(queue)
        elif isinstance(queue, Queue):
            kwargs["queue"] = queue
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "queue": self.queue}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MasterLeagueListData].region)

    @lazy_property
    def tier(self) -> Tier:
        return Tier.master

    @lazy_property
    def queue(self) -> Queue:
        return Queue(self._data[MasterLeagueListData].queue)

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[MasterLeagueListData].name

    @CassiopeiaGhost.property(MasterLeagueListData)
    @ghost_load_on(KeyError)
    @lazy
    def entries(self) -> List[LeagueEntry]:
        return SearchableList([LeagueEntry.from_data(entry) for entry in self._data[MasterLeagueListData].entries])
