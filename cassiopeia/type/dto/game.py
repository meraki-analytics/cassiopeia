import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.game import *
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