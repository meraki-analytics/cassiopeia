from .common import CoreData, DataObjectList
from ..dto import championgg as dto


class GGChampionListData(DataObjectList):
    _dto_type = dto.GGChampionListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class GGChampionData(CoreData):
    _dto_type = dto.GGChampionDto
    _renamed = {"win_rate": "winRate", "id": "championId", "play_rate": "playRate", "games_played": "gamesPlayed", "percent_role_played": "percentRolePlayed", "ban_rate": "banRate", "damage_composition": "damageComposition", "total_damage_taken": "totalDamageTaken", "wards_killed": "wardsKilled", "neutralMinionsKilledTeamJungle": "neutralMinionsKilledTeamJungle", "performance_score": "overallPerformanceScore", "neutralMinionsKilledEnemyJungle": "neutralMinionsKilledEnemyJungle", "gold_earned": "goldEarned", "wards_placed": "wardPlaced", "minions_killed": "minionsKilled", "total_healed": "totalHeal"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def id(self) -> str:
        return self._dto["championId"]

    @property
    def win_rate(self) -> str:
        return self._dto["winRate"]

    @property
    def play_rate(self) -> str:
        return self._dto["playRate"]

    @property
    def play_rate_by_role(self) -> str:
        return self._dto["percentRolePlayed"]

    @property
    def ban_rate(self) -> str:
        return self._dto["banRate"]

    @property
    def games_played(self) -> str:
        return self._dto["gamesPlayed"]

    @property
    def damage_composition(self) -> str:
        return self._dto["damageComposition"]

    @property
    def kills(self) -> str:
        return self._dto["kills"]

    @property
    def total_damage_taken(self) -> str:
        return self._dto["totalDamageTaken"]

    @property
    def wards_killed(self) -> str:
        return self._dto["wardsKilled"]

    @property
    def neutral_minions_killed_in_team_jungle(self) -> str:
        return self._dto["neutralMinionsKilledTeamJungle"]

    @property
    def assists(self) -> str:
        return self._dto["assists"]

    @property
    def performance_score(self) -> str:
        return self._dto["overallPerformanceScore"]

    @property
    def neutral_minions_killed_in_enemy_jungle(self) -> str:
        return self._dto["neutralMinionsKilledEnemyJungle"]

    @property
    def gold_earned(self) -> str:
        return self._dto["goldEarned"]

    @property
    def deaths(self) -> str:
        return self._dto["deaths"]

    @property
    def minions_killed(self) -> str:
        return self._dto["minionsKilled"]

    @property
    def total_healed(self) -> str:
        return self._dto["totalHeal"]

    @property
    def elo(self) -> str:
        return self._dto["elo"].split(",")

    @property
    def patch(self) -> str:
        return self._dto["patch"]


# No non-CoreData core type is needed
