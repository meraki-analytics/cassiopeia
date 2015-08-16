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
        """The AggregatedStats (contains pretty much every stat you probably want to access)"""
        return AggregatedStats(self.data.aggregatedStats) if self.data.aggregatedStats else None

    @property
    def losses(self):
        """How many loses this participant has"""
        return self.data.losses

    @cassiopeia.type.core.common.lazyproperty
    def modify_date(self):
        """The date when the stats were last updated (in epoch milliseconds)"""
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def type(self):
        """The identifier for what Queue this stat summary is for"""
        return cassiopeia.type.core.common.StatSummaryType(self.data.playerStatSummaryType) if self.data.playerStatSummaryType else None

    @property
    def wins(self):
        """How many wins this participant has"""
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class AggregatedStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.stats.AggregatedStats

    def __str__(self):
        return "Aggregated Stats"

    @property
    def kda(self):
        """The participant's kda"""
        return (self.data.totalChampionKills + self.data.totalAssists) / (self.data.totalDeathsPerSession if self.data.totalDeathsPerSession else 1)

    @property
    def average_assists(self):
        """Dominion only"""
        return self.data.averageAssists

    @property
    def average_kills(self):
        """Dominion only"""
        return self.data.averageChampionsKilled

    @property
    def average_combat_score(self):
        """Dominion only. The part of your score in Dominion that comes from combat-related activities"""
        return self.data.averageCombatPlayerScore

    @property
    def average_node_captures(self):
        """Dominion only"""
        return self.data.averageNodeCapture

    @property
    def average_node_capture_assists(self):
        """Dominion only"""
        return self.data.averageNodeCaptureAssist

    @property
    def average_node_neutralizations(self):
        """Dominion only"""
        return self.data.averageNodeNeutralize

    @property
    def average_node_neutralization_assists(self):
        return self.data.averageNodeNeutralizeAssist

    @property
    def average_deaths(self):
        """Dominion only"""
        return self.data.averageNumDeaths

    @property
    def average_objective_score(self):
        """Dominion only. The part of your score in Dominion that comes from object-based activities"""
        return self.data.averageObjectivePlayerScore

    @property
    def average_team_score(self):
        """Dominion only"""
        return self.data.averageTeamObjective

    @property
    def average_score(self):
        """Dominion only"""
        return self.data.averageTotalPlayerScore

    @property
    def bot_games(self):
        """The number of bot games the participant has played"""
        return self.data.botGamesPlayed

    @property
    def killing_sprees(self):
        """How many killing sprees the participant has had"""
        return self.data.killingSpree

    @property
    def max_assists(self):
        """Dominion only. The most assists the participant has ever had"""
        return self.data.maxAssists

    @property
    def max_kills(self):
        return self.data.maxChampionsKilled

    @property
    def max_combat_score(self):
        """Dominion only. The highest combat score the participant has ever had"""
        return self.data.maxCombatPlayerScore

    @property
    def max_crit(self):
        """The highest damage crit the participant has ever had"""
        return self.data.maxLargestCriticalStrike

    @property
    def max_killing_spree(self):
        """The largest killing spree the participant has ever had"""
        return self.data.maxLargestKillingSpree

    @property
    def max_node_captures(self):
        return self.data.maxNodeCapture

    @property
    def max_node_capture_assists(self):
        """Dominion only. The most node capture assists the participant has ever had"""
        return self.data.maxNodeCaptureAssist

    @property
    def max_node_neutralizations(self):
        """Dominion only. The most node neutralizations the participant has ever had"""
        return self.data.maxNodeNeutralize

    @property
    def maxNodeNeutralizeAssist(self):
        """Dominion only. The most node neutralization assists the participant has ever had"""
        return self.data.maxNodeNeutralizeAssist

    @property
    def max_deaths(self):
        """Only returned for ranked statistics. The most deaths the participant has ever had"""
        return self.data.maxNumDeaths

    @property
    def max_objective_score(self):
        """Dominion only. The highest object score the participant has ever had"""
        return self.data.maxObjectivePlayerScore

    @property
    def max_team_score(self):
        """Dominion only. The highest team score the participant has ever had"""
        return self.data.maxTeamObjective

    @property
    def max_game_time(self):
        """The longest a participant has ever been in a game"""
        return self.data.maxTimePlayed

    @property
    def max_time_alive(self):
        """The longest a participant has ever been alive"""
        return self.data.maxTimeSpentLiving

    @property
    def max_score(self):
        """Dominion only. The highest Dominion score the participant has ever obtained"""
        return self.data.maxTotalPlayerScore

    @property
    def max_kills_per_session(self):
        """Well, we don't know what this one is. Let us know if you figure it out."""
        return self.data.mostChampionKillsPerSession

    @property
    def max_spells_cast(self):
        """The most spell casts the participant has ever done in a game"""
        return self.data.mostSpellsCast

    @property
    def normal_games(self):
        return self.data.normalGamesPlayed

    @property
    def ranked_premade_games(self):
        """How many premade, ranked games the participant has played"""
        return self.data.rankedPremadeGamesPlayed

    @property
    def ranked_solo_games(self):
        """How many premade, solo games the participant has played"""
        return self.data.rankedSoloGamesPlayed

    @property
    def assists(self):
        """The total number of assists this participant has had"""
        return self.data.totalAssists

    @property
    def kills(self):
        """The total number of champion kills this participant has had"""
        return self.data.totalChampionKills

    @property
    def damage_dealt(self):
        """The total amount of damage this participant has dealt"""
        return self.data.totalDamageDealt

    @property
    def damage_taken(self):
        """The total amount of damage this participant has taken"""
        return self.data.totalDamageTaken

    @property
    def deaths(self):
        """The total number of deaths this participant has had"""
        return self.data.totalDeathsPerSession

    @property
    def double_kills(self):
        """The total number of double kills this participant has had"""
        return self.data.totalDoubleKills

    @property
    def first_bloods(self):
        """The total number of first bloods this participant has had"""
        return self.data.totalFirstBlood

    @property
    def gold_earned(self):
        """The total amount of gold earned this participant has had"""
        return self.data.totalGoldEarned

    @property
    def healing_done(self):
        """The total amount of healing this participant has done"""
        return self.data.totalHeal

    @property
    def magic_damage_dealt(self):
        """The total amount of magic damage this participant has dealt"""
        return self.data.totalMagicDamageDealt

    @property
    def minions_killed(self):
        """The total number of minion kills this participant has had"""
        return self.data.totalMinionKills

    @property
    def neutral_monster_killed(self):
        """The total number of neutral monster kills this participant has had"""
        return self.data.totalNeutralMinionsKilled

    @property
    def node_captures(self):
        """Dominion only. The total number of nodes this participant has captured"""
        return self.data.totalNodeCapture

    @property
    def node_neutralizations(self):
        """Dominion only. The total number of nodes this participant has neutralized"""
        return self.data.totalNodeNeutralize

    @property
    def penta_kills(self):
        """The total number of penta kills this participant has gotten"""
        return self.data.totalPentaKills

    @property
    def physical_damage_dealt(self):
        """The total amount of physical damage this participant has dealt"""
        return self.data.totalPhysicalDamageDealt

    @property
    def quadra_kills(self):
        """The total number of quadra kills this participant has gotten"""
        return self.data.totalQuadraKills

    @property
    def losses(self):
        """The total number of loses this participant has had"""
        return self.data.totalSessionsLost

    @property
    def games_played(self):
        """The total number of games this participant has played"""
        return self.data.totalSessionsPlayed

    @property
    def wins(self):
        """The total number of wins this participant has had"""
        return self.data.totalSessionsWon

    @property
    def triple_kills(self):
        """The total number of triple kills this participant has gotten"""
        return self.data.totalTripleKills

    @property
    def turrets_killed(self):
        """The total number of turrets this participant has killed"""
        return self.data.totalTurretsKilled

    @property
    def unreal_kills(self):
        """The total number of unreal kills this participant has gotten"""
        return self.data.totalUnrealKills

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    StatsSummary.dto_type = cassiopeia.type.dto.stats.PlayerStatsSummary
    AggregatedStats.dto_type = cassiopeia.type.dto.stats.AggregatedStats
