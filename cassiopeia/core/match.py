import os
import datetime
from typing import List, Tuple, Dict
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableLazyList

from ..configuration import settings
from ..data import Region, Platform, Tier, Map, GameType, GameMode, Queue, Division, Side, Season
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto import match as dto
from .staticdata.version import VersionListData
from .summoner import Summoner
from .staticdata.champion import Champion
from .staticdata.rune import Rune
from .staticdata.mastery import Mastery
from .staticdata.summonerspell import SummonerSpell, SummonerSpellData


# TODO Implement timelines


##############
# Data Types #
##############


class MatchListData(list):
    pass


class ParticipantTimelineData(DataObject):
    _renamed = {"id": "participantId", "cs_diff_per_min_deltas": "csDiffPerMinDeltas", "gold_per_min_deltas": "goldPerMinDeltas", "xp_pdiff_per_min_deltas": "xpDiffPerMinDeltas", "creeps_per_min_deltas": "creepsPerMinDeltas", "damage_taken_diff_per_min_deltas": "damageTakenDiffPerMinDeltas", "damage_taken_per_min_deltas": "damageTakenPerMinDeltas"}

    @property
    def lane(self) -> str:
        return ParticipantStatsData(self._dto["lane"])

    @property
    def role(self) -> str:
        return ParticipantStatsData(self._dto["role"])

    @property
    def id(self) -> int:
        return ParticipantStatsData(self._dto["participantId"])

    @property
    def cs_diff_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["csDiffPerMinDeltas"])

    @property
    def gold_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["goldPerMinDeltas"])

    @property
    def xp_diff_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["xpDiffPerMinDeltas"])

    @property
    def creeps_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["creepsPerMinDeltas"])

    @property
    def xp_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["xpPerMinDeltas"])

    @property
    def damage_taken_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["damageTakenPerMinDeltas"])

    @property
    def damage_taken_diff_per_min_deltas(self) -> Dict[str, float]:
        return ParticipantStatsData(self._dto["damageTakenDiffPerMinDeltas"])


class ParticipantStatsData(DataObject):
    _renamed = {"physical_damage_dealt": "physicalDamageDealt", "magic_damage_dealt": "magicDamageDealt", "neutral_minions_killed_team_jungle": "neutralMinionsKilledTeamJungle", "total_player_score": "totalPlayerScore", "neutral_minions_killed_enemy_jungle": "neutralMinionsKilledEnemyJungle", "altars_captured": "altarsCaptured", "largest_critical_strike": "largestCriticalStrike", "total_damage_dealt": "totalDamageDealt", "magic_damage_dealt_to_champions": "magicDamageDealtToChampions", "vision_wards_bought_in_game": "visionWardsBoughtInGame", "damage_dealt_to_objectives": "damageDealtToObjectives", "largest_killing_spree": "largestKillingSpree", "quadra_kills": "quadraKills", "team_objective": "teamObjective", "total_time_crowd_control_dealt": "totalTimeCrowdControlDealt", "longest_time_spent_living": "longestTimeSpentLiving", "wards_killed": "wardsKilled", "first_tower_assist": "firstTowerAssist", "first_tower_kill": "firstTowerKill", "first_blood_assist": "firstBloodAssist", "vision_score": "visionScore", "wards_placed": "wardsPlaced", "turret_kills": "turretKills", "triple_kills": "tripleKills", "damage_self_mitigated": "damageSelfMitigated", "champion_level": "champLevel", "node_neutralize_assist": "nodeNeutralizeAssist", "first_inhibitor_kill": "firstInhibitorKill", "gold_earned": "goldEarned", "magical_damage_taken": "magicalDamageTaken", "double_kills": "doubleKills", "node_capture_assist": "nodeCaptureAssist", "true_damage_taken": "trueDamageTaken", "node_neutralize": "nodeNeutralize", "first_inhibitor_assist": "firstInhibitorAssist", "unreal_kills": "unrealKills", "neutral_minions_killed": "neutralMinionsKilled", "objective_player_score": "objectivePlayerScore", "combat_player_score": "combatPlayerScore", "damage_dealt_to_turrets": "damageDealtToTurrets", "altars_neutralized": "altarsNeutralized", "physical_damage_dealt_to_champions": "physicalDamageDealtToChampions", "gold_spent": "goldSpent", "true_damage_dealt": "trueDamageDealt", "true_damage_dealt_to_champions": "trueDamageDealtToChampions", "id": "participantId", "penta_kills": "pentaKills", "total_heal": "totalHeal", "total_minions_killed": "totalMinionsKilled", "first_blood_kill": "firstBloodKill", "node_capture": "nodeCapture", "largest_multi_kill": "largestMultiKill", "sight_wards_bought_in_game": "sightWardsBoughtInGame", "total_damage_dealt_to_champions": "totalDamageDealtToChampions", "total_units_healed": "totalUnitsHealed", "inhibitor_kills": "inhibitorKills", "total_score_rank": "totalScoreRank", "total_damage_taken": "totalDamageTaken", "killing_sprees": "killingSprees", "time_CCing_others": "timeCCingOthers", "physical_damage_taken": "physicalDamageTaken"}

    @property
    def physical_damage_dealt(self) -> int:
        return self._dto["physicalDamageDealt"]

    @property
    def magic_damage_dealt(self) -> int:
        return self._dto["magicDamageDealt"]

    @property
    def neutral_minions_killed_team_jungle(self) -> int:
        return self._dto["neutralMinionsKilledTeamJungle"]

    @property
    def total_player_score(self) -> int:
        return self._dto["totalPlayerScore"]

    @property
    def deaths(self) -> int:
        return self._dto["deaths"]

    @property
    def win(self) -> bool:
        return self._dto["win"]

    @property
    def neutral_minions_killed_enemy_jungle(self) -> int:
        return self._dto["neutralMinionsKilledEnemyJungle"]

    @property
    def altars_captured(self) -> int:
        return self._dto["altarsCaptured"]

    @property
    def largest_critical_strike(self) -> int:
        return self._dto["largestCriticalStrike"]

    @property
    def total_damage_dealt(self) -> int:
        return self._dto["totalDamageDealt"]

    @property
    def magic_damage_dealt_to_champions(self) -> int:
        return self._dto["magicDamageDealtToChampions"]

    @property
    def vision_wards_bought_in_game(self) -> int:
        return self._dto["visionWardsBoughtInGame"]

    @property
    def damage_dealt_to_objectives(self) -> int:
        return self._dto["damageDealtToObjectives"]

    @property
    def largest_killing_spree(self) -> int:
        return self._dto["largestKillingSpree"]

    @property
    def item1(self) -> int:
        return self._dto["item1"]

    @property
    def quadra_kills(self) -> int:
        return self._dto["quadraKills"]

    @property
    def team_objective(self) -> int:
        return self._dto["teamObjective"]

    @property
    def total_time_crowd_control_dealt(self) -> int:
        return self._dto["totalTimeCrowdControlDealt"]

    @property
    def longestTimeSpentLiving(self) -> int:
        return self._dto["longest_time_spent_living"]

    @property
    def wards_killed(self) -> int:
        return self._dto["wardsKilled"]

    @property
    def first_tower_assist(self) -> bool:
        return self._dto["firstTowerAssist"]

    @property
    def first_tower_kill(self) -> bool:
        return self._dto["firstTowerKill"]

    @property
    def item2(self) -> int:
        return self._dto["item2"]

    @property
    def item3(self) -> int:
        return self._dto["item3"]

    @property
    def item0(self) -> int:
        return self._dto["item0"]

    @property
    def first_blood_assist(self) -> bool:
        return self._dto["firstBloodAssist"]

    @property
    def visionScore(self) -> int:
        return self._dto["vision_score"]

    @property
    def wards_placed(self) -> int:
        return self._dto["wardsPlaced"]

    @property
    def item4(self) -> int:
        return self._dto["item4"]

    @property
    def item5(self) -> int:
        return self._dto["item5"]

    @property
    def item6(self) -> int:
        return self._dto["item6"]

    @property
    def turret_kills(self) -> int:
        return self._dto["turretKills"]

    @property
    def triple_kills(self) -> int:
        return self._dto["tripleKills"]

    @property
    def damage_self_mitigated(self) -> int:
        return self._dto["damageSelfMitigated"]

    @property
    def champion_level(self) -> int:
        return self._dto["champLevel"]

    @property
    def node_neutralize_assist(self) -> int:
        return self._dto["nodeNeutralizeAssist"]

    @property
    def first_inhibitor_kill(self) -> bool:
        return self._dto["firstInhibitorKill"]

    @property
    def gold_earned(self) -> int:
        return self._dto["goldEarned"]

    @property
    def magical_damage_taken(self) -> int:
        return self._dto["magicalDamageTaken"]

    @property
    def kills(self) -> int:
        return self._dto["kills"]

    @property
    def double_kills(self) -> int:
        return self._dto["doubleKills"]

    @property
    def node_capture_assist(self) -> int:
        return self._dto["nodeCaptureAssist"]

    @property
    def true_damage_taken(self) -> int:
        return self._dto["trueDamageTaken"]

    @property
    def node_neutralize(self) -> int:
        return self._dto["nodeNeutralize"]

    @property
    def first_inhibitor_assist(self) -> bool:
        return self._dto["firstInhibitorAssist"]

    @property
    def assists(self) -> int:
        return self._dto["assists"]

    @property
    def unreal_kills(self) -> int:
        return self._dto["unrealKills"]

    @property
    def neutral_minions_killed(self) -> int:
        return self._dto["neutralMinionsKilled"]

    @property
    def objective_player_score(self) -> int:
        return self._dto["objectivePlayerScore"]

    @property
    def combat_player_score(self) -> int:
        return self._dto["combatPlayerScore"]

    @property
    def damage_dealt_to_turrets(self) -> int:
        return self._dto["damageDealtToTurrets"]

    @property
    def altars_neutralized(self) -> int:
        return self._dto["altarsNeutralized"]

    @property
    def physicalDamageDealtToChampions(self) -> int:
        return self._dto["physical_damage_dealt_to_champions"]

    @property
    def gold_spent(self) -> int:
        return self._dto["goldSpent"]

    @property
    def true_damage_dealt(self) -> int:
        return self._dto["trueDamageDealt"]

    @property
    def true_damage_dealt_to_champions(self) -> int:
        return self._dto["trueDamageDealtToChampions"]

    @property
    def id(self) -> int:
        return self._dto["participantId"]

    @property
    def penta_kills(self) -> int:
        return self._dto["pentaKills"]

    @property
    def total_heal(self) -> int:
        return self._dto["totalHeal"]

    @property
    def total_minions_killed(self) -> int:
        return self._dto["totalMinionsKilled"]

    @property
    def first_blood_kill(self) -> bool:
        return self._dto["firstBloodKill"]

    @property
    def node_capture(self) -> int:
        return self._dto["nodeCapture"]

    @property
    def largest_multi_kill(self) -> int:
        return self._dto["largestMultKill"]

    @property
    def sight_wards_bought_in_game(self) -> int:
        return self._dto["sightWardsBoughtInGame"]

    @property
    def total_damage_dealt_to_champions(self) -> int:
        return self._dto["totalDamageDealtToChampions"]

    @property
    def total_units_healed(self) -> int:
        return self._dto["totalUnitsHealed"]

    @property
    def inhibitor_kills(self) -> int:
        return self._dto["inhibitorKills"]

    @property
    def total_score_rank(self) -> int:
        return self._dto["totalScoreRank"]

    @property
    def total_damage_taken(self) -> int:
        return self._dto["totalDamageTaken"]

    @property
    def killing_sprees(self) -> int:
        return self._dto["killingSprees"]

    @property
    def time_CCing_others(self) -> int:
        return self._dto["timeCCingOthers"]

    @property
    def physical_damage_taken(self) -> int:
        return self._dto["physicalDamageTaken"]


class ParticipantData(DataObject):
    _renamed = {"id": "participantId", "side": "teamId", "summoner_spell_d": "spell1Id", "summoner_spell_f": "spell2Id", "champion_id": "championId", "rank_last_season":"highestAchievedSeasonTier"}

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
    def side(self) -> int:
        return self._dto["teamId"]

    @property
    def summoner_spell_d(self) -> SummonerSpellData:
        return SummonerSpellData({"id": self._dto["spell1Id"]})

    @property
    def summoner_spell_f(self) -> SummonerSpellData:
        return SummonerSpellData({"id": self._dto["spell2Id"]})

    @property
    def rank_last_season(self) -> Tuple[str, int]:
        return self._dto["highestAchievedSeasonTier"]

    @property
    def champion_id(self) -> int:
        return self._dto["championId"]


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
    def profile_icon(self) -> "ProfileIconData":
        from .summoner import ProfileIconData
        return ProfileIconData({"id": self._dto["profileIcon"]})

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
        return [ChampionData({"id": ban["championId"]}) for ban in self._dto["bans"]]

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


class ParticipantTimeline(CassiopeiaObject):
    _data_types = {ParticipantTimelineData}

    @property
    def lane(self) -> str:
        return self._data[ParticipantTimelineData].lane

    @property
    def role(self) -> str:
        return self._data[ParticipantTimelineData].role

    @property
    def id(self) -> int:
        return self._data[ParticipantTimelineData].id

    @property
    def cs_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].cs_diff_per_min_deltas

    @property
    def gold_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].gold_per_min_deltas

    @property
    def xp_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xp_diff_per_min_deltas

    @property
    def creeps_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].creeps_per_min_deltas

    @property
    def xp_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xp_per_min_deltas

    @property
    def damage_taken_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damage_taken_per_min_deltas

    @property
    def damage_taken_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damage_taken_diff_per_min_deltas


class ParticipantStats(CassiopeiaObject):
    _data_types = {ParticipantStatsData}

    @property
    def physical_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].physical_damage_dealt

    @property
    def magic_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].magic_damage_dealt

    @property
    def neutral_minions_killed_team_jungle(self) -> int:
        return self._data[ParticipantStatsData].neutral_minions_killed_team_jungle

    @property
    def total_player_score(self) -> int:
        return self._data[ParticipantStatsData].total_player_score

    @property
    def deaths(self) -> int:
        return self._data[ParticipantStatsData].deaths

    @property
    def win(self) -> bool:
        return self._data[ParticipantStatsData].win

    @property
    def neutral_minions_killed_enemy_jungle(self) -> int:
        return self._data[ParticipantStatsData].neutral_minions_killed_enemy_jungle

    @property
    def altars_captured(self) -> int:
        return self._data[ParticipantStatsData].altars_captured

    @property
    def largest_critical_strike(self) -> int:
        return self._data[ParticipantStatsData].largest_critical_strike

    @property
    def total_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].total_damage_dealt

    @property
    def magic_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].magic_damage_dealt_to_champions

    @property
    def vision_wards_bought_in_game(self) -> int:
        return self._data[ParticipantStatsData].vision_wards_bought_in_game

    @property
    def damage_dealt_to_objectives(self) -> int:
        return self._data[ParticipantStatsData].damage_dealt_to_objectives

    @property
    def largest_killing_spree(self) -> int:
        return self._data[ParticipantStatsData].largest_killing_spree

    @property
    def item1(self) -> int:
        return self._data[ParticipantStatsData].item1

    @property
    def quadra_kills(self) -> int:
        return self._data[ParticipantStatsData].quadra_kills

    @property
    def team_objective(self) -> int:
        return self._data[ParticipantStatsData].team_objective

    @property
    def total_time_crowd_control_dealt(self) -> int:
        return self._data[ParticipantStatsData].total_time_crowd_control_dealt

    @property
    def longest_time_spent_living(self) -> int:
        return self._data[ParticipantStatsData].longest_time_spent_living

    @property
    def wards_killed(self) -> int:
        return self._data[ParticipantStatsData].wards_killed

    @property
    def first_tower_assist(self) -> bool:
        return self._data[ParticipantStatsData].first_tower_assist

    @property
    def first_tower_kill(self) -> bool:
        return self._data[ParticipantStatsData].first_tower_kill

    @property
    def item2(self) -> int:
        return self._data[ParticipantStatsData].item2

    @property
    def item3(self) -> int:
        return self._data[ParticipantStatsData].item3

    @property
    def item0(self) -> int:
        return self._data[ParticipantStatsData].item0

    @property
    def first_blood_assist(self) -> bool:
        return self._data[ParticipantStatsData].first_blood_assist

    @property
    def vision_score(self) -> int:
        return self._data[ParticipantStatsData].vision_score

    @property
    def wards_placed(self) -> int:
        return self._data[ParticipantStatsData].wards_placed

    @property
    def item4(self) -> int:
        return self._data[ParticipantStatsData].item4

    @property
    def item5(self) -> int:
        return self._data[ParticipantStatsData].item5

    @property
    def item6(self) -> int:
        return self._data[ParticipantStatsData].item6

    @property
    def turret_kills(self) -> int:
        return self._data[ParticipantStatsData].turret_kills

    @property
    def triple_kills(self) -> int:
        return self._data[ParticipantStatsData].triple_kills

    @property
    def damage_self_mitigated(self) -> int:
        return self._data[ParticipantStatsData].damage_self_mitigated

    @property
    def champion_level(self) -> int:
        return self._data[ParticipantStatsData].champion_level

    @property
    def node_neutralize_assist(self) -> int:
        return self._data[ParticipantStatsData].node_neutralize_assist

    @property
    def first_inhibitor_kill(self) -> bool:
        return self._data[ParticipantStatsData].first_inhibitor_kill

    @property
    def gold_earned(self) -> int:
        return self._data[ParticipantStatsData].gold_earned

    @property
    def magical_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].magical_damage_taken

    @property
    def kills(self) -> int:
        return self._data[ParticipantStatsData].kills

    @property
    def double_kills(self) -> int:
        return self._data[ParticipantStatsData].double_kills

    @property
    def node_capture_assist(self) -> int:
        return self._data[ParticipantStatsData].node_capture_assist

    @property
    def true_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].true_damage_taken

    @property
    def node_neutralize(self) -> int:
        return self._data[ParticipantStatsData].node_neutralize

    @property
    def first_inhibitor_assist(self) -> bool:
        return self._data[ParticipantStatsData].first_inhibitor_assist

    @property
    def assists(self) -> int:
        return self._data[ParticipantStatsData].assists

    @property
    def unreal_kills(self) -> int:
        return self._data[ParticipantStatsData].unreal_kills

    @property
    def neutral_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].neutral_minions_killed

    @property
    def objective_player_score(self) -> int:
        return self._data[ParticipantStatsData].objective_player_score

    @property
    def combat_player_score(self) -> int:
        return self._data[ParticipantStatsData].combat_player_score

    @property
    def damage_dealt_to_turrets(self) -> int:
        return self._data[ParticipantStatsData].damage_dealt_to_turrets

    @property
    def altars_neutralized(self) -> int:
        return self._data[ParticipantStatsData].altars_neutralized

    @property
    def physical_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].physical_damage_dealt_to_champions

    @property
    def gold_spent(self) -> int:
        return self._data[ParticipantStatsData].gold_spent

    @property
    def true_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].true_damage_dealt

    @property
    def true_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].true_damage_dealt_to_champions

    @property
    def id(self) -> int:
        return self._data[ParticipantStatsData].id

    @property
    def penta_kills(self) -> int:
        return self._data[ParticipantStatsData].penta_kills

    @property
    def total_heal(self) -> int:
        return self._data[ParticipantStatsData].total_heal

    @property
    def total_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].total_minions_killed

    @property
    def first_blood_kill(self) -> bool:
        return self._data[ParticipantStatsData].first_blood_kill

    @property
    def node_capture(self) -> int:
        return self._data[ParticipantStatsData].node_capture

    @property
    def largest_multi_kill(self) -> int:
        return self._data[ParticipantStatsData].largest_multi_kill

    @property
    def sight_wards_bought_in_game(self) -> int:
        return self._data[ParticipantStatsData].sight_wards_bought_in_game

    @property
    def total_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].total_damage_dealt_to_champions

    @property
    def total_units_healed(self) -> int:
        return self._data[ParticipantStatsData].total_units_healed

    @property
    def inhibitor_kills(self) -> int:
        return self._data[ParticipantStatsData].inhibitor_kills

    @property
    def total_score_rank(self) -> int:
        return self._data[ParticipantStatsData].total_score_rank

    @property
    def total_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].total_damage_taken

    @property
    def killing_sprees(self) -> int:
        return self._data[ParticipantStatsData].killing_sprees

    @property
    def time_CCing_others(self) -> int:
        return self._data[ParticipantStatsData].time_CCing_others

    @property
    def physical_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].physical_damage_taken


@searchable({str: ["summoner", "champion", "runes", "masteries", "side", "summoner_spell_d", "summoner_spell_f"], Summoner: ["summoner"], Champion: ["champion"], Side: ["side"], Rune: ["runes"], Mastery: ["masteries"], SummonerSpell: ["summoner_spell_d", "summoner_spell_f"]})
class Participant(CassiopeiaObject):
    _data_types = {ParticipantData, PlayerData}

    def __init__(self, data: DataObject = None, match: "Match" = None, **kwargs):
        self.__match = match
        super().__init__(data, **kwargs)

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
    def side(self) -> Side:
        try:
            return Side(self._data[ParticipantData].side)
        except KeyError:  # teamId
            # The match has only partially loaded this participant and it doesn't have all it's data, so load the full match
            self.__match.__load__(MatchData)
            self.__match._Ghost__set_loaded(MatchData)
            for participant in self.__match.participants:
                if participant.summoner.name == self.summoner.name:
                    self._data[ParticipantData] = participant._data[ParticipantData]
                    return Side(self._data[ParticipantData].side)

    @lazy_property
    def summoner_spell_d(self) -> SummonerSpell:
        return SummonerSpell(self._data[ParticipantData].summoner_spell_d)

    @lazy_property
    def summoner_spell_f(self) -> SummonerSpell:
        return SummonerSpell(self._data[ParticipantData].summoner_spell_f)

    @lazy_property
    def rank_last_season(self) -> Tuple[Tier, Division]:
        return Tier(self._data[ParticipantData].rank_last_season[0]), Division(self._data[ParticipantData].rank_last_season[1])

    @lazy_property
    def champion(self) -> "Champion":
        from .staticdata.champion import Champion
        return Champion(id=self._data[ParticipantData].champion_id)

    # All the Player data from ParticipantIdentities.player is contained in the Summoner class.
    # The non-current accountId and platformId should never be relevant/used, and can be deleted from our type system.
    #   See: https://discussion.developer.riotgames.com/questions/1713/is-there-any-scenario-where-accountid-should-be-us.html
    @lazy_property
    def summoner(self) -> "Summoner":
        data = {}
        try:
            data["id"] = self._data[PlayerData].summoner_id
        except KeyError:
            pass
        try:
            data["name"] = self._data[PlayerData].summoner_name
        except KeyError:
            pass
        from .summoner import Summoner, AccountData, ProfileIcon
        account = self._data[PlayerData].current_account_id
        data["account"] = account
        data["region"] = Platform(self._data[PlayerData].current_platform_id).region
        try:
            data["profile_icon"] = ProfileIcon(self._data[PlayerData].profile_icon)
        except KeyError:
            pass
        return Summoner(**data)

    @property
    def team(self) -> "Team":
        if self.side == Side.blue:
            return self.__match.blue_team
        else:
            return self.__match.red_team


@searchable({str: ["participants"], bool: ["win"]})
class Team(CassiopeiaObject):
    _data_types = {TeamData}

    def __init__(self, data: DataObject, participants: List[Participant], **kwargs):
        self.__participants = participants
        super().__init__(data, **kwargs)

    @property
    def first_dragon(self) -> bool:
        return self._data[TeamData].first_dragon

    @property
    def first_inhibitor(self) -> bool:
        return self._data[TeamData].first_inhibitor

    @property
    def first_rift_herald(self) -> bool:
        return self._data[TeamData].first_rift_herald

    @property
    def first_baron(self) -> bool:
        return self._data[TeamData].first_baron

    @property
    def first_tower(self) -> bool:
        return self._data[TeamData].first_tower

    @property
    def first_blood(self) -> bool:
        return self._data[TeamData].first_blood

    @property
    def bans(self) -> List["Champion"]:
        return [Champion(champion) for champion in self._data[TeamData].bans]

    @property
    def baron_kills(self) -> int:
        return self._data[TeamData].baron_kills

    @property
    def rift_herald_kills(self) -> int:
        return self._data[TeamData].rift_herald_kills

    @property
    def vilemaw_kills(self) -> int:
        return self._data[TeamData].vilemaw_kills

    @property
    def inhibitor_kills(self) -> int:
        return self._data[TeamData].inhibitor_kills

    @property
    def tower_kills(self) -> int:
        return self._data[TeamData].tower_kills

    @property
    def dragon_kills(self) -> int:
        return self._data[TeamData].dragon_kills

    @property
    def side(self) -> Side:
        return Side(self._data[TeamData].side)

    @property
    def dominion_victory_score(self) -> int:
        return self._data[TeamData].dominion_victory_score

    @property
    def win(self) -> bool:
        return self._data[TeamData].win != "Fail"

    @property
    def participants(self) -> List[Participant]:
        return self.__participants


@searchable({str: ["participants", "region", "platform", "season", "queue", "mode", "map", "type"], Region: ["region"], Platform: ["platform"], Season: ["season"], Queue: ["queue"], GameMode: ["mode"], Map: ["map"], GameType: ["type"]})
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
        self.__participants = []  # For lazy-loading the participants in a special way

    @classmethod
    def from_match_reference(cls, ref, **kwargs):
        # TODO Somehow put in ref.lane, ref.role, and ref.champion_id
        participant = {"participantId": 0, "championId": ref.champion_id}
        player = {"participantId": 0, "currentAccountId": kwargs["current_account_id"], "currentPlatformId": ref.platform_id}
        instance = cls(id=ref.id, season_id=ref.season_id, queue_id=ref.queue_id, platform_id=ref.platform_id, creation=ref.creation)
        instance._data[MatchData]._dto["participants"] = [participant]
        instance._data[MatchData]._dto["participantIdentities"] = [{"participantId": 0, "player": player}]
        return instance

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[MatchData].region)

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
    # This method is lazy-loaded in a special way because of its unique behavior
    def participants(self) -> List[Participant]:
        # This is a complicated function because we don't want to load the particpants if the only one the user cares about is the one loaded from a match ref

        def construct_participant(participant_data, participant_identities):
            """A helper function for creating a participant from participant, participant identity, and player data."""
            for pidentity in participant_identities:
                if pidentity.id == participant_data.id:
                    participant = Participant(data=ParticipantData({}), match=self)
                    participant._data[ParticipantData] = participant_data
                    participant._data[PlayerData] = pidentity.player
                    return participant

        def generate_participants(match):
            # If a participant was provided from a matchref, yield that first
            yielded_one = False
            if len(match._data[MatchData].participants) == 1:
                yielded_one = True
                try:
                    yield match.__participants[0]
                except IndexError:
                    p = match._data[MatchData].participants[0]
                    participant = construct_participant(p, match._data[MatchData].participant_identities)
                    match.__participants.append(participant)
                    yield participant

            # Create all the participants if any haven't been created yet.
            # Note that it's important to overwrite the one from the matchref if it was loaded because we have more data after we load the full match.
            if yielded_one or len(match.__participants) < len(match._data[MatchData].participants):
                if not match._Ghost__is_loaded(MatchData):
                    match.__load__(MatchData)
                    match._Ghost__set_loaded(MatchData)  # __load__ doesn't trigger __set_loaded. is this a "bug"?
                match.__participants = [None for _ in match._data[MatchData].participants]
                for i, p in enumerate(match._data[MatchData].participants):
                    participant = construct_participant(p, match._data[MatchData].participant_identities)
                    match.__participants[i] = participant

            # Yield the rest of the participants
            for participant in match.__participants[yielded_one:]:
                yield participant

        return SearchableLazyList(generate_participants(self))

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on(KeyError)
    @lazy
    def teams(self) -> List[Team]:
        return [Team(t, participants=[p for p in self.participants if p.side.value == self._data[MatchData].teams[i].side]) for i, t in enumerate(self._data[MatchData].teams)]

    @property
    def red_team(self) -> Team:
        if self.teams[0].side is Side.red:
            return self.teams[0]
        else:
            return self.teams[1]

    @property
    def blue_team(self) -> Team:
        if self.teams[0].side is Side.blue:
            return self.teams[0]
        else:
            return self.teams[1]

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
