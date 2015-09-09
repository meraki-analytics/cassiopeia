import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.currentgame import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_rune():
    global Rune
    @cassiopeia.type.core.common.inheritdocs
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameRune"
        count = sqlalchemy.Column(sqlalchemy.Integer)
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))

def _sa_bind_mastery():
    global Mastery
    @cassiopeia.type.core.common.inheritdocs
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameMastery"
        masteryId = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _participant_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameParticipant._id", ondelete="CASCADE"))

def _sa_bind_observer():
    global Observer
    @cassiopeia.type.core.common.inheritdocs
    class Observer(Observer, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameObserver"
        encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_current_game_participant():
    global CurrentGameParticipant
    @cassiopeia.type.core.common.inheritdocs
    class CurrentGameParticipant(CurrentGameParticipant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameParticipant"
        bot = sqlalchemy.Column(sqlalchemy.Boolean)
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Mastery", cascade="all, delete-orphan", passive_deletes=True)
        profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        runes = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Rune", cascade="all, delete-orphan", passive_deletes=True)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        summonerId = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_banned_champion():
    global BannedChampion
    @cassiopeia.type.core.common.inheritdocs
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("CurrentGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_current_game_info():
    global CurrentGameInfo
    @cassiopeia.type.core.common.inheritdocs
    class CurrentGameInfo(CurrentGameInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "CurrentGameInfo"
        bannedChampions = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
        gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        gameLength = sqlalchemy.Column(sqlalchemy.Integer)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        gameQueueConfigId = sqlalchemy.Column(sqlalchemy.Integer)
        gameStartTime = sqlalchemy.Column(sqlalchemy.BigInteger)
        gameType = sqlalchemy.Column(sqlalchemy.String(30))
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        observers = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.Observer", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.currentgame.CurrentGameParticipant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))

def _sa_bind_all():
    _sa_bind_rune()
    _sa_bind_mastery()
    _sa_bind_observer()
    _sa_bind_current_game_participant()
    _sa_bind_banned_champion()
    _sa_bind_current_game_info()