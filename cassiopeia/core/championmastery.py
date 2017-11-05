import datetime
from typing import Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform
from .common import CoreData, CassiopeiaGhost, CassiopeiaList, DataObjectList, get_latest_version, provide_default_region, ghost_load_on
from ..dto.championmastery import ChampionMasteryDto
from .staticdata.champion import Champion
from .summoner import Summoner
from ..dto import championmastery as dto


##############
# Data Types #
##############


class ChampionMasteryListData(DataObjectList):
    _dto_type = dto.ChampionMasteryListDto
    _renamed = {"summoner_id": "summonerId"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def summoner_id(self) -> str:
        return self._dto["summonerId"]


class ChampionMasteryData(CoreData):
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


class ChampionMasteries(CassiopeiaList):
    _data_types = {ChampionMasteryListData}

    @provide_default_region
    def __init__(self, *args, summoner: Union[Summoner, int, str], region: Union[Region, str] = None, _account_id: int = None):
        super().__init__(*args, region=region)
        if _account_id is not None:
            summoner = Summoner(account=_account_id, region=region)
        elif isinstance(summoner, str):
            summoner = Summoner(name=summoner, region=region)
        elif isinstance(summoner, int):
            summoner = Summoner(id=summoner, region=region)
        self.__summoner = summoner

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, int, str], region: Union[Region, str]) -> dict:
        query = {"region": region}
        if isinstance(summoner, Summoner):
            from .summoner import SummonerData
            summoner_data = summoner._data[SummonerData]
            try:
                query["summoner.id"] = summoner_data.id
            except KeyError:
                try:
                    query["summoner.account.id"] = summoner_data.account_id
                except KeyError:
                    query["summoner.name"] = summoner_data.name
        elif isinstance(summoner, str):
            query["summoner.name"] = summoner
        else:  # int
            query["summoner.id"] = summoner
        return query

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ChampionMasteryListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def summoner(self):
        return self.__summoner


@searchable({str: ["champion", "summoner"], int: ["points", "level"], bool: ["chest_granted"], datetime.datetime: ["last_played"], Champion: ["champion"], Summoner: ["summoner"]})
class ChampionMastery(CassiopeiaGhost):
    _data_types = {ChampionMasteryData}

    @provide_default_region
    def __init__(self, *, summoner: Union[Summoner, int, str] = None, champion: Union[Champion, int, str] = None, region: Union[Region, str] = None, _account_id: int = None):
        kwargs = {"region": region}

        if _account_id is not None:
            summoner = Summoner(account=_account_id, region=region)

        if summoner is not None:
            if isinstance(summoner, Summoner):
                self.__class__.summoner.fget._lazy_set(self, summoner)
            elif isinstance(summoner, str):
                summoner = Summoner(name=summoner, region=region)
                self.__class__.summoner.fget._lazy_set(self, summoner)
            else:  # int
                kwargs["summoner_id"] = summoner

        if champion is not None:
            if isinstance(champion, Champion):
                self.__class__.champion.fget._lazy_set(self, champion)
            elif isinstance(champion, str):
                champion = Champion(name=champion, region=self.region, version=get_latest_version(self.region, endpoint="champion"))
                self.__class__.champion.fget._lazy_set(self, champion)
            else:  # int
                kwargs["champion_id"] = champion

        super().__init__(**kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, int, str], champion: Union[Champion, int, str], region: Union[Region, str]) -> dict:
        query = {"region": region}
        if isinstance(summoner, Summoner):
            from .summoner import SummonerData
            summoner_data = summoner._data[SummonerData]
            try:
                query["summoner.id"] = summoner_data.id
            except KeyError:
                try:
                    query["summoner.account.id"] = summoner_data.account_id
                except KeyError:
                    query["summoner.name"] = summoner_data.name
        elif isinstance(summoner, str):
            query["summoner.name"] = summoner
        else:  # int
            query["summoner.id"] = summoner

        if isinstance(champion, Champion):
            from .staticdata.champion import ChampionData
            champion_data = champion._data[ChampionData]
            try:
                query["champion.id"] = champion_data.id
            except KeyError:
                query["champion.name"] = champion_data.name
        elif isinstance(champion, str):
            query["champion.name"] = champion
        else:  # int
            query["champion.id"] = champion
        return query

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform.value, "summoner.id": self.summoner.id, "champion.id": self.champion.id}

    def __load__(self, load_group: CoreData = None) -> None:
        from datapipelines import NotFoundError
        try:
            return super().__load__(load_group)
        except NotFoundError:
            from ..transformers.championmastery import ChampionMasteryTransformer
            dto = {
                "championLevel": 0,
                "chestGranted": False,
                "championPoints": 0,
                "championPointsUntilNextLevel": 1800,
                "championPointsSinceLastLevel": 0,
                "lastPlayTime": None
            }
            data = ChampionMasteryTransformer.champion_mastery_dto_to_data(None, dto)
            self.__load_hook__(load_group, data)

    @property
    def region(self) -> Region:
        return Region(self._data[ChampionMasteryData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(ChampionMasteryData)
    @lazy
    def champion(self) -> Champion:
        """Champion for this entry."""
        return Champion(id=self._data[ChampionMasteryData].champion_id, region=self.region, version=get_latest_version(self.region, endpoint="champion"))

    @CassiopeiaGhost.property(ChampionMasteryData)
    @lazy
    def summoner(self) -> Summoner:
        """Summoner for this entry."""
        return Summoner(id=self._data[ChampionMasteryData].summoner_id, region=self.region)

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def chest_granted(self) -> bool:
        """Is chest granted for this champion or not in current season?"""
        return self._data[ChampionMasteryData].chest_granted

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def level(self) -> int:
        """Champion level for specified player and champion combination."""
        return self._data[ChampionMasteryData].level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def points(self) -> int:
        """Total number of champion points for this player and champion combination - used to determine champion level."""
        return self._data[ChampionMasteryData].points

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def points_until_next_level(self) -> int:
        """Number of points needed to achieve next level. Zero if player reached maximum champion level for this champion."""
        return self._data[ChampionMasteryData].points_until_next_level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def points_since_last_level(self) -> int:
        """Number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion."""
        return self._data[ChampionMasteryData].points_since_last_level

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    @lazy
    def last_played(self) -> datetime.datetime:
        """Last time this champion was played by this player."""
        return datetime.datetime.fromtimestamp(self._data[ChampionMasteryData].last_played / 1000)
