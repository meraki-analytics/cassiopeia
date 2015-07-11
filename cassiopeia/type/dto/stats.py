import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class PlayerStatsSummaryList(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<PlayerStatsSummary> # Collection of player stats summaries associated with the summoner.
        self.playerStatSummaries = [(PlayerStatsSummary(pss) if not isinstance(pss, PlayerStatsSummary) else pss) for pss in dictionary.get("playerStatSummaries", None) if pss]

        # int # Summoner ID.
        self.summonerId = dictionary.get("summonerId", 0)


class PlayerStatsSummary(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "PlayerStatsSummary"
    aggregatedStats = sqlalchemy.orm.relationship("cassiopeia.type.dto.stats.AggregatedStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
    losses = sqlalchemy.Column(sqlalchemy.Integer)
    modifyDate = sqlalchemy.Column(sqlalchemy.Integer)
    playerStatSummaryType = sqlalchemy.Column(sqlalchemy.String)
    wins = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, dictionary):
        # AggregatedStats # Aggregated stats.
        val = dictionary.get("aggregatedStats", None)
        # Sometimes Riot sends {} instead of no value for this field when it's blank.
        self.aggregatedStats = None if not val else AggregatedStats(val) if not isinstance(val, AggregatedStats) else val

        # int # Number of losses for this queue type. Returned for ranked queue types only.
        self.losses = dictionary.get("losses", 0)

        # int # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate", 0)

        # str # Player stats summary type. (Legal values: AramUnranked5x5, Ascension, CAP5x5, CoopVsAI, CoopVsAI3x3, CounterPick, FirstBlood1x1, FirstBlood2x2, Hexakill, KingPoro, NightmareBot, OdinUnranked, OneForAll5x5, RankedPremade3x3, RankedPremade5x5, RankedSolo5x5, RankedTeam3x3, RankedTeam5x5, SummonersRift6x6, Unranked, Unranked3x3, URF, URFBots)
        self.playerStatSummaryType = dictionary.get("playerStatSummaryType", "")

        # int # Number of wins for this queue type.
        self.wins = dictionary.get("wins", 0)


class AggregatedStats(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
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
    _summary_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("PlayerStatsSummary._id"))

    def __init__(self, dictionary):
        # int # Dominion only.
        self.averageAssists = dictionary.get("averageAssists", 0)

        # int # Dominion only.
        self.averageChampionsKilled = dictionary.get("averageChampionsKilled", 0)

        # int # Dominion only.
        self.averageCombatPlayerScore = dictionary.get("averageCombatPlayerScore", 0)

        # int # Dominion only.
        self.averageNodeCapture = dictionary.get("averageNodeCapture", 0)

        # int # Dominion only.
        self.averageNodeCaptureAssist = dictionary.get("averageNodeCaptureAssist", 0)

        # int # Dominion only.
        self.averageNodeNeutralize = dictionary.get("averageNodeNeutralize", 0)

        # int # Dominion only.
        self.averageNodeNeutralizeAssist = dictionary.get("averageNodeNeutralizeAssist", 0)

        # int # Dominion only.
        self.averageNumDeaths = dictionary.get("averageNumDeaths", 0)

        # int # Dominion only.
        self.averageObjectivePlayerScore = dictionary.get("averageObjectivePlayerScore", 0)

        # int # Dominion only.
        self.averageTeamObjective = dictionary.get("averageTeamObjective", 0)

        # int # Dominion only.
        self.averageTotalPlayerScore = dictionary.get("averageTotalPlayerScore", 0)

        # int # botGamesPlayed
        self.botGamesPlayed = dictionary.get("botGamesPlayed", 0)

        # int # killingSpree
        self.killingSpree = dictionary.get("killingSpree", 0)

        # int # Dominion only.
        self.maxAssists = dictionary.get("maxAssists", 0)

        # int # maxChampionsKilled
        self.maxChampionsKilled = dictionary.get("maxChampionsKilled", 0)

        # int # Dominion only.
        self.maxCombatPlayerScore = dictionary.get("maxCombatPlayerScore", 0)

        # int # maxLargestCriticalStrike
        self.maxLargestCriticalStrike = dictionary.get("maxLargestCriticalStrike", 0)

        # int # maxLargestKillingSpree
        self.maxLargestKillingSpree = dictionary.get("maxLargestKillingSpree", 0)

        # int # Dominion only.
        self.maxNodeCapture = dictionary.get("maxNodeCapture", 0)

        # int # Dominion only.
        self.maxNodeCaptureAssist = dictionary.get("maxNodeCaptureAssist", 0)

        # int # Dominion only.
        self.maxNodeNeutralize = dictionary.get("maxNodeNeutralize", 0)

        # int # Dominion only.
        self.maxNodeNeutralizeAssist = dictionary.get("maxNodeNeutralizeAssist", 0)

        # int # Only returned for ranked statistics.
        self.maxNumDeaths = dictionary.get("maxNumDeaths", 0)

        # int # Dominion only.
        self.maxObjectivePlayerScore = dictionary.get("maxObjectivePlayerScore", 0)

        # int # Dominion only.
        self.maxTeamObjective = dictionary.get("maxTeamObjective", 0)

        # int # maxTimePlayed
        self.maxTimePlayed = dictionary.get("maxTimePlayed", 0)

        # int # maxTimeSpentLiving
        self.maxTimeSpentLiving = dictionary.get("maxTimeSpentLiving", 0)

        # int # Dominion only.
        self.maxTotalPlayerScore = dictionary.get("maxTotalPlayerScore", 0)

        # int # mostChampionKillsPerSession
        self.mostChampionKillsPerSession = dictionary.get("mostChampionKillsPerSession", 0)

        # int # mostSpellsCast
        self.mostSpellsCast = dictionary.get("mostSpellsCast", 0)

        # int # normalGamesPlayed
        self.normalGamesPlayed = dictionary.get("normalGamesPlayed", 0)

        # int # rankedPremadeGamesPlayed
        self.rankedPremadeGamesPlayed = dictionary.get("rankedPremadeGamesPlayed", 0)

        # int # rankedSoloGamesPlayed
        self.rankedSoloGamesPlayed = dictionary.get("rankedSoloGamesPlayed", 0)

        # int # totalAssists
        self.totalAssists = dictionary.get("totalAssists", 0)

        # int # totalChampionKills
        self.totalChampionKills = dictionary.get("totalChampionKills", 0)

        # int # totalDamageDealt
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)

        # int # totalDamageTaken
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)

        # int # Only returned for ranked statistics.
        self.totalDeathsPerSession = dictionary.get("totalDeathsPerSession", 0)

        # int # totalDoubleKills
        self.totalDoubleKills = dictionary.get("totalDoubleKills", 0)

        # int # totalFirstBlood
        self.totalFirstBlood = dictionary.get("totalFirstBlood", 0)

        # int # totalGoldEarned
        self.totalGoldEarned = dictionary.get("totalGoldEarned", 0)

        # int # totalHeal
        self.totalHeal = dictionary.get("totalHeal", 0)

        # int # totalMagicDamageDealt
        self.totalMagicDamageDealt = dictionary.get("totalMagicDamageDealt", 0)

        # int # totalMinionKills
        self.totalMinionKills = dictionary.get("totalMinionKills", 0)

        # int # totalNeutralMinionsKilled
        self.totalNeutralMinionsKilled = dictionary.get("totalNeutralMinionsKilled", 0)

        # int # Dominion only.
        self.totalNodeCapture = dictionary.get("totalNodeCapture", 0)

        # int # Dominion only.
        self.totalNodeNeutralize = dictionary.get("totalNodeNeutralize", 0)

        # int # totalPentaKills
        self.totalPentaKills = dictionary.get("totalPentaKills", 0)

        # int # totalPhysicalDamageDealt
        self.totalPhysicalDamageDealt = dictionary.get("totalPhysicalDamageDealt", 0)

        # int # totalQuadraKills
        self.totalQuadraKills = dictionary.get("totalQuadraKills", 0)

        # int # totalSessionsLost
        self.totalSessionsLost = dictionary.get("totalSessionsLost", 0)

        # int # totalSessionsPlayed
        self.totalSessionsPlayed = dictionary.get("totalSessionsPlayed", 0)

        # int # totalSessionsWon
        self.totalSessionsWon = dictionary.get("totalSessionsWon", 0)

        # int # totalTripleKills
        self.totalTripleKills = dictionary.get("totalTripleKills", 0)

        # int # totalTurretsKilled
        self.totalTurretsKilled = dictionary.get("totalTurretsKilled", 0)

        # int # totalUnrealKills
        self.totalUnrealKills = dictionary.get("totalUnrealKills", 0)


class RankedStats(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<ChampionStats> # Collection of aggregated stats summarized by champion.
        self.champions = [(ChampionStats(c) if not isinstance(c, ChampionStats) else c) for c in dictionary.get("champions", []) if c]

        # int # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate", 0)

        # int # Summoner ID.
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def champion_ids(self):
        ids = set()
        for s in self.champions:
            if(s.id):
                ids.add(s.id)
        return ids


class ChampionStats(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion ID. Note that champion ID 0 represents the combined stats for all champions. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        self.id = dictionary.get("id", 0)

        # AggregatedStats # Aggregated stats associated with the champion.
        val = dictionary.get("stats", None)
        self.stats = AggregatedStats(val) if val and not isinstance(val, AggregatedStats) else val