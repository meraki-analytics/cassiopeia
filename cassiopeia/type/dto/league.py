import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.league import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_mini_series():
    global MiniSeries
    @cassiopeia.type.core.common.inheritdocs
    class MiniSeries(MiniSeries, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MiniSeries"
        losses = sqlalchemy.Column(sqlalchemy.Integer)
        progress = sqlalchemy.Column(sqlalchemy.String(30))
        target = sqlalchemy.Column(sqlalchemy.Integer)
        wins = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _entry_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("LeagueEntry._id", ondelete="CASCADE"))

def _sa_bind_league_entry():
    global LeagueEntry
    @cassiopeia.type.core.common.inheritdocs
    class LeagueEntry(LeagueEntry, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "LeagueEntry"
        division = sqlalchemy.Column(sqlalchemy.String(30))
        isFreshBlood = sqlalchemy.Column(sqlalchemy.Boolean)
        isHotStreak = sqlalchemy.Column(sqlalchemy.Boolean)
        isInactive = sqlalchemy.Column(sqlalchemy.Boolean)
        isVeteran = sqlalchemy.Column(sqlalchemy.Boolean)
        leaguePoints = sqlalchemy.Column(sqlalchemy.Integer)
        losses = sqlalchemy.Column(sqlalchemy.Integer)
        miniSeries = sqlalchemy.orm.relationship("cassiopeia.type.dto.league.MiniSeries", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        playerOrTeamId = sqlalchemy.Column(sqlalchemy.String(50))
        playerOrTeamName = sqlalchemy.Column(sqlalchemy.String(30))
        wins = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _league_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("League._id", ondelete="CASCADE"))

def _sa_bind_league():
    global League
    @cassiopeia.type.core.common.inheritdocs
    class League(League, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "League"
        entries = sqlalchemy.orm.relationship("cassiopeia.type.dto.league.LeagueEntry", cascade="all, delete-orphan", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        participantId = sqlalchemy.Column(sqlalchemy.String(50))
        queue = sqlalchemy.Column(sqlalchemy.String(30))
        tier = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

def _sa_bind_all():
    _sa_bind_mini_series()
    _sa_bind_league_entry()
    _sa_bind_league()