import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.stats import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_player_stats_summary():
    global PlayerStatsSummary
    @cassiopeia.type.core.common.inheritdocs
    class PlayerStatsSummary(PlayerStatsSummary, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "PlayerStatsSummary"
        aggregatedStats = sqlalchemy.orm.relationship("cassiopeia.type.dto.stats.AggregatedStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        losses = sqlalchemy.Column(sqlalchemy.Integer)
        modifyDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        playerStatSummaryType = sqlalchemy.Column(sqlalchemy.String(30))
        wins = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

def _sa_bind_aggregated_stats():
    global AggregatedStats
    @cassiopeia.type.core.common.inheritdocs
    class AggregatedStats(AggregatedStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "AggregatedStats"
        averageAssists = sqlalchemy.Column(sqlalchemy.Integer)
        averageChampionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        averageCombatPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        averageNodeCapture = sqlalchemy.Column(sqlalchemy.Integer)
        averageNodeCaptureAssist = sqlalchemy.Column(sqlalchemy.Integer)
        averageNodeNeutralize = sqlalchemy.Column(sqlalchemy.Integer)
        averageNodeNeutralizeAssist = sqlalchemy.Column(sqlalchemy.Integer)
        averageNumDeaths = sqlalchemy.Column(sqlalchemy.Integer)
        averageObjectivePlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        averageTeamObjective = sqlalchemy.Column(sqlalchemy.Integer)
        averageTotalPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        botGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        killingSpree = sqlalchemy.Column(sqlalchemy.Integer)
        maxAssists = sqlalchemy.Column(sqlalchemy.Integer)
        maxChampionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        maxCombatPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        maxLargestCriticalStrike = sqlalchemy.Column(sqlalchemy.Integer)
        maxLargestKillingSpree = sqlalchemy.Column(sqlalchemy.Integer)
        maxNodeCapture = sqlalchemy.Column(sqlalchemy.Integer)
        maxNodeCaptureAssist = sqlalchemy.Column(sqlalchemy.Integer)
        maxNodeNeutralize = sqlalchemy.Column(sqlalchemy.Integer)
        maxNodeNeutralizeAssist = sqlalchemy.Column(sqlalchemy.Integer)
        maxNumDeaths = sqlalchemy.Column(sqlalchemy.Integer)
        maxObjectivePlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        maxTeamObjective = sqlalchemy.Column(sqlalchemy.Integer)
        maxTimePlayed = sqlalchemy.Column(sqlalchemy.Integer)
        maxTimeSpentLiving = sqlalchemy.Column(sqlalchemy.Integer)
        maxTotalPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        mostChampionKillsPerSession = sqlalchemy.Column(sqlalchemy.Integer)
        mostSpellsCast = sqlalchemy.Column(sqlalchemy.Integer)
        normalGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        rankedPremadeGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        rankedSoloGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        totalAssists = sqlalchemy.Column(sqlalchemy.Integer)
        totalChampionKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        totalDeathsPerSession = sqlalchemy.Column(sqlalchemy.Integer)
        totalDoubleKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalFirstBlood = sqlalchemy.Column(sqlalchemy.Integer)
        totalGoldEarned = sqlalchemy.Column(sqlalchemy.Integer)
        totalHeal = sqlalchemy.Column(sqlalchemy.Integer)
        totalMagicDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalMinionKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalNeutralMinionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        totalNodeCapture = sqlalchemy.Column(sqlalchemy.Integer)
        totalNodeNeutralize = sqlalchemy.Column(sqlalchemy.Integer)
        totalPentaKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalPhysicalDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalQuadraKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalSessionsLost = sqlalchemy.Column(sqlalchemy.Integer)
        totalSessionsPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        totalSessionsWon = sqlalchemy.Column(sqlalchemy.Integer)
        totalTripleKills = sqlalchemy.Column(sqlalchemy.Integer)
        totalTurretsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        totalUnrealKills = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _summary_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("PlayerStatsSummary._id", ondelete="CASCADE"))

def _sa_bind_all():
    _sa_bind_player_stats_summary()
    _sa_bind_aggregated_stats()