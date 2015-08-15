import datetime

import cassiopeia.type.core.common
import cassiopeia.type.dto.stats

class StatsSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.stats.PlayerStatsSummary

    def __str__(self):
        return "Stats Summary"

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        return AggregatedStats(self.data.aggregatedStats) if self.data.aggregatedStats else None

    @property
    def losses(self):
        return self.data.losses

    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def type(self):
        return cassiopeia.type.core.common.StatSummaryType(self.data.playerStatSummaryType) if self.data.playerStatSummaryType else None

    @property
    def wins(self):
        return self.data.wins


class AggregatedStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.stats.AggregatedStats

    def __str__(self):
        return "Aggregated Stats"

    @property
    def kda(self):
        return (self.data.totalChampionKills + self.data.totalAssists) / (self.data.totalDeathsPerSession if self.data.totalDeathsPerSession else 1)

    # int # Dominion only.
    @property
    def average_assists(self):
        return self.data.averageAssists

    # int # Dominion only.
    @property
    def average_kills(self):
        return self.data.averageChampionsKilled

    # int # Dominion only.
    @property
    def average_combat_score(self):
        return self.data.averageCombatPlayerScore

    # int # Dominion only.
    @property
    def average_node_captures(self):
        return self.data.averageNodeCapture

    # int # Dominion only.
    @property
    def average_node_capture_assists(self):
        return self.data.averageNodeCaptureAssist

    # int # Dominion only.
    @property
    def average_node_neutralizations(self):
        return self.data.averageNodeNeutralize

    # int # Dominion only.
    @property
    def average_node_neutralization_assists(self):
        return self.data.averageNodeNeutralizeAssist

    # int # Dominion only.
    @property
    def average_deaths(self):
        return self.data.averageNumDeaths

    # int # Dominion only.
    @property
    def average_objective_score(self):
        return self.data.averageObjectivePlayerScore

    # int # Dominion only.
    @property
    def average_team_score(self):
        return self.data.averageTeamObjective

    # int # Dominion only.
    @property
    def average_score(self):
        return self.data.averageTotalPlayerScore

    # int # botGamesPlayed
    @property
    def bot_games(self):
        return self.data.botGamesPlayed

    # int # killingSpree
    @property
    def killing_sprees(self):
        return self.data.killingSpree

    # int # Dominion only.
    @property
    def max_assists(self):
        return self.data.maxAssists

    # int # maxChampionsKilled
    @property
    def max_kills(self):
        return self.data.maxChampionsKilled

    # int # Dominion only.
    @property
    def max_combat_score(self):
        return self.data.maxCombatPlayerScore

    # int # maxLargestCriticalStrike
    @property
    def max_crit(self):
        return self.data.maxLargestCriticalStrike

    # int # maxLargestKillingSpree
    @property
    def max_killing_spree(self):
        return self.data.maxLargestKillingSpree

    # int # Dominion only.
    @property
    def max_node_captures(self):
        return self.data.maxNodeCapture

    # int # Dominion only.
    @property
    def max_node_capture_assists(self):
        return self.data.maxNodeCaptureAssist

    # int # Dominion only.
    @property
    def max_node_neutralizations(self):
        return self.data.maxNodeNeutralize

    # int # Dominion only.
    @property
    def maxNodeNeutralizeAssist(self):
        return self.data.maxNodeNeutralizeAssist

    # int # Only returned for ranked statistics.
    @property
    def max_deaths(self):
        return self.data.maxNumDeaths

    # int # Dominion only.
    @property
    def max_objective_score(self):
        return self.data.maxObjectivePlayerScore

    # int # Dominion only.
    @property
    def max_team_score(self):
        return self.data.maxTeamObjective

    # int # maxTimePlayed
    @property
    def max_game_time(self):
        return self.data.maxTimePlayed

    # int # maxTimeSpentLiving
    @property
    def max_time_alive(self):
        return self.data.maxTimeSpentLiving

    # int # Dominion only.
    @property
    def max_score(self):
        return self.data.maxTotalPlayerScore

    # int # mostChampionKillsPerSession
    @property
    def max_kills_per_session(self):
        return self.data.mostChampionKillsPerSession

    # int # mostSpellsCast
    @property
    def max_spells_cast(self):
        return self.data.mostSpellsCast

    # int # normalGamesPlayed
    @property
    def normal_games(self):
        return self.data.normalGamesPlayed

    # int # rankedPremadeGamesPlayed
    @property
    def ranked_premade_games(self):
        return self.data.rankedPremadeGamesPlayed

    # int # rankedSoloGamesPlayed
    @property
    def ranked_solo_games(self):
        return self.data.rankedSoloGamesPlayed

    # int # totalAssists
    @property
    def assists(self):
        return self.data.totalAssists

    # int # totalChampionKills
    @property
    def kills(self):
        return self.data.totalChampionKills

    # int # totalDamageDealt
    @property
    def damage_dealt(self):
        return self.data.totalDamageDealt

    # int # totalDamageTaken
    @property
    def damage_taken(self):
        return self.data.totalDamageTaken

    # int # Only returned for ranked statistics.
    @property
    def deaths(self):
        return self.data.totalDeathsPerSession

    # int # totalDoubleKills
    @property
    def double_kills(self):
        return self.data.totalDoubleKills

    # int # totalFirstBlood
    @property
    def first_bloods(self):
        return self.data.totalFirstBlood

    # int # totalGoldEarned
    @property
    def gold_earned(self):
        return self.data.totalGoldEarned

    # int # totalHeal
    @property
    def healing_done(self):
        return self.data.totalHeal

    # int # totalMagicDamageDealt
    @property
    def magic_damage_dealt(self):
        return self.data.totalMagicDamageDealt

    # int # totalMinionKills
    @property
    def minions_killed(self):
        return self.data.totalMinionKills

    # int # totalNeutralMinionsKilled
    @property
    def neutral_minions_killed(self):
        return self.data.totalNeutralMinionsKilled

    # int # Dominion only.
    @property
    def node_captures(self):
        return self.data.totalNodeCapture

    # int # Dominion only.
    @property
    def node_neutralizations(self):
        return self.data.totalNodeNeutralize

    # int # totalPentaKills
    @property
    def penta_kills(self):
        return self.data.totalPentaKills

    # int # totalPhysicalDamageDealt
    @property
    def physical_damage_dealt(self):
        return self.data.totalPhysicalDamageDealt

    # int # totalQuadraKills
    @property
    def quadra_kills(self):
        return self.data.totalQuadraKills

    # int # totalSessionsLost
    @property
    def losses(self):
        return self.data.totalSessionsLost

    # int # totalSessionsPlayed
    @property
    def games_played(self):
        return self.data.totalSessionsPlayed

    # int # totalSessionsWon
    @property
    def wins(self):
        return self.data.totalSessionsWon

    # int # totalTripleKills
    @property
    def triple_kills(self):
        return self.data.totalTripleKills

    # int # totalTurretsKilled
    @property
    def turrets_killed(self):
        return self.data.totalTurretsKilled

    # int # totalUnrealKills
    @property
    def unreal_kills(self):
        return self.data.totalUnrealKills

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    StatsSummary.dto_type = cassiopeia.type.dto.stats.PlayerStatsSummary
    AggregatedStats.dto_type = cassiopeia.type.dto.stats.AggregatedStats