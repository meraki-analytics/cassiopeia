from typing import List, Dict
import datetime

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ..configuration import settings
from ..data import Region, Platform, GameMode, GameType, Queue, Map
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto import spectator as dto
from .staticdata.profileicon import ProfileIcon
from .staticdata.champion import Champion, ChampionData
from .staticdata.rune import Rune
from .staticdata.mastery import Mastery
from .staticdata.summonerspell import SummonerSpell
from .summoner import Summoner


##############
# Data Types #
##############


class RuneData(DataObject):
    _renamed = {"id": "runeId"}

    @property
    def id(self) -> int:
        """The ID of the rune"""
        return self._dto["runeId"]

    @property
    def count(self) -> int:
        """The count of this rune used by the participant"""
        return self._dto["count"]


class MasteryData(DataObject):
    _renamed = {"id": "masteryId"}

    @property
    def id(self) -> int:
        """The ID of the mastery"""
        return self._dto["masteryId"]

    @property
    def rank(self) -> int:
        """The number of points put into this mastery by the user"""
        return self._dto["rank"]


class CurrentGameParticipantData(DataObject):
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
    def summoner_name(self) -> int:
        """The summoner name of this participant"""
        return self._dto["summonerName"]

    @property
    def runes(self) -> List[RuneData]:
        """The runes used by this participant"""
        return self._dto["runes"]

    @property
    def masteries(self) -> List[MasteryData]:
        """The masteries used by this participant"""
        return self._dto["masteries"]

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


class TeamData(DataObject):
    _renamed = {}

    @property
    def participants(self) -> List[CurrentGameParticipantData]:
        return [CurrentGameParticipantData(p) for p in self._dto["participants"]]

    @property
    def bans(self) -> Dict[int, ChampionData]:
        return {b["pickTurn"]: ChampionData({"id": b["championId"]}) for b in self._dto["bans"]}


class CurrentGameInfoData(DataObject):
    _dto_type = dto.CurrentGameInfoDto
    _renamed = {"platform": "platformId", "observer_key": "observers", "creation": "gameStartTime", "duration": "gameLength", "mode": "gameMode", "map": "mapId", "type": "gameType", "queue": "gameQueueConfigId"}

    @property
    def id(self) -> int:
        return self._dto["gameId"]

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def platform(self) -> int:
        return self._dto["platformId"]

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
        return [TeamData(blue_team), TeamData(red_team)]

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


@searchable({})
class Participant(CassiopeiaObject):
    _data_types = {CurrentGameParticipantData}

    @property
    def champion(self) -> Champion:
        return Champion(id=self._data[CurrentGameParticipantData].champion_id)

    @property
    def summoner(self) -> Summoner:
        ProfileIcon(id=self._data[CurrentGameParticipantData].profile_icon_id)
        return Summoner(id=self._data[CurrentGameParticipantData].summoner_id, name=self._data[CurrentGameParticipantData].summoner_name)

    @property
    def runes(self) -> Dict[Rune, int]:
        return SearchableDictionary({Rune(id=rune.id): rune.count for rune in self._data[CurrentGameParticipantData].runes})

    @property
    def masteries(self) -> Dict[Mastery, int]:
        return SearchableDictionary({Mastery(id=mastery.id): mastery.rank for mastery in self._data[CurrentGameParticipantData].masteries})

    @property
    def is_bot(self) -> bool:
        return self._data[CurrentGameParticipantData].is_bot

    @property
    def team(self) -> "Team":
        raise NotImplemented  # TODO

    @property
    def summoner_spell_d(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summoner_spell_d)

    @property
    def summoner_spell_f(self) -> SummonerSpell:
        return SummonerSpell(id=self._data[CurrentGameParticipantData].summoner_spell_f)


@searchable({})
class Team(CassiopeiaObject):
    _data_types = {TeamData}

    @lazy_property
    def participants(self) -> List[Participant]:
        return SearchableList([Participant(p) for p in self._data[TeamData].participants])

    @lazy_property
    def bans(self) -> Dict[int, Champion]:
        return {pick: Champion(champ) for pick, champ in self._data[TeamData].bans.items()}


@searchable({})
class CurrentMatch(CassiopeiaGhost):
    _data_types = {CurrentGameInfoData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this summoner."""
        return Region(self._data[CurrentGameInfoData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this summoner."""
        return self.region.platform

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        return self._data[CurrentGameInfoData].id

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    @lazy
    def teams(self) -> List[Team]:
        return SearchableList([Team(team) for team in self._data[CurrentGameInfoData].teams])

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def blue_team(self) -> Team:
        return self._data[CurrentGameInfoData].teams[0]

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def red_team(self) -> Team:
        return self._data[CurrentGameInfoData].teams[1]

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def mode(self) -> GameMode:
        return GameMode(self._data[CurrentGameInfoData].mode)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def map(self) -> Map:
        return Map(self._data[CurrentGameInfoData].map)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def type(self) -> GameType:
        return GameType(self._data[CurrentGameInfoData].type)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def queue(self) -> Queue:
        return Queue(self._data[CurrentGameInfoData].queue)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def duration(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._data[CurrentGameInfoData].duration / 1000)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def creation(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._data[CurrentGameInfoData].creation / 1000)

    @CassiopeiaGhost.property(CurrentGameInfoData)
    @ghost_load_on(KeyError)
    def observer_key(self) -> str:
        return self._data[CurrentGameInfoData].observer_key
