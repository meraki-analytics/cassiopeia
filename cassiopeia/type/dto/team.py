import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class Team(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Date that team was created specified as epoch milliseconds.
        self.createDate = dictionary.get("createDate", 0)

        # str # FullId
        self.fullId = dictionary.get("fullId", "")

        # int # Date that last game played by team ended specified as epoch milliseconds.
        self.lastGameDate = dictionary.get("lastGameDate", 0)

        # int # Date that last member joined specified as epoch milliseconds.
        self.lastJoinDate = dictionary.get("lastJoinDate", 0)

        # int # Date that team last joined the ranked team queue specified as epoch milliseconds.
        self.lastJoinedRankedTeamQueueDate = dictionary.get("lastJoinedRankedTeamQueueDate", 0)

        # list<MatchHistorySummary> # MatchHistory
        self.matchHistory = [(MatchHistorySummary(mh) if not isinstance(mh, MatchHistorySummary) else mh) for mh in dictionary.get("matchHistory", []) if mh]

        # int # Date that team was last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate", 0)

        # str # Name
        self.name = dictionary.get("name", "")

        # Roster # Roster
        val = dictionary.get("roster", None)
        self.roster = Roster(val) if val and not isinstance(val, Roster) else val

        # int # Date that second to last member joined specified as epoch milliseconds.
        self.secondLastJoinDate = dictionary.get("secondLastJoinDate", 0)

        # str # Status
        self.status = dictionary.get("status", "")

        # str # Tag
        self.tag = dictionary.get("tag", "")

        # list<TeamStatDetail> # Stat details
        self.teamStatDetails = [(TeamStatDetail(ts) if not isinstance(ts, TeamStatDetail) else ts) for ts in dictionary.get("teamStatDetails", []) if ts]

        # int # Date that third to last member joined specified as epoch milliseconds.
        self.thirdLastJoinDate = dictionary.get("thirdLastJoinDate", 0)

    @property
    def summoner_ids(self):
        ids = set()
        ids.add(self.roster.ownerId)
        for member in self.roster.memberList:
            ids.add(member.playerId)
        return ids


class MatchHistorySummary(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Assists
        self.assists = dictionary.get("assists", 0)

        # int # Date that match was completed specified as epoch milliseconds.
        self.date = dictionary.get("date", 0)

        # int # Deaths
        self.deaths = dictionary.get("deaths", 0)

        # int # GameId
        self.gameId = dictionary.get("gameId", 0)

        # str # GameMode
        self.gameMode = dictionary.get("gameMode", "")

        # bool # Invalid
        self.invalid = dictionary.get("invalid", False)

        # int # Kills
        self.kills = dictionary.get("kills", 0)

        # int # MapId
        self.mapId = dictionary.get("mapId", 0)

        # int # OpposingTeamKills
        self.opposingTeamKills = dictionary.get("opposingTeamKills", 0)

        # str # OpposingTeamName
        self.opposingTeamName = dictionary.get("opposingTeamName", "")

        # bool # Win
        self.win = dictionary.get("win", False)


class Roster(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<TeamMemberInfo> # MemberList
        self.memberList = [(TeamMemberInfo(ts) if not isinstance(ts, TeamMemberInfo) else ts) for ts in dictionary.get("memberList", []) if ts]

        # int # OwnerId
        self.ownerId = dictionary.get("ownerId", 0)


class TeamStatDetail(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # AverageGamesPlayed
        self.averageGamesPlayed = dictionary.get("averageGamesPlayed", 0)

        # int # Losses
        self.losses = dictionary.get("losses", 0)

        # str # TeamStatType
        self.teamStatType = dictionary.get("teamStatType", "")

        # int # Wins
        self.wins = dictionary.get("wins", 0)


class TeamMemberInfo(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Date that team member was invited to team specified as epoch milliseconds.
        self.inviteDate = dictionary.get("inviteDate", 0)

        # int # Date that team member joined team specified as epoch milliseconds.
        self.joinDate = dictionary.get("joinDate", 0)

        # int # PlayerId
        self.playerId = dictionary.get("playerId", 0)

        # str # Status
        self.status = dictionary.get("status", "")

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_bind_team():
    global Team
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

def sa_bind_match_history_summary():
    global MatchHistorySummary
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

def sa_bind_roster():
    global Roster
    class Roster(Roster, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Roster"
        memberList = sqlalchemy.orm.relationship("cassiopeia.type.dto.team.TeamMemberInfo", cascade="all, delete-orphan", passive_deletes=True)
        ownerId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.ForeignKey("Team.fullId", ondelete="CASCADE"))

def sa_bind_team_stat_detail():
    global TeamStatDetail
    class TeamStatDetail(TeamStatDetail, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "TeamStatDetail"
        averageGamesPlayed = sqlalchemy.Column(sqlalchemy.Integer)
        losses = sqlalchemy.Column(sqlalchemy.Integer)
        teamStatType = sqlalchemy.Column(sqlalchemy.String(30))
        wins = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _team_id = sqlalchemy.Column(sqlalchemy.String(50), sqlalchemy.ForeignKey("Team.fullId", ondelete="CASCADE"))

def sa_bind_team_member_info():
    global TeamMemberInfo
    class TeamMemberInfo(TeamMemberInfo, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "TeamMemberInfo"
        inviteDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        joinDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        playerId = sqlalchemy.Column(sqlalchemy.Integer)
        status = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _roster_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Roster._id", ondelete="CASCADE"))

def sa_bind_all():
    sa_bind_team()
    sa_bind_match_history_summary()
    sa_bind_roster()
    sa_bind_team_stat_detail()
    sa_bind_team_member_info()