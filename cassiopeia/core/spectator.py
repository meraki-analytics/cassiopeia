from typing import List, Dict, Union
import datetime

from datapipelines import NotFoundError
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ..data import Region, Platform, GameMode, GameType, Queue, Side
from .common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaList, get_latest_version, provide_default_region, ghost_load_on
from ..dto import spectator as dto
from .staticdata.profileicon import ProfileIcon
from .staticdata.champion import Champion
from .staticdata.rune import Rune
from .staticdata.summonerspell import SummonerSpell
from .staticdata.map import Map
from .summoner import Summoner


##############
# Data Types #
##############


class FeaturedGamesData(CoreDataList):
    _dto_type = dto.FeaturedGamesDto
    _renamed = {}


class CurrentGameParticipantData(CoreData):
    _renamed = {"spell1Id": "summonerSpellFId", "spell2Id": "summonerSpellDId"}

    def __call__(self, **kwargs):
        if "perks" in kwargs:
            self.runes = kwargs.pop("perks")["perkIds"]
        super().__call__(**kwargs)
        return self


class TeamData(CoreData):
    _renamed = {}


class CurrentGameInfoData(CoreData):
    _dto_type = dto.CurrentGameInfoDto
    _renamed = {"platformId": "platform", "observers": "observerEncryptionKey", "gameStartTime": "creation", "gameLength": "duration", "gameMode": "mode", "mapId": "map", "gameType": "type", "gameQueueConfigId": "queue", "gameId": "id"}

    def __call__(self, **kwargs):
        if "observers" in kwargs:
            self.observerEncryptionKey = kwargs.pop("observers")["encryptionKey"]
        super().__call__(**kwargs)
        return self

    @property
    def teams(self) -> List[TeamData]:
        blue_team = {"participants": [], "bans": []}
        red_team = {"participants": [], "bans": []}
        for p in self.participants:
            if Side(p["teamId"]) is Side.blue:
                p = CurrentGameParticipantData(**p)
                blue_team["participants"].append(p)
            elif Side(p["teamId"]) is Side.red:
                p = CurrentGameParticipantData(**p)
                red_team["participants"].append(p)
        for b in self.bannedChampions:
            if Side(b["teamId"]) is Side.blue:
                blue_team["bans"].append(b)
            elif Side(b["teamId"]) is Side.red:
                red_team["bans"].append(b)
        return [TeamData(**blue_team), TeamData(**red_team)]


##############
# Core Types #
##############


class FeaturedMatches(CassiopeiaList):
    _data_types = {FeaturedGamesData}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[FeaturedGamesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def client_refresh_interval(self) -> int:
        return self._data[FeaturedGamesData].clientRefreshInterval


@searchable({str: ["summoner", "champion"], Summoner: ["summoner"], Champion: ["champion"]})
class Participant(CassiopeiaObject):
    _data_types = {CurrentGameParticipantData}

    @classmethod
    def from_data(cls, data: CoreData, region: Region):
        self = super().from_data(data)
        self.__region = region
        return self

    @property
    def champion(self) -> Champion:
        return Champion(id=self._data[CurrentGameParticipantData].championId, region=self.__region, version=get_latest_version(self.__region, endpoint="champion"))

    @property
    def summoner(self) -> Summoner:
        ProfileIcon(id=self._data[CurrentGameParticipantData].profileIconId, region=self.__region)
        if hasattr(self._data[CurrentGameParticipantData], "summonerId"):
            return Summoner(id=self._data[CurrentGameParticipantData].summonerId, name=self._data[CurrentGameParticipantData].summonerName, region=self.__region)
        else:
            return Summoner(name=self._data[CurrentGameParticipantData].summonerName, region=self.__region)

    @property
    def runes(self) -> List[Rune]:
        return SearchableList([Rune(id=rune_id, region=self.__region, version=get_latest_version(self.__region, endpoint="rune")) for rune_id in self._data[CurrentGameParticipantData].runes])

    @property
    def is_bot(self) -> bool:
        return self._data[CurrentGameParticipantData].isBot

    @property
    def team(self) -> Side:
        return Side(self._data[CurrentGameParticipantData].teamId)

    @property
    def side(self) -> Side:
        """Alias for team"""
        return Side(self._data[CurrentGameParticipantData].teamId)

    @property
    def summoner_spell_d(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summonerSpellDId, region=self.__region, version=get_latest_version(self.__region, endpoint="summoner"))

    @property
    def summoner_spell_f(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summonerSpellFId, region=self.__region, version=get_latest_version(self.__region, endpoint="summoner"))


@searchable({})
class Team(CassiopeiaObject):
    _data_types = {TeamData}

    @classmethod
    def from_data(cls, data: CoreData, region: Region):
        self = super().from_data(data)
        self.__region = region
        return self

    @lazy_property
    def participants(self) -> List[Participant]:
        return SearchableList([Participant.from_data(p, region=self.__region) for p in self._data[TeamData].participants])

    @lazy_property
    def bans(self) -> Dict[int, Champion]:
        return {pick: Champion(id=championId, region=self.__region, version=get_latest_version(self.__region, endpoint="champion")) for pick, championId in self._data[TeamData].bans.items()}


@searchable({})
class CurrentMatch(CassiopeiaGhost):
    _data_types = {CurrentGameInfoData}

    @provide_default_region
    def __init__(self, *, summoner: Union[Summoner, int, str] = None, region: Union[Region, str] = None):
        kwargs = {"region": region}

        if summoner is not None:
            if isinstance(summoner, str):
                summoner = Summoner(name=summoner, region=region)
            elif isinstance(summoner, int):
                summoner = Summoner(id=summoner, region=region)
            self.__summoner = summoner
        super().__init__(**kwargs)

    @classmethod
    def from_data(cls, data: CurrentGameInfoData, summoner: Union[Summoner, int, str]):
        self = super().from_data(data)
        if isinstance(summoner, str):
            summoner = Summoner(name=summoner, region=data.region)
        elif isinstance(summoner, int):
            summoner = Summoner(id=summoner, region=data.region)
        self.__summoner = summoner
        return self

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, int, str], region: Union[Region, str]) -> dict:
        query = {"region": region}
        if isinstance(summoner, Summoner):
            query["summoner.id"] = summoner.id
        elif isinstance(summoner, int):  # int
            query["summoner.id"] = summoner
        elif isinstance(summoner, str):
            query["summoner.id"] = Summoner(name=summoner, region=region).id
        assert "summoner.id" in query
        return query

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "summoner.id": self.__summoner.id}

    @property
    def exists(self):
        try:
            if not self._Ghost__all_loaded:
                self.__load__()
            self.creation  # Make sure we can access this attribute
            return True
        except (AttributeError, NotFoundError):
            return False

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[CurrentGameInfoData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def id(self) -> int:
        return self._data[CurrentGameInfoData].id

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    @lazy
    def teams(self) -> List[Team]:
        return SearchableList([Team.from_data(team, region=self.region) for team in self._data[CurrentGameInfoData].teams])

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def blue_team(self) -> Team:
        return self.teams[0]

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def red_team(self) -> Team:
        return self.teams[1]

    @property
    def participants(self) -> List[Participant]:
        return SearchableList([*self.blue_team.participants, *self.red_team.participants])

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def mode(self) -> GameMode:
        return GameMode(self._data[CurrentGameInfoData].mode)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def map(self) -> Map:
        return Map(id=self._data[CurrentGameInfoData].map, region=self.region, version=get_latest_version(self.region, endpoint="map"))

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def type(self) -> GameType:
        return GameType(self._data[CurrentGameInfoData].type)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def queue(self) -> Queue:
        return Queue.from_id(self._data[CurrentGameInfoData].queue)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def duration(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self._data[CurrentGameInfoData].duration)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def creation(self) -> datetime.datetime:
        return datetime.datetime.utcfromtimestamp(self._data[CurrentGameInfoData].creation / 1000)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def observer_key(self) -> str:
        return self._data[CurrentGameInfoData].observerEncryptionKey
