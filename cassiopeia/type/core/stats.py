import datetime

import cassiopeia.type.core.common
import cassiopeia.type.dto.stats


@cassiopeia.type.core.common.inheritdocs
class StatsSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.stats.PlayerStatsSummary

    def __str__(self):
        return "Stats Summary"

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return AggregatedStats(self.data.aggregatedStats) if self.data.aggregatedStats else None

    @property
    def losses(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.losses

    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def type(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return cassiopeia.type.core.common.StatSummaryType(self.data.playerStatSummaryType) if self.data.playerStatSummaryType else None

    @property
    def wins(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class AggregatedStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.stats.AggregatedStats

    def __str__(self):
        return "Aggregated Stats"

    @property
    def kda(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return (self.data.totalChampionKills + self.data.totalAssists) / (self.data.totalDeathsPerSession if self.data.totalDeathsPerSession else 1)

    @property
    def average_assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageAssists

    @property
    def average_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageChampionsKilled

    @property
    def average_combat_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageCombatPlayerScore

    @property
    def average_node_captures(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageNodeCapture

    @property
    def average_node_capture_assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageNodeCaptureAssist

    @property
    def average_node_neutralizations(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageNodeNeutralize

    @property
    def average_node_neutralization_assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageNodeNeutralizeAssist

    @property
    def average_deaths(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageNumDeaths

    @property
    def average_objective_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageObjectivePlayerScore

    @property
    def average_team_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageTeamObjective

    @property
    def average_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.averageTotalPlayerScore

    @property
    def bot_games(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.botGamesPlayed

    @property
    def killing_sprees(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.killingSpree

    @property
    def max_assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxAssists

    @property
    def max_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxChampionsKilled

    @property
    def max_combat_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxCombatPlayerScore

    @property
    def max_crit(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxLargestCriticalStrike

    @property
    def max_killing_spree(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxLargestKillingSpree

    @property
    def max_node_captures(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxNodeCapture

    @property
    def max_node_capture_assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxNodeCaptureAssist

    @property
    def max_node_neutralizations(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxNodeNeutralize

    @property
    def max_node_neutralize_assist(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxNodeNeutralizeAssist

    @property
    def max_deaths(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxNumDeaths

    @property
    def max_objective_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxObjectivePlayerScore

    @property
    def max_team_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxTeamObjective

    @property
    def max_game_time(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxTimePlayed

    @property
    def max_time_alive(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxTimeSpentLiving

    @property
    def max_score(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.maxTotalPlayerScore

    @property
    def max_kills_per_session(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.mostChampionKillsPerSession

    @property
    def max_spells_cast(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.mostSpellsCast

    @property
    def normal_games(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.normalGamesPlayed

    @property
    def ranked_premade_games(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.rankedPremadeGamesPlayed

    @property
    def ranked_solo_games(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.rankedSoloGamesPlayed

    @property
    def assists(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalAssists

    @property
    def kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalChampionKills

    @property
    def damage_dealt(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalDamageDealt

    @property
    def damage_taken(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalDamageTaken

    @property
    def deaths(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalDeathsPerSession

    @property
    def double_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalDoubleKills

    @property
    def first_bloods(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalFirstBlood

    @property
    def gold_earned(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalGoldEarned

    @property
    def healing_done(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalHeal

    @property
    def magic_damage_dealt(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalMagicDamageDealt

    @property
    def minions_killed(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalMinionKills

    @property
    def neutral_monster_killed(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalNeutralMinionsKilled

    @property
    def node_captures(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalNodeCapture

    @property
    def node_neutralizations(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalNodeNeutralize

    @property
    def penta_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalPentaKills

    @property
    def physical_damage_dealt(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalPhysicalDamageDealt

    @property
    def quadra_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalQuadraKills

    @property
    def losses(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalSessionsLost

    @property
    def games_played(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalSessionsPlayed

    @property
    def wins(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalSessionsWon

    @property
    def triple_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalTripleKills

    @property
    def turrets_killed(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalTurretsKilled

    @property
    def unreal_kills(self):
        """
        Returns:
            AggregatedStats: the aggregated stats (contains pretty much every stat you probably want to access)
        """
        return self.data.totalUnrealKills


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    StatsSummary.dto_type = cassiopeia.type.dto.stats.PlayerStatsSummary
    AggregatedStats.dto_type = cassiopeia.type.dto.stats.AggregatedStats
