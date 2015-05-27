from cassiopeia.type.dto.common import CassiopeiaDto


class PlayerStatsSummaryList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<PlayerStatsSummary> # Collection of player stats summaries associated with the summoner.
        self.playerStatSummaries = [PlayerStatsSummary(pss) if not isinstance(pss,PlayerStatsSummary) else pss for pss in dictionary["playerStatSummaries"]]

        # long # Summoner ID.
        self.summonerId = dictionary["summonerId"]



class PlayerStatsSummary(CassiopeiaDto):
    def __init__(self, dictionary):
        # AggregatedStats # Aggregated stats.
        self.aggregatedStats = AggregatedStats(dictionary["aggregatedStats"]) if not isinstance(dictionary["aggregatedStats"],AggregatedStats) else dictionary["aggregatedStats"]

        # int # Number of losses for this queue type. Returned for ranked queue types only.
        self.losses = dictionary["losses"]

        # long # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary["modifyDate"]

        # string # Player stats summary type. (Legal values: AramUnranked5x5, Ascension, CAP5x5, CoopVsAI, CoopVsAI3x3, CounterPick, FirstBlood1x1, FirstBlood2x2, Hexakill, KingPoro, NightmareBot, OdinUnranked, OneForAll5x5, RankedPremade3x3, RankedPremade5x5, RankedSolo5x5, RankedTeam3x3, RankedTeam5x5, SummonersRift6x6, Unranked, Unranked3x3, URF, URFBots)
        self.playerStatSummaryType = dictionary["playerStatSummaryType"]

        # int # Number of wins for this queue type.
        self.wins = dictionary["wins"]



class AggregatedStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Dominion only.
        self.averageAssists = dictionary["averageAssists"]

        # int # Dominion only.
        self.averageChampionsKilled = dictionary["averageChampionsKilled"]

        # int # Dominion only.
        self.averageCombatPlayerScore = dictionary["averageCombatPlayerScore"]

        # int # Dominion only.
        self.averageNodeCapture = dictionary["averageNodeCapture"]

        # int # Dominion only.
        self.averageNodeCaptureAssist = dictionary["averageNodeCaptureAssist"]

        # int # Dominion only.
        self.averageNodeNeutralize = dictionary["averageNodeNeutralize"]

        # int # Dominion only.
        self.averageNodeNeutralizeAssist = dictionary["averageNodeNeutralizeAssist"]

        # int # Dominion only.
        self.averageNumDeaths = dictionary["averageNumDeaths"]

        # int # Dominion only.
        self.averageObjectivePlayerScore = dictionary["averageObjectivePlayerScore"]

        # int # Dominion only.
        self.averageTeamObjective = dictionary["averageTeamObjective"]

        # int # Dominion only.
        self.averageTotalPlayerScore = dictionary["averageTotalPlayerScore"]

        # int # botGamesPlayed
        self.botGamesPlayed = dictionary["botGamesPlayed"]

        # int # killingSpree
        self.killingSpree = dictionary["killingSpree"]

        # int # Dominion only.
        self.maxAssists = dictionary["maxAssists"]

        # int # maxChampionsKilled
        self.maxChampionsKilled = dictionary["maxChampionsKilled"]

        # int # Dominion only.
        self.maxCombatPlayerScore = dictionary["maxCombatPlayerScore"]

        # int # maxLargestCriticalStrike
        self.maxLargestCriticalStrike = dictionary["maxLargestCriticalStrike"]

        # int # maxLargestKillingSpree
        self.maxLargestKillingSpree = dictionary["maxLargestKillingSpree"]

        # int # Dominion only.
        self.maxNodeCapture = dictionary["maxNodeCapture"]

        # int # Dominion only.
        self.maxNodeCaptureAssist = dictionary["maxNodeCaptureAssist"]

        # int # Dominion only.
        self.maxNodeNeutralize = dictionary["maxNodeNeutralize"]

        # int # Dominion only.
        self.maxNodeNeutralizeAssist = dictionary["maxNodeNeutralizeAssist"]

        # int # Only returned for ranked statistics.
        self.maxNumDeaths = dictionary["maxNumDeaths"]

        # int # Dominion only.
        self.maxObjectivePlayerScore = dictionary["maxObjectivePlayerScore"]

        # int # Dominion only.
        self.maxTeamObjective = dictionary["maxTeamObjective"]

        # int # maxTimePlayed
        self.maxTimePlayed = dictionary["maxTimePlayed"]

        # int # maxTimeSpentLiving
        self.maxTimeSpentLiving = dictionary["maxTimeSpentLiving"]

        # int # Dominion only.
        self.maxTotalPlayerScore = dictionary["maxTotalPlayerScore"]

        # int # mostChampionKillsPerSession
        self.mostChampionKillsPerSession = dictionary["mostChampionKillsPerSession"]

        # int # mostSpellsCast
        self.mostSpellsCast = dictionary["mostSpellsCast"]

        # int # normalGamesPlayed
        self.normalGamesPlayed = dictionary["normalGamesPlayed"]

        # int # rankedPremadeGamesPlayed
        self.rankedPremadeGamesPlayed = dictionary["rankedPremadeGamesPlayed"]

        # int # rankedSoloGamesPlayed
        self.rankedSoloGamesPlayed = dictionary["rankedSoloGamesPlayed"]

        # int # totalAssists
        self.totalAssists = dictionary["totalAssists"]

        # int # totalChampionKills
        self.totalChampionKills = dictionary["totalChampionKills"]

        # int # totalDamageDealt
        self.totalDamageDealt = dictionary["totalDamageDealt"]

        # int # totalDamageTaken
        self.totalDamageTaken = dictionary["totalDamageTaken"]

        # int # Only returned for ranked statistics.
        self.totalDeathsPerSession = dictionary["totalDeathsPerSession"]

        # int # totalDoubleKills
        self.totalDoubleKills = dictionary["totalDoubleKills"]

        # int # totalFirstBlood
        self.totalFirstBlood = dictionary["totalFirstBlood"]

        # int # totalGoldEarned
        self.totalGoldEarned = dictionary["totalGoldEarned"]

        # int # totalHeal
        self.totalHeal = dictionary["totalHeal"]

        # int # totalMagicDamageDealt
        self.totalMagicDamageDealt = dictionary["totalMagicDamageDealt"]

        # int # totalMinionKills
        self.totalMinionKills = dictionary["totalMinionKills"]

        # int # totalNeutralMinionsKilled
        self.totalNeutralMinionsKilled = dictionary["totalNeutralMinionsKilled"]

        # int # Dominion only.
        self.totalNodeCapture = dictionary["totalNodeCapture"]

        # int # Dominion only.
        self.totalNodeNeutralize = dictionary["totalNodeNeutralize"]

        # int # totalPentaKills
        self.totalPentaKills = dictionary["totalPentaKills"]

        # int # totalPhysicalDamageDealt
        self.totalPhysicalDamageDealt = dictionary["totalPhysicalDamageDealt"]

        # int # totalQuadraKills
        self.totalQuadraKills = dictionary["totalQuadraKills"]

        # int # totalSessionsLost
        self.totalSessionsLost = dictionary["totalSessionsLost"]

        # int # totalSessionsPlayed
        self.totalSessionsPlayed = dictionary["totalSessionsPlayed"]

        # int # totalSessionsWon
        self.totalSessionsWon = dictionary["totalSessionsWon"]

        # int # totalTripleKills
        self.totalTripleKills = dictionary["totalTripleKills"]

        # int # totalTurretsKilled
        self.totalTurretsKilled = dictionary["totalTurretsKilled"]

        # int # totalUnrealKills
        self.totalUnrealKills = dictionary["totalUnrealKills"]



class RankedStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<ChampionStats> # Collection of aggregated stats summarized by champion.
        self.champions = [ChampionStats(c) if not isinstance(c,ChampionStats) else c for c in dictionary["champions"]]

        # long # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary["modifyDate"]

        # long # Summoner ID.
        self.summonerId = dictionary["summonerId"]



class ChampionStats(CassiopeiaDto):
    def __init__(self, dictionary):

        # int # Champion ID. Note that champion ID 0 represents the combined stats for all champions. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        self.id = dictionary["id"]

        # AggregatedStats # Aggregated stats associated with the champion.
        self.stats = AggregatedStats(dictionary["stats"]) if not isinstance(dictionary["stats"],AggregatedStats) else dictionary["stats"]