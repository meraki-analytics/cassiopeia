import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class PlayerStatsSummaryList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        playerStatSummaries (list<PlayerStatsSummary>): collection of player stats summaries associated with the summoner
        summonerId (int): summoner ID
    """
    def __init__(self, dictionary):
        self.playerStatSummaries = [(PlayerStatsSummary(pss) if not isinstance(pss, PlayerStatsSummary) else pss) for pss in dictionary.get("playerStatSummaries", []) if pss]
        self.summonerId = dictionary.get("summonerId", 0)


@cassiopeia.type.core.common.inheritdocs
class PlayerStatsSummary(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        losses (int): number of losses for this queue type. Returned for ranked queue types only
        modifyDate (int): date stats were last modified specified as epoch milliseconds
        playerStatSummaryType (str): player stats summary type (Legal values: AramUnranked5x5, Ascension, CAP5x5, CoopVsAI, CoopVsAI3x3, CounterPick, FirstBlood1x1, FirstBlood2x2, Hexakill, KingPoro, NightmareBot, OdinUnranked, OneForAll5x5, RankedPremade3x3, RankedPremade5x5, RankedSolo5x5, RankedTeam3x3, RankedTeam5x5, SummonersRift6x6, Unranked, Unranked3x3, URF, URFBots)
        wins (int): number of wins for this queue type
    """
    def __init__(self, dictionary):
        val = dictionary.get("aggregatedStats", None)
        self.aggregatedStats = None if not val else AggregatedStats(val) if not isinstance(val, AggregatedStats) else val
        self.losses = dictionary.get("losses", 0)
        self.modifyDate = dictionary.get("modifyDate", 0)
        self.playerStatSummaryType = dictionary.get("playerStatSummaryType", "")
        self.wins = dictionary.get("wins", 0)


@cassiopeia.type.core.common.inheritdocs
class AggregatedStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        averageAssists (int): dominion only
        averageChampionsKilled (int): dominion only
        averageCombatPlayerScore (int): dominion only
        averageNodeCapture (int): dominion only
        averageNodeCaptureAssist (int): dominion only
        averageNodeNeutralize (int): dominion only
        averageNodeNeutralizeAssist (int): dominion only
        averageNumDeaths (int): dominion only
        averageObjectivePlayerScore (int): dominion only
        averageTeamObjective (int): dominion only
        averageTotalPlayerScore (int): dominion only
        botGamesPlayed (int): botGamesPlayed
        killingSpree (int): killingSpree
        maxAssists (int): dominion only
        maxChampionsKilled (int): maxChampionsKilled
        maxCombatPlayerScore (int): dominion only
        maxLargestCriticalStrike (int): maxLargestCriticalStrike
        maxLargestKillingSpree (int): maxLargestKillingSpree
        maxNodeCapture (int): dominion only
        maxNodeCaptureAssist (int): dominion only
        maxNodeNeutralize (int): dominion only
        maxNodeNeutralizeAssist (int): dominion only
        maxNumDeaths (int): only returned for ranked statistics.
        maxObjectivePlayerScore (int): dominion only
        maxTeamObjective (int): dominion only
        maxTimePlayed (int): maxTimePlayed
        maxTimeSpentLiving (int): maxTimeSpentLiving
        maxTotalPlayerScore (int): dominion only
        mostChampionKillsPerSession (int): mostChampionKillsPerSession
        mostSpellsCast (int): mostSpellsCast
        normalGamesPlayed (int): normalGamesPlayed
        rankedPremadeGamesPlayed (int): rankedPremadeGamesPlayed
        rankedSoloGamesPlayed (int): rankedSoloGamesPlayed
        totalAssists (int): totalAssists
        totalChampionKills (int): totalChampionKills
        totalDamageDealt (int): totalDamageDealt
        totalDamageTaken (int): totalDamageTaken
        totalDeathsPerSession (int): only returned for ranked statistics
        totalDoubleKills (int): totalDoubleKills
        totalFirstBlood (int): totalFirstBlood
        totalGoldEarned (int): totalGoldEarned
        totalHeal (int): totalHeal
        totalMagicDamageDealt (int): totalMagicDamageDealt
        totalMinionKills (int): totalMinionKills
        totalNeutralMinionsKilled (int): totalNeutralMinionsKilled
        totalNodeCapture (int): dominion only
        totalNodeNeutralize (int): dominion only
        totalPentaKills (int): totalPentaKills
        totalPhysicalDamageDealt (int): totalPhysicalDamageDealt
        totalQuadraKills (int): totalQuadraKills
        totalSessionsLost (int): totalSessionsLost
        totalSessionsPlayed (int): totalSessionsPlayed
        totalSessionsWon (int): totalSessionsWon
        totalTripleKills (int): totalTripleKills
        totalTurretsKilled (int): totalTurretsKilled
        totalUnrealKills (int): totalUnrealKills
    """
    def __init__(self, dictionary):
        self.averageAssists = dictionary.get("averageAssists", 0)
        self.averageChampionsKilled = dictionary.get("averageChampionsKilled", 0)
        self.averageCombatPlayerScore = dictionary.get("averageCombatPlayerScore", 0)
        self.averageNodeCapture = dictionary.get("averageNodeCapture", 0)
        self.averageNodeCaptureAssist = dictionary.get("averageNodeCaptureAssist", 0)
        self.averageNodeNeutralize = dictionary.get("averageNodeNeutralize", 0)
        self.averageNodeNeutralizeAssist = dictionary.get("averageNodeNeutralizeAssist", 0)
        self.averageNumDeaths = dictionary.get("averageNumDeaths", 0)
        self.averageObjectivePlayerScore = dictionary.get("averageObjectivePlayerScore", 0)
        self.averageTeamObjective = dictionary.get("averageTeamObjective", 0)
        self.averageTotalPlayerScore = dictionary.get("averageTotalPlayerScore", 0)
        self.botGamesPlayed = dictionary.get("botGamesPlayed", 0)
        self.killingSpree = dictionary.get("killingSpree", 0)
        self.maxAssists = dictionary.get("maxAssists", 0)
        self.maxChampionsKilled = dictionary.get("maxChampionsKilled", 0)
        self.maxCombatPlayerScore = dictionary.get("maxCombatPlayerScore", 0)
        self.maxLargestCriticalStrike = dictionary.get("maxLargestCriticalStrike", 0)
        self.maxLargestKillingSpree = dictionary.get("maxLargestKillingSpree", 0)
        self.maxNodeCapture = dictionary.get("maxNodeCapture", 0)
        self.maxNodeCaptureAssist = dictionary.get("maxNodeCaptureAssist", 0)
        self.maxNodeNeutralize = dictionary.get("maxNodeNeutralize", 0)
        self.maxNodeNeutralizeAssist = dictionary.get("maxNodeNeutralizeAssist", 0)
        self.maxNumDeaths = dictionary.get("maxNumDeaths", 0)
        self.maxObjectivePlayerScore = dictionary.get("maxObjectivePlayerScore", 0)
        self.maxTeamObjective = dictionary.get("maxTeamObjective", 0)
        self.maxTimePlayed = dictionary.get("maxTimePlayed", 0)
        self.maxTimeSpentLiving = dictionary.get("maxTimeSpentLiving", 0)
        self.maxTotalPlayerScore = dictionary.get("maxTotalPlayerScore", 0)
        self.mostChampionKillsPerSession = dictionary.get("mostChampionKillsPerSession", 0)
        self.mostSpellsCast = dictionary.get("mostSpellsCast", 0)
        self.normalGamesPlayed = dictionary.get("normalGamesPlayed", 0)
        self.rankedPremadeGamesPlayed = dictionary.get("rankedPremadeGamesPlayed", 0)
        self.rankedSoloGamesPlayed = dictionary.get("rankedSoloGamesPlayed", 0)
        self.totalAssists = dictionary.get("totalAssists", 0)
        self.totalChampionKills = dictionary.get("totalChampionKills", 0)
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)
        self.totalDeathsPerSession = dictionary.get("totalDeathsPerSession", 0)
        self.totalDoubleKills = dictionary.get("totalDoubleKills", 0)
        self.totalFirstBlood = dictionary.get("totalFirstBlood", 0)
        self.totalGoldEarned = dictionary.get("totalGoldEarned", 0)
        self.totalHeal = dictionary.get("totalHeal", 0)
        self.totalMagicDamageDealt = dictionary.get("totalMagicDamageDealt", 0)
        self.totalMinionKills = dictionary.get("totalMinionKills", 0)
        self.totalNeutralMinionsKilled = dictionary.get("totalNeutralMinionsKilled", 0)
        self.totalNodeCapture = dictionary.get("totalNodeCapture", 0)
        self.totalNodeNeutralize = dictionary.get("totalNodeNeutralize", 0)
        self.totalPentaKills = dictionary.get("totalPentaKills", 0)
        self.totalPhysicalDamageDealt = dictionary.get("totalPhysicalDamageDealt", 0)
        self.totalQuadraKills = dictionary.get("totalQuadraKills", 0)
        self.totalSessionsLost = dictionary.get("totalSessionsLost", 0)
        self.totalSessionsPlayed = dictionary.get("totalSessionsPlayed", 0)
        self.totalSessionsWon = dictionary.get("totalSessionsWon", 0)
        self.totalTripleKills = dictionary.get("totalTripleKills", 0)
        self.totalTurretsKilled = dictionary.get("totalTurretsKilled", 0)
        self.totalUnrealKills = dictionary.get("totalUnrealKills", 0)


@cassiopeia.type.core.common.inheritdocs
class RankedStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        champions (list<ChampionStats>): collection of aggregated stats summarized by champion
        modifyDate (int): date stats were last modified specified as epoch milliseconds
        summonerId (int): summoner ID
    """
    def __init__(self, dictionary):
        self.champions = [(ChampionStats(c) if not isinstance(c, ChampionStats) else c) for c in dictionary.get("champions", []) if c]
        self.modifyDate = dictionary.get("modifyDate", 0)
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def champion_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for s in self.champions:
            if s.id:
                ids.add(s.id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class ChampionStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all champion IDs contained in this object
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        val = dictionary.get("stats", None)
        self.stats = AggregatedStats(val) if val and not isinstance(val, AggregatedStats) else val


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
