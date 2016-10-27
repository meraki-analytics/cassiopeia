import cassiopeia.type.core.common
import cassiopeia.type.dto.common


@cassiopeia.type.core.common.inheritdocs
class ChampionMastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        championId (int): champion ID for this entry
        championLevel (int): champion level for specified player and champion combination
        championPoints (int): total number of champion points for this player and champion combination - they are used to determine championLevel
        championPointsSinceLastLevel (int): number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion.
        championPointsUntilNextLevel (int): number of points needed to achieve next level. Zero if player reached maximum champion level for this champion.
        chestGranted (bool): is chest granted for this champion or not in current season
        lastPlayTime (int): last time this champion was played by this player - in Unix milliseconds time format
        playerId (int): player ID for this entry
        tokensEarned (int): number of token earned for next level mastery
    """

    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.championLevel = dictionary.get("championLevel", 0)
        self.championPoints = dictionary.get("championPoints", 0)
        self.championPointsSinceLastLevel = dictionary.get("championPointsSinceLastLevel", 0)
        self.championPointsUntilNextLevel = dictionary.get("championPointsUntilNextLevel", 0)
        self.chestGranted = dictionary.get("chestGranted", False)
        self.lastPlayTime = dictionary.get("lastPlayTime", 0)
        self.playerId = dictionary.get("playerId", 0)
        self.tokensEarned = dictionary.get("tokensEarned", 0)
