import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class RawStats(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Number of assists
        self.assists = dictionary.get("assists", 0)

        # int # Number of enemy inhibitors killed
        self.barracksKilled = dictionary.get("barracksKilled", 0)

        # int # Number of champions killed
        self.championsKilled = dictionary.get("championsKilled", 0)

        # int # The combat player score
        self.combatPlayerScore = dictionary.get("combatPlayerScore", 0)

        # int # Number of consumables purchased
        self.consumablesPurchased = dictionary.get("consumablesPurchased", 0)

        # int # Total damage dealt
        self.damageDealtPlayer = dictionary.get("damageDealtPlayer", 0)

        # int # Number of double kills
        self.doubleKills = dictionary.get("doubleKills", 0)

        # int # First blood
        self.firstBlood = dictionary.get("firstBlood", 0)

        # int # Amount of gold
        self.gold = dictionary.get("gold", 0)

        # int # Total gold earned
        self.goldEarned = dictionary.get("goldEarned", 0)

        # int # Total gold spent
        self.goldSpent = dictionary.get("goldSpent", 0)

        # int # ID of item 0
        self.item0 = dictionary.get("item0", 0)

        # int # ID of item 1
        self.item1 = dictionary.get("item1", 0)

        # int # ID of item 2
        self.item2 = dictionary.get("item2", 0)

        # int # ID of item 3
        self.item3 = dictionary.get("item3", 0)

        # int # ID of item 4
        self.item4 = dictionary.get("item4", 0)

        # int # ID of item 5
        self.item5 = dictionary.get("item5", 0)

        # int # ID of item 6
        self.item6 = dictionary.get("item6", 0)

        # int # Number of items purchased
        self.itemsPurchased = dictionary.get("itemsPurchased", 0)

        # int # Number of killing sprees
        self.killingSprees = dictionary.get("killingSprees", 0)

        # int # Largest critical strike
        self.largestCriticalStrike = dictionary.get("largestCriticalStrike", 0)

        # int # Largest killing spree
        self.largestKillingSpree = dictionary.get("largestKillingSpree", 0)

        # int # Largest multi kill
        self.largestMultiKill = dictionary.get("largestMultiKill", 0)

        # int # Number of tier 3 items built.
        self.legendaryItemsCreated = dictionary.get("legendaryItemsCreated", 0)

        # int # Level
        self.level = dictionary.get("level", 0)

        # int # Total magic damage dealt
        self.magicDamageDealtPlayer = dictionary.get("magicDamageDealtPlayer", 0)

        # int # Total magic damage dealt to champions
        self.magicDamageDealtToChampions = dictionary.get("magicDamageDealtToChampions", 0)

        # int # Total magic damage taken
        self.magicDamageTaken = dictionary.get("magicDamageTaken", 0)

        # int # Total minions denied
        self.minionsDenied = dictionary.get("minionsDenied", 0)

        # int # Total minions killed
        self.minionsKilled = dictionary.get("minionsKilled", 0)

        # int # Total neutral minions killed
        self.neutralMinionsKilled = dictionary.get("neutralMinionsKilled", 0)

        # int # Neutral minions killed in enemy jungle
        self.neutralMinionsKilledEnemyJungle = dictionary.get("neutralMinionsKilledEnemyJungle", 0)

        # int # Neutral minions killed in own jungle
        self.neutralMinionsKilledYourJungle = dictionary.get("neutralMinionsKilledYourJungle", 0)

        # bool # Flag specifying if the summoner got the killing blow on the nexus.
        self.nexusKilled = dictionary.get("nexusKilled", False)

        # int # Number of nodes captured
        self.nodeCapture = dictionary.get("nodeCapture", 0)

        # int # Number of node capture assists
        self.nodeCaptureAssist = dictionary.get("nodeCaptureAssist", 0)

        # int # Number of nodes neutralized
        self.nodeNeutralize = dictionary.get("nodeNeutralize", 0)

        # int # Number of node neutralization assists
        self.nodeNeutralizeAssist = dictionary.get("nodeNeutralizeAssist", 0)

        # int # Number of deaths
        self.numDeaths = dictionary.get("numDeaths", 0)

        # int # Number of items bought
        self.numItemsBought = dictionary.get("numItemsBought", 0)

        # int # Objective player score
        self.objectivePlayerScore = dictionary.get("objectivePlayerScore", 0)

        # int # Number of penta kills
        self.pentaKills = dictionary.get("pentaKills", 0)

        # int # Total physical damage dealt
        self.physicalDamageDealtPlayer = dictionary.get("physicalDamageDealtPlayer", 0)

        # int # Total physical damage dealt to champions
        self.physicalDamageDealtToChampions = dictionary.get("physicalDamageDealtToChampions", 0)

        # int # Total physical damage taken
        self.physicalDamageTaken = dictionary.get("physicalDamageTaken", 0)

        # int # Player position
        self.playerPosition = dictionary.get("playerPosition", 0)

        # int # Player role
        self.playerRole = dictionary.get("playerRole", 0)

        # int # Number of quadra kills
        self.quadraKills = dictionary.get("quadraKills", 0)

        # int # Number of sight wards bought
        self.sightWardsBought = dictionary.get("sightWardsBought", 0)

        # int # Number of times first champion spell was cast.
        self.spell1Cast = dictionary.get("spell1Cast", 0)

        # int # Number of times second champion spell was cast.
        self.spell2Cast = dictionary.get("spell2Cast", 0)

        # int # Number of times third champion spell was cast.
        self.spell3Cast = dictionary.get("spell3Cast", 0)

        # int # Number of times fourth champion spell was cast.
        self.spell4Cast = dictionary.get("spell4Cast", 0)

        # int # Number of times summoner spell 1 was cast
        self.summonSpell1Cast = dictionary.get("summonSpell1Cast", 0)

        # int # Number of times summoner spell 2 was cast
        self.summonSpell2Cast = dictionary.get("summonSpell2Cast", 0)

        # int # Number of super monsters killed
        self.superMonsterKilled = dictionary.get("superMonsterKilled", 0)

        # int # Team
        self.team = dictionary.get("team", 0)

        # int # Team objectives
        self.teamObjective = dictionary.get("teamObjective", 0)

        # int # Time played
        self.timePlayed = dictionary.get("timePlayed", 0)

        # int # Total damage dealt
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)

        # int # Total damage dealt to champions
        self.totalDamageDealtToChampions = dictionary.get("totalDamageDealtToChampions", 0)

        # int # Total damage taken
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)

        # int # Total healing done
        self.totalHeal = dictionary.get("totalHeal", 0)

        # int # Total player score
        self.totalPlayerScore = dictionary.get("totalPlayerScore", 0)

        # int # Total score rank
        self.totalScoreRank = dictionary.get("totalScoreRank", 0)

        # int # Total crowd control time dealt
        self.totalTimeCrowdControlDealt = dictionary.get("totalTimeCrowdControlDealt", 0)

        # int # Number of units healed
        self.totalUnitsHealed = dictionary.get("totalUnitsHealed", 0)

        # int # Number of triple kills
        self.tripleKills = dictionary.get("tripleKills", 0)

        # int # Total true damage dealt
        self.trueDamageDealtPlayer = dictionary.get("trueDamageDealtPlayer", 0)

        # int # Total true damage dealt to champions
        self.trueDamageDealtToChampions = dictionary.get("trueDamageDealtToChampions", 0)

        # int # Total true damage taken
        self.trueDamageTaken = dictionary.get("trueDamageTaken", 0)

        # int # Number of turrets killed
        self.turretsKilled = dictionary.get("turretsKilled", 0)

        # int # Number of unreal kills
        self.unrealKills = dictionary.get("unrealKills", 0)

        # int # Total victory points
        self.victoryPointTotal = dictionary.get("victoryPointTotal", 0)

        # int # Number of vision wards bought
        self.visionWardsBought = dictionary.get("visionWardsBought", 0)

        # int # Number of wards killed
        self.wardKilled = dictionary.get("wardKilled", 0)

        # int # Number of wards placed
        self.wardPlaced = dictionary.get("wardPlaced", 0)

        # bool # Flag specifying whether or not this game was won.
        self.win = dictionary.get("win", False)


class Player(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion id associated with player.
        self.championId = dictionary.get("championId", 0)

        # int # Summoner id associated with player.
        self.summonerId = dictionary.get("summonerId", 0)

        # int # Team id associated with player.
        self.teamId = dictionary.get("teamId", 0)


class Game(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Champion ID associated with game.
        self.championId = dictionary.get("championId", 0)

        # int # Date that end game data was recorded, specified as epoch milliseconds.
        self.createDate = dictionary.get("createDate", 0)

        # list<Player> # Other players associated with the game.
        self.fellowPlayers = [(Player(player) if not isinstance(player, Player) else player) for player in dictionary.get("fellowPlayers", []) if player]

        # int # Game ID.
        self.gameId = dictionary.get("gameId", 0)

        # str # Game mode. (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        self.gameMode = dictionary.get("gameMode", "")

        # str # Game type. (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        self.gameType = dictionary.get("gameType", "")

        # bool # Invalid flag.
        self.invalid = dictionary.get("invalid", False)

        # int # IP Earned.
        self.ipEarned = dictionary.get("ipEarned", 0)

        # int # Level.
        self.level = dictionary.get("level", 0)

        # int # Map ID.
        self.mapId = dictionary.get("mapId", 0)

        # int # ID of first summoner spell.
        self.spell1 = dictionary.get("spell1", 0)

        # int # ID of second summoner spell.
        self.spell2 = dictionary.get("spell2", 0)

        # RawStats # Statistics associated with the game for this summoner.
        val = dictionary.get("stats", None)
        self.stats = RawStats(val) if val and not isinstance(val, RawStats) else val

        # str # Game sub-type. (Legal values: NONE, NORMAL, BOT, RANKED_SOLO_5x5, RANKED_PREMADE_3x3, RANKED_PREMADE_5x5, ODIN_UNRANKED, RANKED_TEAM_3x3, RANKED_TEAM_5x5, NORMAL_3x3, BOT_3x3, CAP_5x5, ARAM_UNRANKED_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF, URF_BOT, NIGHTMARE_BOT, ASCENSION, HEXAKILL, KING_PORO, COUNTER_PICK)
        self.subType = dictionary.get("subType", "")

        # int # Team ID associated with game. Team ID 100 is blue team. Team ID 300 is purple team.
        self.teamId = dictionary.get("teamId", 0)

    @property
    def champion_ids(self):
        ids = set()
        ids.add(self.championId)
        for p in self.fellowPlayers:
            ids.add(p.championId)
        return ids

    @property
    def summoner_ids(self):
        ids = set()
        for p in self.fellowPlayers:
            if(p.summonerId):
                ids.add(p.summonerId)
        return ids

    @property
    def summoner_spell_ids(self):
        ids = set()
        ids.add(self.spell1)
        ids.add(self.spell2)
        return ids

    @property
    def item_ids(self):
        ids = set()
        s = self.stats
        if(s.item0):
            ids.add(s.item0)
        if(s.item1):
            ids.add(s.item1)
        if(s.item2):
            ids.add(s.item2)
        if(s.item3):
            ids.add(s.item3)
        if(s.item4):
            ids.add(s.item4)
        if(s.item5):
            ids.add(s.item5)
        if(s.item6):
            ids.add(s.item6)
        return ids


class RecentGames(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Game> # Collection of recent games played (max 10).
        self.games = [(Game(game) if not isinstance(game, Game) else game) for game in dictionary.get("games", []) if game]

        # int # Summoner ID.
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def champion_ids(self):
        ids = set()
        for game in self.games:
            ids |= game.champion_ids
        return ids

    @property
    def summoner_ids(self):
        ids = set()
        ids.add(self.summonerId)
        for game in self.games:
            ids |= game.summoner_ids
        return ids

    @property
    def summoner_spell_ids(self):
        ids = set()
        for game in self.games:
            ids |= game.summoner_spell_ids
        return ids

    @property
    def item_ids(self):
        ids = set()
        for game in self.games:
            ids |= game.item_ids
        return ids

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_bind_raw_stats():
    global RawStats
    class RawStats(RawStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "GameRawStats"
        assists = sqlalchemy.Column(sqlalchemy.Integer)
        barracksKilled = sqlalchemy.Column(sqlalchemy.Integer)
        championsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        combatPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        consumablesPurchased = sqlalchemy.Column(sqlalchemy.Integer)
        damageDealtPlayer = sqlalchemy.Column(sqlalchemy.Integer)
        doubleKills = sqlalchemy.Column(sqlalchemy.Integer)
        firstBlood = sqlalchemy.Column(sqlalchemy.Integer)
        gold = sqlalchemy.Column(sqlalchemy.Integer)
        goldEarned = sqlalchemy.Column(sqlalchemy.Integer)
        goldSpent = sqlalchemy.Column(sqlalchemy.Integer)
        item0 = sqlalchemy.Column(sqlalchemy.Integer)
        item1 = sqlalchemy.Column(sqlalchemy.Integer)
        item2 = sqlalchemy.Column(sqlalchemy.Integer)
        item3 = sqlalchemy.Column(sqlalchemy.Integer)
        item4 = sqlalchemy.Column(sqlalchemy.Integer)
        item5 = sqlalchemy.Column(sqlalchemy.Integer)
        item6 = sqlalchemy.Column(sqlalchemy.Integer)
        itemsPurchased = sqlalchemy.Column(sqlalchemy.Integer)
        killingSprees = sqlalchemy.Column(sqlalchemy.Integer)
        largestCriticalStrike = sqlalchemy.Column(sqlalchemy.Integer)
        largestKillingSpree = sqlalchemy.Column(sqlalchemy.Integer)
        largestMultiKill = sqlalchemy.Column(sqlalchemy.Integer)
        legendaryItemsCreated = sqlalchemy.Column(sqlalchemy.Integer)
        level = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageDealtPlayer = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        magicDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        minionsDenied = sqlalchemy.Column(sqlalchemy.Integer)
        minionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilledEnemyJungle = sqlalchemy.Column(sqlalchemy.Integer)
        neutralMinionsKilledYourJungle = sqlalchemy.Column(sqlalchemy.Integer)
        nexusKilled = sqlalchemy.Column(sqlalchemy.Boolean)
        nodeCapture = sqlalchemy.Column(sqlalchemy.Integer)
        nodeCaptureAssist = sqlalchemy.Column(sqlalchemy.Integer)
        nodeNeutralize = sqlalchemy.Column(sqlalchemy.Integer)
        nodeNeutralizeAssist = sqlalchemy.Column(sqlalchemy.Integer)
        numDeaths = sqlalchemy.Column(sqlalchemy.Integer)
        numItemsBought = sqlalchemy.Column(sqlalchemy.Integer)
        objectivePlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        pentaKills = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageDealtPlayer = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        physicalDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        playerPosition = sqlalchemy.Column(sqlalchemy.Integer)
        playerRole = sqlalchemy.Column(sqlalchemy.Integer)
        quadraKills = sqlalchemy.Column(sqlalchemy.Integer)
        sightWardsBought = sqlalchemy.Column(sqlalchemy.Integer)
        spell1Cast = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Cast = sqlalchemy.Column(sqlalchemy.Integer)
        spell3Cast = sqlalchemy.Column(sqlalchemy.Integer)
        spell4Cast = sqlalchemy.Column(sqlalchemy.Integer)
        summonSpell1Cast = sqlalchemy.Column(sqlalchemy.Integer)
        summonSpell2Cast = sqlalchemy.Column(sqlalchemy.Integer)
        superMonsterKilled = sqlalchemy.Column(sqlalchemy.Integer)
        team = sqlalchemy.Column(sqlalchemy.Integer)
        teamObjective = sqlalchemy.Column(sqlalchemy.Integer)
        timePlayed = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        totalDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        totalHeal = sqlalchemy.Column(sqlalchemy.Integer)
        totalPlayerScore = sqlalchemy.Column(sqlalchemy.Integer)
        totalScoreRank = sqlalchemy.Column(sqlalchemy.Integer)
        totalTimeCrowdControlDealt = sqlalchemy.Column(sqlalchemy.Integer)
        totalUnitsHealed = sqlalchemy.Column(sqlalchemy.Integer)
        tripleKills = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageDealtPlayer = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageDealtToChampions = sqlalchemy.Column(sqlalchemy.Integer)
        trueDamageTaken = sqlalchemy.Column(sqlalchemy.Integer)
        turretsKilled = sqlalchemy.Column(sqlalchemy.Integer)
        unrealKills = sqlalchemy.Column(sqlalchemy.Integer)
        victoryPointTotal = sqlalchemy.Column(sqlalchemy.Integer)
        visionWardsBought = sqlalchemy.Column(sqlalchemy.Integer)
        wardKilled = sqlalchemy.Column(sqlalchemy.Integer)
        wardPlaced = sqlalchemy.Column(sqlalchemy.Integer)
        win = sqlalchemy.Column(sqlalchemy.Boolean)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Game.gameId", ondelete="CASCADE"))

def sa_bind_player():
    global Player
    class Player(Player, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "GamePlayer"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Game.gameId", ondelete="CASCADE"))

def sa_bind_game():
    global Game
    class Game(Game, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Game"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        createDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        fellowPlayers = sqlalchemy.orm.relationship("cassiopeia.type.dto.game.Player", cascade="all, delete-orphan", passive_deletes=True)
        gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        gameType = sqlalchemy.Column(sqlalchemy.String(30))
        invalid = sqlalchemy.Column(sqlalchemy.Boolean)
        ipEarned = sqlalchemy.Column(sqlalchemy.Integer)
        level = sqlalchemy.Column(sqlalchemy.Integer)
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        spell1 = sqlalchemy.Column(sqlalchemy.Integer)
        spell2 = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.game.RawStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        subType = sqlalchemy.Column(sqlalchemy.String(30))
        teamId = sqlalchemy.Column(sqlalchemy.Integer)

def sa_bind_all():
    sa_bind_raw_stats()
    sa_bind_player()
    sa_bind_game()