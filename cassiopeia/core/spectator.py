from typing import List, Dict, Union
import datetime

from datapipelines import NotFoundError
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ..data import Region, Platform, GameMode, GameType, Queue
from .common import CoreData, DataObjectList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaList, get_latest_version, provide_default_region, ghost_load_on
from ..dto import spectator as dto
from .staticdata.profileicon import ProfileIcon
from .staticdata.champion import Champion
from .staticdata.rune import Rune
from .staticdata.mastery import Mastery
from .staticdata.summonerspell import SummonerSpell
from .staticdata.map import Map
from .summoner import Summoner


##############
# Data Types #
##############


class FeaturedGamesData(DataObjectList):
    _dto_type = dto.FeaturedGamesDto
    _renamed = {"client_refresh_interval": "clientRefreshInterval"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def client_refresh_interval(self) -> str:
        return self._dto["clientRefreshInterval"]

    @property
    def summoner_id(self) -> str:
        return self._dto["summonerId"]


class RuneData(CoreData):
    _renamed = {"id": "runeId"}

    @property
    def id(self) -> int:
        """The ID of the rune"""
        return self._dto["runeId"]

    @property
    def count(self) -> int:
        """The count of this rune used by the participant"""
        return self._dto["count"]


class MasteryData(CoreData):
    _renamed = {"id": "masteryId", "points": "rank"}

    @property
    def id(self) -> int:
        """The ID of the mastery"""
        return self._dto["masteryId"]

    @property
    def points(self) -> int:
        """The number of points put into this mastery by the user"""
        return self._dto["rank"]


class CurrentGameParticipantData(CoreData):
    _renamed = {"profile_icon_id": "profileIconId", "champion_id": "championId", "summoner_name": "summonerName", "summoner_id": "summonerId", "bot": "bot", "team_id": "teamId", "summoner_spell_f": "spell1Id", "summoner_spell_d": "spell2Id"}

    @property
    def profile_icon_id(self) -> int:
        """The ID of the profile icon used by this participant"""
        return self._dto["profileIconId"]

    @property
    def champion_id(self) -> int:
        """The ID of the champion played by this participant"""
        return self._dto["championId"]

    @property
    def summoner_id(self) -> int:
        """The summoner ID of this participant"""
        return self._dto["summonerId"]

    @property
    def summoner_name(self) -> str:
        """The summoner name of this participant"""
        return self._dto["summonerName"]

    @property
    def runes(self) -> List[RuneData]:
        """The runes used by this participant"""
        return [RuneData.from_dto(rune) for rune in self._dto["runes"]]

    @property
    def masteries(self) -> List[MasteryData]:
        """The masteries used by this participant"""
        return [MasteryData.from_dto(mastery) for mastery in self._dto["masteries"]]

    @property
    def is_bot(self) -> int:
        """Flag indicating whether or not this participant is a bot"""
        return self._dto["bot"]

    @property
    def team_id(self) -> int:
        """The team ID of this participant, indicating the participants team"""
        return self._dto["teamId"]

    @property
    def summoner_spell_d(self) -> int:
        """The ID of the first summoner spell used by this participant"""
        return self._dto["spell1Id"]

    @property
    def summoner_spell_f(self) -> int:
        """The ID of the second summoner spell used by this participant"""
        return self._dto["spell2Id"]


class TeamData(CoreData):
    _renamed = {}

    @property
    def participants(self) -> List[CurrentGameParticipantData]:
        return [CurrentGameParticipantData.from_dto(p) for p in self._dto["participants"]]

    @property
    def bans(self) -> Dict[int, int]:
        return {b["pickTurn"]: b["championId"] for b in self._dto["bans"]}


class CurrentGameInfoData(CoreData):
    _dto_type = dto.CurrentGameInfoDto
    _renamed = {"platform": "platformId", "observer_key": "observers", "creation": "gameStartTime", "duration": "gameLength", "mode": "gameMode", "map": "mapId", "type": "gameType", "queue": "gameQueueConfigId"}

    @property
    def id(self) -> int:
        return self._dto["gameId"]

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def teams(self) -> List[TeamData]:
        blue_team = {"participants": [], "bans": []}
        red_team = {"participants": [], "bans": []}
        for p in self._dto["participants"]:
            if p["teamId"] == 100:
                blue_team["participants"].append(p)
            elif p["teamId"] == 200:
                red_team["participants"].append(p)
        for b in self._dto["bannedChampions"]:
            if b["teamId"] == 100:
                blue_team["bans"].append(b)
            elif b["teamId"] == 200:
                red_team["bans"].append(b)
        return [TeamData.from_dto(blue_team), TeamData.from_dto(red_team)]

    @property
    def mode(self) -> str:
        return self._dto["gameMode"]

    @property
    def map(self) -> int:
        return self._dto["mapId"]

    @property
    def type(self) -> str:
        return self._dto["gameType"]

    @property
    def queue(self) -> int:
        return self._dto["gameQueueConfigId"]

    @property
    def duration(self) -> int:
        return self._dto["gameLength"]

    @property
    def creation(self) -> int:
        return self._dto["gameStartTime"]

    @property
    def observer_key(self) -> str:
        return self._dto["observers"]["encryptionKey"]


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
        return self._data[FeaturedGamesData].client_refresh_interval


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
        return Champion(id=self._data[CurrentGameParticipantData].champion_id, region=self.__region, version=get_latest_version(self.__region, endpoint="champion"))

    @property
    def summoner(self) -> Summoner:
        ProfileIcon(id=self._data[CurrentGameParticipantData].profile_icon_id, region=self.__region)
        if "summonerId" in self._data[CurrentGameParticipantData]._dto:
            return Summoner(id=self._data[CurrentGameParticipantData].summoner_id, name=self._data[CurrentGameParticipantData].summoner_name, region=self.__region)
        else:
            return Summoner(name=self._data[CurrentGameParticipantData].summoner_name, region=self.__region)

    @property
    def runes(self) -> Dict[Rune, int]:
        return SearchableDictionary({Rune(id=rune.id, region=self.__region, version=get_latest_version(self.__region, endpoint="rune")): rune.count for rune in self._data[CurrentGameParticipantData].runes})

    @property
    def masteries(self) -> Dict[Mastery, int]:
        return SearchableDictionary({Mastery(id=mastery.id, region=self.__region, version=get_latest_version(self.__region, endpoint="mastery")): mastery.points for mastery in self._data[CurrentGameParticipantData].masteries})

    @property
    def is_bot(self) -> bool:
        return self._data[CurrentGameParticipantData].is_bot

    @property
    def team(self) -> "Team":
        raise NotImplemented  # TODO

    @property
    def summoner_spell_d(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summoner_spell_d, region=self.__region, version=get_latest_version(self.__region, endpoint="summoner"))

    @property
    def summoner_spell_f(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summoner_spell_f, region=self.__region, version=get_latest_version(self.__region, endpoint="summoner"))


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
        return {pick: Champion(id=champion_id, region=self.__region, version=get_latest_version(self.__region, endpoint="champion")) for pick, champion_id in self._data[TeamData].bans.items()}


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
        return datetime.datetime.fromtimestamp(self._data[CurrentGameInfoData].creation / 1000)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on
    def observer_key(self) -> str:
        return self._data[CurrentGameInfoData].observer_key
