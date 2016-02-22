import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class RawStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        assists (int): number of assists
        barracksKilled (int): number of enemy inhibitors killed
        championsKilled (int): number of champions killed
        combatPlayerScore (int): the combat player score
        consumablesPurchased (int): number of consumables purchased
        damageDealtPlayer (int): total damage dealt
        doubleKills (int): number of double kills
        firstBlood (int): first blood
        gold (int): amount of gold
        goldEarned (int): total gold earned
        goldSpent (int): total gold spent
        item0 (int): ID of item 0
        item1 (int): ID of item 1
        item2 (int): ID of item 2
        item3 (int): ID of item 3
        item4 (int): ID of item 4
        item5 (int): ID of item 5
        item6 (int): ID of item 6
        itemsPurchased (int): number of items purchased
        killingSprees (int): number of killing sprees
        largestCriticalStrike (int): largest critical strike
        largestKillingSpree (int): largest killing spree
        largestMultiKill (int): largest multi kill
        legendaryItemsCreated (int): number of tier 3 items built
        level (int): level
        magicDamageDealtPlayer (int): total magic damage dealt
        magicDamageDealtToChampions (int): total magic damage dealt to champions
        magicDamageTaken (int): total magic damage taken
        minionsDenied (int): total minions denied
        minionsKilled (int): total minions killed
        neutralMinionsKilled (int): total neutral minions killed
        neutralMinionsKilledEnemyJungle (int): neutral minions killed in enemy jungle
        neutralMinionsKilledYourJungle (int): neutral minions killed in own jungle
        nexusKilled (bool): flag specifying if the summoner got the killing blow on the nexus
        nodeCapture (int): number of nodes captured
        nodeCaptureAssist (int): number of node capture assists
        nodeNeutralize (int): number of nodes neutralized
        nodeNeutralizeAssist (int): number of node neutralization assists
        numDeaths (int): number of deaths
        numItemsBought (int): number of items bought
        objectivePlayerScore (int): objective player score
        pentaKills (int): number of penta kills
        physicalDamageDealtPlayer (int): total physical damage dealt
        physicalDamageDealtToChampions (int): total physical damage dealt to champions
        physicalDamageTaken (int): total physical damage taken
        playerPosition (int): player position
        playerRole (int): player role
        quadraKills (int): number of quadra kills
        sightWardsBought (int): number of sight wards bought
        spell1Cast (int): number of times first champion spell was cast
        spell2Cast (int): number of times second champion spell was cast
        spell3Cast (int): number of times third champion spell was cast
        spell4Cast (int): number of times fourth champion spell was cast
        summonSpell1Cast (int): number of times summoner spell 1 was cast
        summonSpell2Cast (int): number of times summoner spell 2 was cast
        superMonsterKilled (int): number of super monsters killed
        team (int): team
        teamObjective (int): team objectives
        timePlayed (int): time played
        totalDamageDealt (int): total damage dealt
        totalDamageDealtToChampions (int): total damage dealt to champions
        totalDamageTaken (int): total damage taken
        totalHeal (int): total healing done
        totalPlayerScore (int): total player score
        totalScoreRank (int): total score rank
        totalTimeCrowdControlDealt (int): total crowd control time dealt
        totalUnitsHealed (int): number of units healed
        tripleKills (int): number of triple kills
        trueDamageDealtPlayer (int): total true damage dealt
        trueDamageDealtToChampions (int): total true damage dealt to champions
        trueDamageTaken (int): total true damage taken
        turretsKilled (int): number of turrets killed
        unrealKills (int): number of unreal kills
        victoryPointTotal (int): total victory points
        visionWardsBought (int): number of vision wards bought
        wardKilled (int): number of wards killed
        wardPlaced (int): number of wards placed
        win (bool): flag specifying whether or not this game was won
    """
    def __init__(self, dictionary):
        self.assists = dictionary.get("assists", 0)
        self.barracksKilled = dictionary.get("barracksKilled", 0)
        self.championsKilled = dictionary.get("championsKilled", 0)
        self.combatPlayerScore = dictionary.get("combatPlayerScore", 0)
        self.consumablesPurchased = dictionary.get("consumablesPurchased", 0)
        self.damageDealtPlayer = dictionary.get("damageDealtPlayer", 0)
        self.doubleKills = dictionary.get("doubleKills", 0)
        self.firstBlood = dictionary.get("firstBlood", 0)
        self.gold = dictionary.get("gold", 0)
        self.goldEarned = dictionary.get("goldEarned", 0)
        self.goldSpent = dictionary.get("goldSpent", 0)
        self.item0 = dictionary.get("item0", 0)
        self.item1 = dictionary.get("item1", 0)
        self.item2 = dictionary.get("item2", 0)
        self.item3 = dictionary.get("item3", 0)
        self.item4 = dictionary.get("item4", 0)
        self.item5 = dictionary.get("item5", 0)
        self.item6 = dictionary.get("item6", 0)
        self.itemsPurchased = dictionary.get("itemsPurchased", 0)
        self.killingSprees = dictionary.get("killingSprees", 0)
        self.largestCriticalStrike = dictionary.get("largestCriticalStrike", 0)
        self.largestKillingSpree = dictionary.get("largestKillingSpree", 0)
        self.largestMultiKill = dictionary.get("largestMultiKill", 0)
        self.legendaryItemsCreated = dictionary.get("legendaryItemsCreated", 0)
        self.level = dictionary.get("level", 0)
        self.magicDamageDealtPlayer = dictionary.get("magicDamageDealtPlayer", 0)
        self.magicDamageDealtToChampions = dictionary.get("magicDamageDealtToChampions", 0)
        self.magicDamageTaken = dictionary.get("magicDamageTaken", 0)
        self.minionsDenied = dictionary.get("minionsDenied", 0)
        self.minionsKilled = dictionary.get("minionsKilled", 0)
        self.neutralMinionsKilled = dictionary.get("neutralMinionsKilled", 0)
        self.neutralMinionsKilledEnemyJungle = dictionary.get("neutralMinionsKilledEnemyJungle", 0)
        self.neutralMinionsKilledYourJungle = dictionary.get("neutralMinionsKilledYourJungle", 0)
        self.nexusKilled = dictionary.get("nexusKilled", False)
        self.nodeCapture = dictionary.get("nodeCapture", 0)
        self.nodeCaptureAssist = dictionary.get("nodeCaptureAssist", 0)
        self.nodeNeutralize = dictionary.get("nodeNeutralize", 0)
        self.nodeNeutralizeAssist = dictionary.get("nodeNeutralizeAssist", 0)
        self.numDeaths = dictionary.get("numDeaths", 0)
        self.numItemsBought = dictionary.get("numItemsBought", 0)
        self.objectivePlayerScore = dictionary.get("objectivePlayerScore", 0)
        self.pentaKills = dictionary.get("pentaKills", 0)
        self.physicalDamageDealtPlayer = dictionary.get("physicalDamageDealtPlayer", 0)
        self.physicalDamageDealtToChampions = dictionary.get("physicalDamageDealtToChampions", 0)
        self.physicalDamageTaken = dictionary.get("physicalDamageTaken", 0)
        self.playerPosition = dictionary.get("playerPosition", 0)
        self.playerRole = dictionary.get("playerRole", 0)
        self.quadraKills = dictionary.get("quadraKills", 0)
        self.sightWardsBought = dictionary.get("sightWardsBought", 0)
        self.spell1Cast = dictionary.get("spell1Cast", 0)
        self.spell2Cast = dictionary.get("spell2Cast", 0)
        self.spell3Cast = dictionary.get("spell3Cast", 0)
        self.spell4Cast = dictionary.get("spell4Cast", 0)
        self.summonSpell1Cast = dictionary.get("summonSpell1Cast", 0)
        self.summonSpell2Cast = dictionary.get("summonSpell2Cast", 0)
        self.superMonsterKilled = dictionary.get("superMonsterKilled", 0)
        self.team = dictionary.get("team", 0)
        self.teamObjective = dictionary.get("teamObjective", 0)
        self.timePlayed = dictionary.get("timePlayed", 0)
        self.totalDamageDealt = dictionary.get("totalDamageDealt", 0)
        self.totalDamageDealtToChampions = dictionary.get("totalDamageDealtToChampions", 0)
        self.totalDamageTaken = dictionary.get("totalDamageTaken", 0)
        self.totalHeal = dictionary.get("totalHeal", 0)
        self.totalPlayerScore = dictionary.get("totalPlayerScore", 0)
        self.totalScoreRank = dictionary.get("totalScoreRank", 0)
        self.totalTimeCrowdControlDealt = dictionary.get("totalTimeCrowdControlDealt", 0)
        self.totalUnitsHealed = dictionary.get("totalUnitsHealed", 0)
        self.tripleKills = dictionary.get("tripleKills", 0)
        self.trueDamageDealtPlayer = dictionary.get("trueDamageDealtPlayer", 0)
        self.trueDamageDealtToChampions = dictionary.get("trueDamageDealtToChampions", 0)
        self.trueDamageTaken = dictionary.get("trueDamageTaken", 0)
        self.turretsKilled = dictionary.get("turretsKilled", 0)
        self.unrealKills = dictionary.get("unrealKills", 0)
        self.victoryPointTotal = dictionary.get("victoryPointTotal", 0)
        self.visionWardsBought = dictionary.get("visionWardsBought", 0)
        self.wardKilled = dictionary.get("wardKilled", 0)
        self.wardPlaced = dictionary.get("wardPlaced", 0)
        self.win = dictionary.get("win", False)


@cassiopeia.type.core.common.inheritdocs
class Player(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        championId (int): champion id associated with player
        summonerId (int): summoner id associated with player
        teamId (int): team id associated with player
    """
    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.summonerId = dictionary.get("summonerId", 0)
        self.teamId = dictionary.get("teamId", 0)


@cassiopeia.type.core.common.inheritdocs
class Game(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        championId (int): champion ID associated with game
        createDate (int): date that end game data was recorded, specified as epoch milliseconds
        fellowPlayers (list<Player>): other players associated with the game
        gameId (int): game ID
        gameMode (str): game mode (Legal values: CLASSIC, ODIN, ARAM, TUTORIAL, ONEFORALL, ASCENSION, FIRSTBLOOD, KINGPORO)
        gameType (str): game type (Legal values: CUSTOM_GAME, MATCHED_GAME, TUTORIAL_GAME)
        invalid (bool): invalid flag
        ipEarned (int): IP Earned
        level (int): level
        mapId (int): map ID
        spell1 (int): ID of first summoner spell
        spell2 (int): ID of second summoner spell
        stats (RawStats): statistics associated with the game for this summoner
        subType (str): game sub-type (Legal values: NONE, NORMAL, BOT, RANKED_SOLO_5x5, RANKED_PREMADE_3x3, RANKED_PREMADE_5x5, ODIN_UNRANKED, RANKED_TEAM_3x3, RANKED_TEAM_5x5, NORMAL_3x3, BOT_3x3, CAP_5x5, ARAM_UNRANKED_5x5, ONEFORALL_5x5, FIRSTBLOOD_1x1, FIRSTBLOOD_2x2, SR_6x6, URF, URF_BOT, NIGHTMARE_BOT, ASCENSION, HEXAKILL, KING_PORO, COUNTER_PICK)
        teamId (int): team ID associated with game. Team ID 100 is blue team. Team ID 300 is purple team.
    """
    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.createDate = dictionary.get("createDate", 0)
        self.fellowPlayers = [(Player(player) if not isinstance(player, Player) else player) for player in dictionary.get("fellowPlayers", []) if player]
        self.gameId = dictionary.get("gameId", 0)
        self.gameMode = dictionary.get("gameMode", "")
        self.gameType = dictionary.get("gameType", "")
        self.invalid = dictionary.get("invalid", False)
        self.ipEarned = dictionary.get("ipEarned", 0)
        self.level = dictionary.get("level", 0)
        self.mapId = dictionary.get("mapId", 0)
        self.spell1 = dictionary.get("spell1", 0)
        self.spell2 = dictionary.get("spell2", 0)
        val = dictionary.get("stats", None)
        self.stats = RawStats(val) if val and not isinstance(val, RawStats) else val
        self.subType = dictionary.get("subType", "")
        self.teamId = dictionary.get("teamId", 0)

    @property
    def champion_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        ids.add(self.championId)
        for p in self.fellowPlayers:
            ids.add(p.championId)
        return ids

    @property
    def summoner_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for p in self.fellowPlayers:
            if p.summonerId:
                ids.add(p.summonerId)
        return ids

    @property
    def summoner_spell_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        ids.add(self.spell1)
        ids.add(self.spell2)
        return ids

    @property
    def item_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        s = self.stats
        if s.item0:
            ids.add(s.item0)
        if s.item1:
            ids.add(s.item1)
        if s.item2:
            ids.add(s.item2)
        if s.item3:
            ids.add(s.item3)
        if s.item4:
            ids.add(s.item4)
        if s.item5:
            ids.add(s.item5)
        if s.item6:
            ids.add(s.item6)
        return ids


@cassiopeia.type.core.common.inheritdocs
class RecentGames(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all champion IDs contained in this object
    """
    def __init__(self, dictionary):
        self.games = [(Game(game) if not isinstance(game, Game) else game) for game in dictionary.get("games", []) if game]
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def champion_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()
        for game in self.games:
            ids |= game.champion_ids
        return ids

    @property
    def summoner_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()
        ids.add(self.summonerId)
        for game in self.games:
            ids |= game.summoner_ids
        return ids

    @property
    def summoner_spell_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()
        for game in self.games:
            ids |= game.summoner_spell_ids
        return ids

    @property
    def item_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()
        for game in self.games:
            ids |= game.item_ids
        return ids


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_raw_stats():
    global RawStats

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_player():
    global Player

    @cassiopeia.type.core.common.inheritdocs
    class Player(Player, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "GamePlayer"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Game.gameId", ondelete="CASCADE"))


def _sa_bind_game():
    global Game

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_all():
    _sa_bind_raw_stats()
    _sa_bind_player()
    _sa_bind_game()
