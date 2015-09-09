import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.featuredgames import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_participant():
    global Participant
    @cassiopeia.type.core.common.inheritdocs
    class Participant(Participant, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameParticipant"
        bot = sqlalchemy.Column(sqlalchemy.Boolean)
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        spell1Id = sqlalchemy.Column(sqlalchemy.Integer)
        spell2Id = sqlalchemy.Column(sqlalchemy.Integer)
        summonerName = sqlalchemy.Column(sqlalchemy.String(30))
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_observer():
    global Observer
    @cassiopeia.type.core.common.inheritdocs
    class Observer(Observer, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameObserver"
        encryptionKey = sqlalchemy.Column(sqlalchemy.String(50))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_banned_champion():
    global BannedChampion
    @cassiopeia.type.core.common.inheritdocs
    class BannedChampion(BannedChampion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameBannedChampion"
        championId = sqlalchemy.Column(sqlalchemy.Integer)
        pickTurn = sqlalchemy.Column(sqlalchemy.Integer)
        teamId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _game_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("FeaturedGameInfo.gameId", ondelete="CASCADE"))

def _sa_bind_featured_game_info():
    global FeaturedGameInfo
    @cassiopeia.type.core.common.inheritdocs
    class FeaturedGameInfo(FeaturedGameInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "FeaturedGameInfo"
        bannedChampions = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.BannedChampion", cascade="all, delete-orphan", passive_deletes=True)
        gameId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        gameLength = sqlalchemy.Column(sqlalchemy.Integer)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        gameQueueConfigId = sqlalchemy.Column(sqlalchemy.Integer)
        gameStartTime = sqlalchemy.Column(sqlalchemy.BigInteger)
        gameType = sqlalchemy.Column(sqlalchemy.String(30))
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        observers = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.Observer", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        participants = sqlalchemy.orm.relationship("cassiopeia.type.dto.featuredgames.Participant", cascade="all, delete-orphan", passive_deletes=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))

def _sa_bind_all():
    _sa_bind_participant()
    _sa_bind_observer()
    _sa_bind_banned_champion()
    _sa_bind_featured_game_info()