from cassiopeia.type.dto.common import CassiopeiaDto

class RawStatsDto(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Number of assists
        self.assists = dictionary["assists"]

        # int # Number of enemy inhibitors killed
        self.barracksKilled = dictionary["barracksKilled"]

        # int # Number of champions killed
        self.championsKilled = dictionary["championsKilled"]

        # int # The combat player score
        self.combatPlayerScore = dictionary["combatPlayerScore"]

        # int # Number of consumables purchased
        self.consumablesPurchased = dictionary["consumablesPurchased"]

        # int # Total damage dealt
        self.damageDealtPlayer = dictionary["damageDealtPlayer"]

        # int # Number of double kills
        self.doubleKills = dictionary["doubleKills"]

        # int # First blood
        self.firstBlood = dictionary["firstBlood"]

        # int # Amount of gold
        self.gold = dictionary["gold"]

        # int # Total gold earned
        self.goldEarned = dictionary["goldEarned"]

        # int # Total gold spent
        self.goldSpent = dictionary["goldSpent"]

        # int # ID of item 0
        self.item0 = dictionary["item0"]

        # int # ID of item 1
        self.item1 = dictionary["item1"]

        # int # ID of item 2
        self.item2 = dictionary["item2"]

        # int # ID of item 3
        self.item3 = dictionary["item3"]

        # int # ID of item 4
        self.item4 = dictionary["item4"]

        # int # ID of item 5
        self.item5 = dictionary["item5"]

        # int # ID of item 6
        self.item6 = dictionary["item6"]

        # int # Number of items purchased
        self.itemsPurchased = dictionary["itemsPurchased"]

        # int # Number of killing sprees
        self.killingSprees = dictionary["killingSprees"]

        # int # Largest critical strike
        self.largestCriticalStrike = dictionary["largestCriticalStrike"]

        # int # Largest killing spree
        self.largestKillingSpree = dictionary["largestKillingSpree"]

        # int # Largest multi kill
        self.largestMultiKill = dictionary["largestMultiKill"]

        # int # Number of tier 3 items built.
        self.legendaryItemsCreated = dictionary["legendaryItemsCreated"]

        # int # Level
        self.level = dictionary["level"]

        # int # Total magic damage dealt
        self.magicDamageDealtPlayer = dictionary["magicDamageDealtPlayer"]

        # int # Total magic damage dealt to champions
        self.magicDamageDealtToChampions = dictionary["magicDamageDealtToChampions"]

        # int # Total magic damage taken
        self.magicDamageTaken = dictionary["magicDamageTaken"]

        # int # Total minions denied
        self.minionsDenied = dictionary["minionsDenied"]

        # int # Total minions killed
        self.minionsKilled = dictionary["minionsKilled"]

        # int # Total neutral minions killed
        self.neutralMinionsKilled = dictionary["neutralMinionsKilled"]

        # int # Neutral minions killed in enemy jungle
        self.neutralMinionsKilledEnemyJungle = dictionary["neutralMinionsKilledEnemyJungle"]

        # int # Neutral minions killed in own jungle
        self.neutralMinionsKilledYourJungle = dictionary["neutralMinionsKilledYourJungle"]

        # boolean # Flag specifying if the summoner got the killing blow on the nexus.
        self.nexusKilled = dictionary["nexusKilled"]

        # int # Number of nodes captured
        self.nodeCapture = dictionary["nodeCapture"]

        # int # Number of node capture assists
        self.nodeCaptureAssist = dictionary["nodeCaptureAssist"]

        # int # Number of nodes neutralized
        self.nodeNeutralize = dictionary["nodeNeutralize"]

        # int # Number of node neutralization assists
        self.nodeNeutralizeAssist = dictionary["nodeNeutralizeAssist"]

        # int # Number of deaths
        self.numDeaths = dictionary["numDeaths"]

        # int # Number of items bought
        self.numItemsBought = dictionary["numItemsBought"]

        # int # Objective player score
        self.objectivePlayerScore = dictionary["objectivePlayerScore"]

        # int # Number of penta kills
        self.pentaKills = dictionary["pentaKills"]

        # int # Total physical damage dealt
        self.physicalDamageDealtPlayer = dictionary["physicalDamageDealtPlayer"]

        # int # Total physical damage dealt to champions
        self.physicalDamageDealtToChampions = dictionary["physicalDamageDealtToChampions"]

        # int # Total physical damage taken
        self.physicalDamageTaken = dictionary["physicalDamageTaken"]

        # int # Player position
        self.playerPosition = dictionary["playerPosition"]

        # int # Player role
        self.playerRole = dictionary["playerRole"]

        # int # Number of quadra kills
        self.quadraKills = dictionary["quadraKills"]

        # int # Number of sight wards bought
        self.sightWardsBought = dictionary["sightWardsBought"]

        # int # Number of times first champion spell was cast.
        self.spell1Cast = dictionary["spell1Cast"]

        # int # Number of times second champion spell was cast.
        self.spell2Cast = dictionary["spell2Cast"]

        # int # Number of times third champion spell was cast.
        self.spell3Cast = dictionary["spell3Cast"]

        # int # Number of times fourth champion spell was cast.
        self.spell4Cast = dictionary["spell4Cast"]

        # int # Number of times summoner spell 1 was cast
        self.summonSpell1Cast = dictionary["summonSpell1Cast"]

        # int # Number of times summoner spell 2 was cast
        self.summonSpell2Cast = dictionary["summonSpell2Cast"]

        # int # Number of super monsters killed
        self.superMonsterKilled = dictionary["superMonsterKilled"]

        # int # Team
        self.team = dictionary["team"]

        # int # Team objectives
        self.teamObjective = dictionary["teamObjective"]

        # int # Time played
        self.timePlayed = dictionary["timePlayed"]

        # int # Total damage dealt
        self.totalDamageDealt = dictionary["totalDamageDealt"]

        # int # Total damage dealt to champions
        self.totalDamageDealtToChampions = dictionary["totalDamageDealtToChampions"]

        # int # Total damage taken
        self.totalDamageTaken = dictionary["totalDamageTaken"]

        # int # Total healing done
        self.totalHeal = dictionary["totalHeal"]

        # int # Total player score
        self.totalPlayerScore = dictionary["totalPlayerScore"]

        # int # Total score rank
        self.totalScoreRank = dictionary["totalScoreRank"]

        # int # Total crowd control time dealt
        self.totalTimeCrowdControlDealt = dictionary["totalTimeCrowdControlDealt"]

        # int # Number of units healed
        self.totalUnitsHealed = dictionary["totalUnitsHealed"]

        # int # Number of triple kills
        self.tripleKills = dictionary["tripleKills"]

        # int # Total true damage dealt
        self.trueDamageDealtPlayer = dictionary["trueDamageDealtPlayer"]

        # int # Total true damage dealt to champions
        self.trueDamageDealtToChampions = dictionary["trueDamageDealtToChampions"]

        # int # Total true damage taken
        self.trueDamageTaken = dictionary["trueDamageTaken"]

        # int # Number of turrets killed
        self.turretsKilled = dictionary["turretsKilled"]

        # int # Number of unreal kills
        self.unrealKills = dictionary["unrealKills"]

        # int # Total victory points
        self.victoryPointTotal = dictionary["victoryPointTotal"]

        # int # Number of vision wards bought
        self.visionWardsBought = dictionary["visionWardsBought"]

        # int # Number of wards killed
        self.wardKilled = dictionary["wardKilled"]

        # int # Number of wards placed
        self.wardPlaced = dictionary["wardPlaced"]

        # boolean # Flag specifying whether or not this game was won.
        self.win = dictionary["win"]


class Player(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion id associated with player.
        self.championId = dictionary["championId"]

        # long # Summoner id associated with player.
        self.summonerId = dictionary["summonerId"]

        # int # Team id associated with player.
        self.teamId = dictionary["teamId"]


class Game(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion ID associated with game.
        self.championId = dictionary["championId"]

        # long # Date that end game data was recorded, specified as epoch milliseconds.
        self.createDate = dictionary["createDate"]

        # list<Player> # Other players associated with the game.
        self.fellowPlayers = [Player(player) if not isinstance(player, Player) else player for player in dictionary["fellowPlayers"]]

        # long # Game ID.
        self.gameId = dictionary["gameId"]

        # string # Game mode. (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.gameMode = dictionary["gameMode"]

        # string # Game type. (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.gameType = dictionary["gameType"]

        # boolean # Invalid flag.
        self.invalid = dictionary["invalid"]

        # int # IP Earned.
        self.ipEarned = dictionary["ipEarned"]

        # int # Level.
        self.level = dictionary["level"]

        # int # Map ID.
        self.mapId = dictionary["mapId"]

        # int # ID of first summoner spell.
        self.spell1 = dictionary["spell1"]

        # int # ID of second summoner spell.
        self.spell2 = dictionary["spell2"]

        # RawStats # Statistics associated with the game for this summoner.
        self.stats = RawStats(dictionary["stats"]) if not isinstance(dictionary["stats"], RawStats) else dictionary["stats"]

        # string # Game sub-type. (Legal values: NONE, NORMAL, BOT, RANKED_SOLO_5x5, RANKED_PREMADE_3x3, RANKED_PREMADE_5x5, ODIN_UNRANKED, RANKED_TEAM_3x3, RANKED_TEAM_5x5, NORMAL_3x3, BOT_3x3, CAP_5x5, ARAM_UNRANKED_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF, URF_BOT, NIGHTMARE_BOT, ASCENSION, HEXAKILL, KING_PORO, COUNTER_PICK)
        self.subType = dictionary["subType"]

        # int # Team ID associated with game. Team ID 100 is blue team. Team ID 200 is purple team.
        self.teamId = dictionary["teamId"]


class RecentGames(CassiopeiaDto):
    def __init__(self, dictionary):
        # set<Game> # Collection of recent games played (max 10).
        self.games = {Game(game) if not isinstance(game, Game) else game for game in dictionary["games"]}

        # long # Summoner ID.
        self.summonerId = dictionary["summonerId"]