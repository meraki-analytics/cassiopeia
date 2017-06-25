import os
import datetime
from typing import List, Tuple
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ..configuration import settings
from ..data import Region, Platform, Tier, Map, GameType, GameMode, Queue, Division, Side, Season
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto import match as dto
from .staticdata.version import VersionListData


# TODO Implement timelines


##############
# Data Types #
##############


class MatchListData(list):
    pass


class ParticipantTimelineData(DataObject):  # TODO
    pass
#ParticipantTimelineDto
#lane    string
#participantId   int
#csDiffPerMinDeltas  Map[string, double]
#goldPerMinDeltas    Map[string, double]
#xpDiffPerMinDeltas  Map[string, double]
#creepsPerMinDeltas  Map[string, double]
#xpPerMinDeltas  Map[string, double]
#role    string
#damageTakenDiffPerMinDeltas Map[string, double]
#damageTakenPerMinDeltas Map[string, double]

class ParticipantStatsData(DataObject):  # TODO
    pass
#ParticipantStatsDto 
#physicalDamageDealt long    
#neutralMinionsKilledTeamJungle  int 
#magicDamageDealt    long    
#totalPlayerScore    int 
#deaths  int 
#win boolean 
#neutralMinionsKilledEnemyJungle int 
#altarsCaptured  int 
#largestCriticalStrike   int 
#totalDamageDealt    long    
#magicDamageDealtToChampions long    
#visionWardsBoughtInGame int 
#damageDealtToObjectives long    
#largestKillingSpree int 
#item1   int 
#quadraKills int 
#teamObjective   int 
#totalTimeCrowdControlDealt  int 
#longestTimeSpentLiving  int 
#wardsKilled int 
#firstTowerAssist    boolean 
#firstTowerKill  boolean 
#item2   int 
#item3   int 
#item0   int 
#firstBloodAssist    boolean 
#visionScore long    
#wardsPlaced int 
#item4   int 
#item5   int 
#item6   int 
#turretKills int 
#tripleKills int 
#damageSelfMitigated long    
#champLevel  int 
#nodeNeutralizeAssist    int 
#firstInhibitorKill  boolean 
#goldEarned  int 
#magicalDamageTaken  long    
#kills   int 
#doubleKills int 
#nodeCaptureAssist   int 
#trueDamageTaken long    
#nodeNeutralize  int 
#firstInhibitorAssist    boolean 
#assists int 
#unrealKills int 
#neutralMinionsKilled    int 
#objectivePlayerScore    int 
#combatPlayerScore   int 
#damageDealtToTurrets    long    
#altarsNeutralized   int 
#physicalDamageDealtToChampions  long    
#goldSpent   int 
#trueDamageDealt long    
#trueDamageDealtToChampions  long    
#participantId   int 
#pentaKills  int 
#totalHeal   long    
#totalMinionsKilled  int 
#firstBloodKill  boolean 
#nodeCapture int 
#largestMultiKill    int 
#sightWardsBoughtInGame  int 
#totalDamageDealtToChampions long    
#totalUnitsHealed    int 
#inhibitorKills  int 
#totalScoreRank  int 
#totalDamageTaken    long    
#killingSprees   int 
#timeCCingOthers long    
#physicalDamageTaken long    


class ParticipantData(DataObject):
    _renamed = {"id": "participantId", "team": "teamId", "summoner_spell_d": "spell1Id", "summoner_spell_f": "spell2Id", "champion_id": "championId", "rank_last_season":"highestAchievedSeasonTier"}

    @property
    def stats(self) -> ParticipantStatsData:
        return ParticipantStatsData(self._dto["stats"])

    @property
    def id(self) -> int:
        return self._dto["participantId"]

    @property
    def runes(self) -> List["RuneData"]:
        return self._dto["runes"]

    @property
    def masteries(self) -> List["MasteryData"]:
        return self._dto["masteries"]

    @property
    def timeline(self) -> ParticipantTimelineData:
        return ParticipantTimelineData(self._dto["timeline"])

    @property
    def team(self) -> "TeamData":
        return TeamData(self._dto["teamId"])

    @property
    def summoner_spell_d(self) -> "SummonerSpellData":
        return self._dto["spell1Id"]

    @property
    def summoner_spell_f(self) -> "SummonerSpellData":
        return self._dto["spell2Id"]

    @property
    def rank_last_season(self) -> Tuple[str, int]:
        return self._dto["highestAchievedSeasonTier"]

    @property
    def champion_id(self) -> int:
        return self._dto["championId"]


class ProfileIconData(DataObject):
    _renamed = {"id": "profileIconId"}

    @property
    def id(self) -> int:
        return self._dto["profileIconId"]


class PlayerData(DataObject):
    _renamed = {"current_platform_id": "currentPlatformId", "summoner_name": "summonerName", "summoner_id": "summonerId", "match_history_uri": "matchHistoryUri", "platform_id": "platformId", "current_account_id": "currentAccountId", "profile_icon": "profileIcon", "account_id": "accountId"}

    @property
    def current_platform_id(self) -> int:
        return self._dto["currentPlatformId"]

    @property
    def summoner_id(self) -> int:
        return self._dto["summonerId"]

    @property
    def summoner_name(self) -> str:
        return self._dto["summonerName"]

    @property
    def match_history_uri(self) -> str:
        return self._dto["matchHistoryUri"]

    @property
    def platform_id(self) -> int:
        return self._dto["platformId"]

    @property
    def profile_icon(self) -> ProfileIconData:
        return ProfileIconData(self._dto["profileIcon"])

    @property
    def current_account_id(self) -> int:
        return self._dto["currentAccountId"]

    @property
    def account_id(self) -> int:
        return self._dto["accountId"]


class ParticipantIdentityData(DataObject):
    _renamed = {"id": "participantId"}

    @property
    def player(self) -> PlayerData:
        return PlayerData(self._dto["player"])

    @property
    def id(self) -> int:
        return self._dto["participantId"]


class TeamData(DataObject):
    _renamed = {"first_dragon": "firstDragon", "first_inhibitor": "firstInhibitor", "first_rift_herald": "firstRiftHerald", "first_baron": "firstBaron", "first_tower": "firstTower", "first_blood": "firstBlood", "baron_kills": "baronKills", "rift_herald_kills": "riftHeraldKills", "vilemaw_kills": "vilemawKills", "inhibitor_kills": "inhibitorKills", "tower_kills": "towerKills", "dragon_kills": "dragonKills", "dominion_victory_score": "dominionVictoryScore", "side": "teamId"}

    @property
    def first_dragon(self) -> bool:
        return self._dto["firstDragon"]

    @property
    def first_inhibitor(self) -> bool:
        return self._dto["firstInhibitor"]

    @property
    def first_rift_herald(self) -> bool:
        return self._dto["firstRiftHerald"]

    @property
    def first_baron(self) -> bool:
        return self._dto["firstBaron"]

    @property
    def first_tower(self) -> bool:
        return self._dto["firstTower"]

    @property
    def first_blood(self) -> bool:
        return self._dto["firstBlood"]

    @property
    def bans(self) -> List["ChampionData"]:
        from .staticdata.champion import ChampionData
        return [ChampionData(id=ban["championId"]) for ban in self._dto["bans"]]

    @property
    def baron_kills(self) -> int:
        return self._dto["baronKills"]

    @property
    def rift_herald_kills(self) -> int:
        return self._dto["riftHeraldKills"]

    @property
    def vilemaw_kills(self) -> int:
        return self._dto["vilemawKills"]

    @property
    def inhibitor_kills(self) -> int:
        return self._dto["inhibitorKills"]

    @property
    def tower_kills(self) -> int:
        return self._dto["towerKills"]

    @property
    def dragon_kills(self) -> int:
        return self._dto["dragonKills"]

    @property
    def side(self) -> int:
        return self._dto["teamId"]

    @property
    def dominion_victory_score(self) -> int:
        return self._dto["dominionVictoryScore"]

    @property
    def win(self) -> bool:
        return self._dto["win"]


class MatchReferenceData(DataObject):
    _renamed = {"season_id": "season", "queue_id": "queue", "id": "gameId", "platform_id": "platformId", "champion_id": "champion", "creation": "timestamp"}

    @property
    def id(self) -> int:
        return self._dto["gameId"]

    @property
    def season_id(self) -> int:
        return self._dto["season"]

    @property
    def queue_id(self) -> int:
        return self._dto["queue"]

    @property
    def platform_id(self) -> int:
        return self._dto["platformId"]

    @property
    def lane(self) -> str:
        return self._dto["lane"]

    @property
    def role(self) -> str:
        return self._dto["role"]

    @property
    def champion_id(self) -> int:
        return self._dto["champion"]

    @property
    def creation(self) -> int:
        return self._dto["timestamp"]


class MatchData(DataObject):
    _dto_type = dto.MatchDto
    _renamed = {"season_id": "seasonId", "queue_id": "queueId", "id": "gameId", "participant_identities": "participantIdentities", "version": "gameVersion", "platform_id": "platformId", "mode": "gameMode", "map_id": "mapId", "type": "gameType", "duration": "gameDuration", "creation": "gameCreation"}

    @lazy_property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def id(self) -> int:
        return self._dto["gameId"]

    @property
    def season_id(self) -> int:
        return self._dto["seasonId"]

    @property
    def queue_id(self) -> int:
        return self._dto["queueId"]

    @property
    def participants(self) -> List[ParticipantData]:
        return [ParticipantData(p) for p in self._dto["participants"]]

    @property
    def participant_identities(self) -> List[ParticipantIdentityData]:
        return [ParticipantIdentityData(p) for p in self._dto["participantIdentities"]]

    @property
    def teams(self) -> List[TeamData]:
        return [TeamData(t) for t in self._dto["teams"]]

    @property
    def version(self) -> str:
        return self._dto["gameVersion"]

    @property
    def platform_id(self) -> int:
        return self._dto["platformId"]

    @property
    def mode(self) -> str:
        return self._dto["gameMode"]

    @property
    def map_id(self) -> int:
        return self._dto["mapId"]

    @property
    def type(self) -> str:
        return self._dto["gameType"]

    @property
    def duration(self) -> int:
        return self._dto["gameDuration"]

    @property
    def creation(self) -> int:
        return self._dto["gameCreation"]


##############
# Core Types #
##############


class ParticipantTimeline(CassiopeiaObject):  # TODO
    _data_types = {ParticipantTimelineData}


class ParticipantStats(CassiopeiaObject):  # TODO
    _data_types = {ParticipantStatsData}


class ProfileIcon(CassiopeiaObject):
    _data_types = {ProfileIconData}

    @property
    def id(self) -> int:
        return self._data[ProfileIconData].id

    @property
    def name(self) -> str:
        global _profile_icon_names
        if _profile_icon_names is None:
            module_directory = os.path.dirname(os.path.realpath(__file__))
            module_directory, _ = os.path.split(module_directory)  # Go up one directory
            filename = os.path.join(module_directory, 'profile_icon_names.json')
            _profile_icon_names = json.load(open(filename))
            _profile_icon_names = {int(key): value for key, value in _profile_icon_names.items()}
        try:
            return _profile_icon_names[self._data[ProfileIconData].id]
        except KeyError:
            return None

    @property
    def url(self) -> str:
        versions = settings.pipeline.get(VersionListData, query={"platform": settings.default_platform})
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{id}.png".format(version=versions[0], id=self.id)

    @property
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})


class Participant(CassiopeiaObject):
    _data_types = {ParticipantData}

    @lazy_property
    def stats(self) -> ParticipantStats:
        return ParticipantStats(self._data[ParticipantData].stats)

    @property
    def id(self) -> int:
        return self._data[ParticipantData].id

    @lazy_property
    def runes(self) -> List["Rune"]:
        return self._data[ParticipantData].runes

    @lazy_property
    def masteries(self) -> List["Mastery"]:
        return self._data[ParticipantData].masteries

    @lazy_property
    def timeline(self) -> ParticipantTimeline:
        return ParticipantTimeline(self._data[ParticipantData].timeline)

    @lazy_property
    def team(self) -> "Team":
        return Team(self._data[ParticipantData].team)

    @lazy_property
    def summoner_spell_d(self) -> "SummonerSpell":
        return SummonerSpell(self._data[ParticipantData].summoner_spell_d)

    @lazy_property
    def summoner_spell_f(self) -> "SummonerSpell":
        return SummonerSpell(self._data[ParticipantData].summoner_spell_f)

    @lazy_property
    def rank_last_season(self) -> Tuple[Tier, Division]:
        return Tier(self._data[ParticipantData].rank_last_season[0]), Division(self._data[ParticipantData].rank_last_season[1])

    @lazy_property
    def champion(self) -> "Champion":
        from .staticdata.champion import Champion
        return Champion(id=self._data[ParticipantData].champion_id)


class Player(CassiopeiaObject):
    _data_types = {PlayerData}

    # TODO Can we rename current_platform and platform to have intuitive names. Same with accounts
    @property
    def current_platform(self) -> Platform:
        return Platform(self._data[PlayerData].current_platform_id)

    @property
    def platform(self) -> Platform:
        return Platform(self._data[PlayerData].platform_id)

    @property
    def summoner(self) -> "Summoner":
        return Summoner(id=self._data[PlayerData].summoner_id, name=self._data[PlayerData].summoner_name)

    @property
    def match_history_uri(self) -> str:
        return self._dto["matchHistoryUri"]

    @property
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(self._data[PlayerData].profile_icon)

    @property
    def current_account(self) -> "Account":
        return Account(self._data[PlayerData].current_account_id)

    @property
    def account(self) -> "Account":
        return Account(self._data[PlayerData].account_id)


class ParticipantIdentity(CassiopeiaObject):
    _data_types = {ParticipantIdentityData}

    @property
    def player(self) -> PlayerData:
        return Player(self._data[ParticipantIdentityData].player)

    @property
    def id(self) -> int:
        return self._data[ParticipantIdentityData].id


class Team(CassiopeiaObject):
    _data_types = {TeamData}

    @property
    def first_dragon(self) -> bool:
        return self._data[TeamData].firstDragon

    @property
    def first_inhibitor(self) -> bool:
        return self._data[TeamData].firstInhibitor

    @property
    def first_rift_herald(self) -> bool:
        return self._data[TeamData].firstRiftHerald

    @property
    def first_baron(self) -> bool:
        return self._data[TeamData].firstBaron

    @property
    def first_tower(self) -> bool:
        return self._data[TeamData].firstTower

    @property
    def first_blood(self) -> bool:
        return self._data[TeamData].firstBlood

    @property
    def bans(self) -> List["Champion"]:
        return [Champion(champion) for champion in self._data[TeamData].bans]

    @property
    def baron_kills(self) -> int:
        return self._data[TeamData].baronKills

    @property
    def rift_herald_kills(self) -> int:
        return self._data[TeamData].riftHeraldKills

    @property
    def vilemaw_kills(self) -> int:
        return self._data[TeamData].vilemawKills

    @property
    def inhibitor_kills(self) -> int:
        return self._data[TeamData].inhibitorKills

    @property
    def tower_kills(self) -> int:
        return self._data[TeamData].towerKills

    @property
    def dragon_kills(self) -> int:
        return self._data[TeamData].dragonKills

    @property
    def side(self) -> Side:
        return Side(self._data[TeamData].teamId)

    @property
    def dominion_victory_score(self) -> int:
        return self._data[TeamData].dominionVictoryScore

    @property
    def win(self) -> bool:
        return self._data[TeamData].win


@searchable({})
class Match(CassiopeiaGhost):
    _data_types = {MatchData}
    _retyped = {
      "region": {
        Region: ("value", "region")
      },
      "platform": {
        Platform: ("value", "platform")
      },
      "season": {
        Season: ("value", "season")
      },
      "queue": {
        Queue: ("value", "queue")
      },
      "mode": {
        GameMode: ("value", "mode")
      },
      "map": {
        Map: ("value", "map")
      },
      "type": {
        GameType: ("value", "type")
      }
    }
    # TODO We may need _retyped to accept methods so that it can convert duration and creation.

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @classmethod
    def from_match_reference(cls, ref):
        # TODO Somehow put in ref.lane, ref.role, and ref.champion_id
        instance = cls(id=ref.id, season_id=ref.season_id, queue_id=ref.queue_id, platform_id=ref.platform_id, creation=ref.creation)
        return instance

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[SummonerData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def id(self) -> int:
        return self._data[MatchData].id

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def season(self) -> Season:
        return Season(self._data[MatchData].season_id)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def queue(self) -> Queue:
        return Queue(self._data[MatchData].queue_id)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def participants(self) -> List[Participant]:
        return [Participant(p) for p in self._data[MatchData].participants]

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def participant_identities(self) -> List[ParticipantIdentity]:
        return [ParticipantIdentity(p) for p in self._data[MatchData].participant_identities]

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def teams(self) -> List[Team]:
        return [Team(t) for t in self._data[MatchData].teams]

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    def version(self) -> str:
        return self._data[MatchData].version

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def platform(self) -> Platform:
        return Platform(self._data[MatchData].platform_id)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def mode(self) -> GameMode:
        return GameMode(self._data[MatchData].mode)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def map(self) -> Map:
        return Map(self._data[MatchData].map_id)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def type(self) -> GameType:
        return GameType(self._data[MatchData].type)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def duration(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._data[MatchData].duration / 1000)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def creation(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._data[MatchData].creation / 1000)