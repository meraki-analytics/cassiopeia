import arrow
from typing import Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform
from .common import CoreData, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, CoreDataList, get_latest_version, provide_default_region, ghost_load_on
from ..dto.championmastery import ChampionMasteryDto
from .staticdata.champion import Champion
from .summoner import Summoner
from ..dto import championmastery as dto


##############
# Data Types #
##############


class ChampionMasteryListData(CoreDataList):
    _dto_type = dto.ChampionMasteryListDto
    _renamed = {}


class ChampionMasteryData(CoreData):
    _dto_type = ChampionMasteryDto
    _renamed = {"championLevel": "level", "championPoints": "points", "playerId": "summonerId", "championPointsUntilNextLevel": "pointsUntilNextLevel", "championPointsSinceLastLevel": "pointsSinceLastLevel", "lastPlayTime": "lastPlayed", "tokensEarned": "tokens"}


##############
# Core Types #
##############


class ChampionMasteries(CassiopeiaLazyList):
    _data_types = {ChampionMasteryListData}

    @provide_default_region
    def __init__(self, *, summoner: Summoner, region: Union[Region, str] = None):
        self.__summoner = summoner
        kwargs = {"region": region}
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, int, str], region: Union[Region, str]) -> dict:
        query = {"region": region}
        if isinstance(summoner, Summoner):
            query["summoner.id"] = summoner.id
        elif isinstance(summoner, str):
            if len(summoner) < 35:
                # It's a summoner name
                query["summoner.id"] = Summoner(name=summoner, region=region).id
            else:
                # It's probably a summoner id
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


@searchable({str: ["champion", "summoner"], int: ["points", "level"], bool: ["chest_granted"], arrow.Arrow: ["last_played"], Champion: ["champion"], Summoner: ["summoner"]})
class ChampionMastery(CassiopeiaGhost):
    _data_types = {ChampionMasteryData}

    @provide_default_region
    def __init__(self, *, summoner: Union[Summoner, int, str] = None, champion: Union[Champion, int, str] = None, region: Union[Region, str] = None, _account_id: str = None):
        kwargs = {"region": region}

        if _account_id is not None:
            summoner = Summoner(account_id=_account_id, region=region)

        if summoner is not None:
            if isinstance(summoner, Summoner):
                self.__class__.summoner.fget._lazy_set(self, summoner)
            elif isinstance(summoner, str):
                if len(summoner) < 35:
                    # It's a summoner name
                    summoner = Summoner(name=summoner, region=region)
                    self.__class__.summoner.fget._lazy_set(self, summoner)
                else:
                    # It's probably a summoner id
                    kwargs["summonerId"] = summoner

        if champion is not None:
            if isinstance(champion, Champion):
                self.__class__.champion.fget._lazy_set(self, champion)
            elif isinstance(champion, str):
                champion = Champion(name=champion, region=self.region, version=get_latest_version(self.region, endpoint="champion"))
                self.__class__.champion.fget._lazy_set(self, champion)
            else:  # int
                kwargs["championId"] = champion

        super().__init__(**kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, int, str], champion: Union[Champion, int, str], region: Union[Region, str]) -> dict:
        query = {"region": region}
        if isinstance(summoner, Summoner):
            query["summoner.id"] = summoner.id
        elif isinstance(summoner, str):
            if len(summoner) < 35:
                # It's a summoner name
                query["summoner.id"] = Summoner(name=summoner, region=region).id
            else:
                # It's probably a summoner id
                query["summoner.id"] = summoner
            

        if isinstance(champion, Champion):
            query["champion.id"] = champion.id
        elif isinstance(champion, str):
            query["champion.id"] = Champion(name=champion, region=region).id
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
                "tokensEarned": 0,
                "championPointsSinceLastLevel": 0,
                "lastPlayTime": None
            }
            data = ChampionMasteryTransformer.champion_mastery_dto_to_data(None, dto)
            self.__load_hook__(load_group, data)

    def __eq__(self, other: "ChampionMastery"):
        if not isinstance(other, ChampionMastery) or self.region != other.region:
            return False
        return self.champion == other.champion and self.summoner == other.summoner

    def __str__(self):
        return "ChampionMastery(summoner={summoner}, champion={champion})".format(summoner=str(self.summoner), champion=str(self.champion))

    __hash__ = CassiopeiaGhost.__hash__

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
        return Champion(id=self._data[ChampionMasteryData].championId, region=self.region, version=get_latest_version(self.region, endpoint="champion"))

    @CassiopeiaGhost.property(ChampionMasteryData)
    @lazy
    def summoner(self) -> Summoner:
        """Summoner for this entry."""
        return Summoner(id=self._data[ChampionMasteryData].summonerId, region=self.region)

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def chest_granted(self) -> bool:
        """Is chest granted for this champion or not in current season?"""
        return self._data[ChampionMasteryData].chestGranted

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
        return self._data[ChampionMasteryData].pointsUntilNextLevel

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def tokens(self) -> int:
        """Number of tokens earned toward next mastery level."""
        return self._data[ChampionMasteryData].tokens

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    def points_since_last_level(self) -> int:
        """Number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion."""
        return self._data[ChampionMasteryData].pointsSinceLastLevel

    @CassiopeiaGhost.property(ChampionMasteryData)
    @ghost_load_on
    @lazy
    def last_played(self) -> arrow.Arrow:
        """Last time this champion was played by this player."""
        return arrow.get(self._data[ChampionMasteryData].lastPlayed / 1000)
