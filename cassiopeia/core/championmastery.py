import datetime

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ..configuration import settings
from ..data import Region, Platform
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto.championmastery import ChampionMasteryDto
from .staticdata.champion import Champion
from .summoner import Summoner
from ..dto import championmastery as dto


##############
# Data Types #
##############


class ChampionMasteryListData(list):
    _dto_type = dto.ChampionMasteryListDto


class ChampionMasteryData(DataObject):
    _dto_type = ChampionMasteryDto
    _renamed = {"chest_granted": "chestGranted", "level": "championLevel", "points": "championPoints", "champion_id": "championId", "summoner_id": "playerId", "points_until_next_level": "championPointsUntilNextLevel", "points_since_last_level": "championPointsSinceLastLevel", "last_played": "lastPlayTime"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def champion_id(self) -> int:
        return self._dto["championId"]

    @property
    def summoner_id(self) -> int:
        return self._dto["playerId"]

    @property
    def chest_granted(self) -> bool:
        return self._dto["chestGranted"]

    @property
    def level(self) -> int:
        return self._dto["championLevel"]

    @property
    def points(self) -> int:
        return self._dto["championPoints"]

    @property
    def points_until_next_level(self) -> int:
        return self._dto["championPointsUntilNextLevel"]

    @property
    def points_since_last_level(self) -> int:
        return self._dto["championPointsSinceLastLevel"]

    @property
    def last_played(self) -> int:
        return self._dto["lastPlayTime"]


##############
# Core Types #
##############


@searchable({str: ["champion", "summoner"], int: ["points", "level"], bool: ["chest_granted"], datetime.datetime: ["last_played"], Champion: ["champion"], Summoner: ["summoner"]})
class ChampionMastery(CassiopeiaGhost):
    _data_types = {ChampionMasteryData}
    _retyped = {
      "summoner": {
        Summoner: ("id", "summoner_id"),
        int: (None, "summoner_id")
      },
      "champion": {
        Champion: ("id", "champion_id"),
        int: (None, "champion_id")
      },
      "region": {
        Region: ("value", "region")
      },
      "platform": {
        Platform: ("value", "platform")
      }
    }

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    def __load__(self, load_group: DataObject = None) -> None:
        from datapipelines import NotFoundError
        try:
            super().__load__(load_group)
        except NotFoundError:
            dto = {
                "championLevel": 0,
                "chestGranted": False,
                "championPoints": 0,
                "championPointsUntilNextLevel": None,  # TODO what is this value?
                "championPointsSinceLastLevel": 0,
                "lastPlayTime": None
            }
            self.__load_hook__(load_group, dto)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ChampionData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @CassiopeiaGhost.property(ChampionMasteryData)
    @lazy
    def champion(self) -> Champion:
        """Champion for this entry."""
        return Champion(id=self._data[ChampionMasteryData].champion_id)

    @CassiopeiaGhost.property(ChampionMasteryData)
    @lazy
    def summoner(self) -> Summoner:
        """Summoner for this entry."""
        return Summoner(id=self._data[ChampionMasteryData].summoner_id)

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    def chest_granted(self) -> bool:
        """Is chest granted for this champion or not in current season?"""
        return self._data[ChampionMasteryData].chest_granted

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    def level(self) -> int:
        """Champion level for specified player and champion combination."""
        return self._data[ChampionMasteryData].level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    def points(self) -> int:
        """Total number of champion points for this player and champion combination - used to determine champion level."""
        return self._data[ChampionMasteryData].points

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    def points_until_next_level(self) -> int:
        """Number of points needed to achieve next level. Zero if player reached maximum champion level for this champion."""
        return self._data[ChampionMasteryData].points_until_next_level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    def points_since_last_level(self) -> int:
        """Number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion."""
        return self._data[ChampionMasteryData].points_since_last_level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on(KeyError)
    @lazy
    def last_played(self) -> datetime.datetime:
        """Last time this champion was played by this player."""
        return datetime.datetime.fromtimestamp(self._data[ChampionMasteryData].last_played / 1000)
