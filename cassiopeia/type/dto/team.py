import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.team import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_team():
    global Team
    @cassiopeia.type.core.common.inheritdocs
    class Team(Team, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Team"
        createDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        fullId = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
        lastGameDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        lastJoinDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        lastJoinedRankedTeamQueueDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        matchHistory = sqlalchemy.orm.relationship("cassiopeia.type.dto.team.MatchHistorySummary", cascade="all, delete-orphan", passive_deletes=True)
        modifyDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        roster = sqlalchemy.orm.relationship("cassiopeia.type.dto.team.Roster", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        secondLastJoinDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        status = sqlalchemy.Column(sqlalchemy.String(30))
        tag = sqlalchemy.Column(sqlalchemy.String(30))
        teamStatDetails = sqlalchemy.orm.relationship("cassiopeia.type.dto.team.TeamStatDetail", cascade="all, delete-orphan", passive_deletes=True)
        thirdLastJoinDate = sqlalchemy.Column(sqlalchemy.BigInteger)

def _sa_bind_match_history_summary():
    global MatchHistorySummary
    @cassiopeia.type.core.common.inheritdocs
    class MatchHistorySummary(MatchHistorySummary, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "TeamMatchHistorySummary"
        assists = sqlalchemy.Column(sqlalchemy.Integer)
        date = sqlalchemy.Column(sqlalchemy.BigInteger)
        deaths = sqlalchemy.Column(sqlalchemy.Integer)
        gameId = sqlalchemy.Column(sqlalchemy.Integer)
        gameMode = sqlalchemy.Column(sqlalchemy.String(30))
        invalid = sqlalchemy.Column(sqlalchemy.Boolean)
        kills = sqlalchemy.Column(sqlalchemy.Integer)
        mapId = sqlalchemy.Column(sqlalchemy.Integer)
        opposingTeamKills = sqlalchemy.Column(sqlalchemy.Integer)
        opposingTeamName = sqlalchemy.Column(sqlalchemy.String(30))
        win = sqlalchemy.Column(sqlalchemy.Boolean)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.ForeignKey("Team.fullId", ondelete="CASCADE"))

def _sa_bind_roster():
    global Roster
    @cassiopeia.type.core.common.inheritdocs
    class Roster(Roster, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Roster"
        memberList = sqlalchemy.orm.relationship("cassiopeia.type.dto.team.TeamMemberInfo", cascade="all, delete-orphan", passive_deletes=True)
        ownerId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.ForeignKey("Team.fullId", ondelete="CASCADE"))

def _sa_bind_team_stat_detail():
    global TeamStatDetail
    @cassiopeia.type.core.common.inheritdocs
    class TeamStatDetail(TeamStatDetail, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "TeamStatDetail"
        averageGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        losses = sqlalchemy.Column(sqlalchemy.Integer)
        teamStatType = sqlalchemy.Column(sqlalchemy.String(30))
        wins = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.ForeignKey("Team.fullId", ondelete="CASCADE"))

def _sa_bind_team_member_info():
    global TeamMemberInfo
    @cassiopeia.type.core.common.inheritdocs
    class TeamMemberInfo(TeamMemberInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "TeamMemberInfo"
        inviteDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        joinDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        playerId = sqlalchemy.Column(sqlalchemy.Integer)
        status = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _roster_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Roster._id", ondelete="CASCADE"))

def _sa_bind_all():
    _sa_bind_team()
    _sa_bind_match_history_summary()
    _sa_bind_roster()
    _sa_bind_team_stat_detail()
    _sa_bind_team_member_info()