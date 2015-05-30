from cassiopeia.type.dto.common import CassiopeiaDto

class PlayerStatsSummaryList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<PlayerStatsSummary> # Collection of player stats summaries associated with the summoner.
        self.playerStatSummaries = [(PlayerStatsSummary(pss) if not isinstance(pss, PlayerStatsSummary) else pss) for pss in dictionary.get("playerStatSummaries", None) if pss]

        # int # Summoner ID.
        self.summonerId = dictionary.get("summonerId", 0)


class PlayerStatsSummary(CassiopeiaDto):
    def __init__(self, dictionary):
        # AggregatedStats # Aggregated stats.
        val = dictionary.get("aggregatedStats", None)
        self.aggregatedStats = AggregatedStats(val) if val and not isinstance(val, AggregatedStats) else val

        # int # Number of losses for this queue type. Returned for ranked queue types only.
        self.losses = dictionary.get("losses", 0)

        # int # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate", 0)

        # str # Player stats summary type. (Legal values: AramUnranked5x5, Ascension, CAP5x5, CoopVsAI, CoopVsAI3x3, CounterPick, FirstBlood1x1, FirstBlood2x2, Hexakill, KingPoro, NightmareBot, OdinUnranked, OneForAll5x5, RankedPremade3x3, RankedPremade5x5, RankedSolo5x5, RankedTeam3x3, RankedTeam5x5, SummonersRift6x6, Unranked, Unranked3x3, URF, URFBots)
        self.playerStatSummaryType = dictionary.get("playerStatSummaryType", "")

        # int # Number of wins for this queue type.
        self.wins = dictionary.get("wins", 0)


class AggregatedStats(CassiopeiaDto):
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


class RankedStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<ChampionStats> # Collection of aggregated stats summarized by champion.
        self.champions = [(ChampionStats(c) if not isinstance(c, ChampionStats) else c) for c in dictionary.get("champions", []) if c]

        # int # Date stats were last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate", 0)

        # int # Summoner ID.
        self.summonerId = dictionary.get("summonerId", 0)


class ChampionStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion ID. Note that champion ID 0 represents the combined stats for all champions. For static information correlating to champion IDs, please refer to the LoL Static Data API.
        self.id = dictionary.get("id", 0)

        # AggregatedStats # Aggregated stats associated with the champion.
        val = dictionary.get("stats", None)
        self.stats = AggregatedStats(val) if val and not isinstance(val, AggregatedStats) else val