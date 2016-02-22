import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class Team(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        createDate (int): date that team was created specified as epoch milliseconds
        fullId (str): fullId
        lastGameDate (int): date that last game played by team ended specified as epoch milliseconds
        lastJoinDate (int): date that last member joined specified as epoch milliseconds
        lastJoinedRankedTeamQueueDate (int): date that team last joined the ranked team queue specified as epoch milliseconds
        matchHistory (list<MatchHistorySummary>): matchHistory
        modifyDate (int): date that team was last modified specified as epoch milliseconds
        name (str): name
        roster (Roster): roster
        secondLastJoinDate (int): date that second to last member joined specified as epoch milliseconds
        status (str): status
        tag (str): tag
        teamStatDetails (list<TeamStatDetail>): stat details
        thirdLastJoinDate (int): date that third to last member joined specified as epoch milliseconds
    """
    def __init__(self, dictionary):
        self.createDate = dictionary.get("createDate", 0)
        self.fullId = dictionary.get("fullId", "")
        self.lastGameDate = dictionary.get("lastGameDate", 0)
        self.lastJoinDate = dictionary.get("lastJoinDate", 0)
        self.lastJoinedRankedTeamQueueDate = dictionary.get("lastJoinedRankedTeamQueueDate", 0)
        self.matchHistory = [(MatchHistorySummary(mh) if not isinstance(mh, MatchHistorySummary) else mh) for mh in dictionary.get("matchHistory", []) if mh]
        self.modifyDate = dictionary.get("modifyDate", 0)
        self.name = dictionary.get("name", "")
        val = dictionary.get("roster", None)
        self.roster = Roster(val) if val and not isinstance(val, Roster) else val
        self.secondLastJoinDate = dictionary.get("secondLastJoinDate", 0)
        self.status = dictionary.get("status", "")
        self.tag = dictionary.get("tag", "")
        self.teamStatDetails = [(TeamStatDetail(ts) if not isinstance(ts, TeamStatDetail) else ts) for ts in dictionary.get("teamStatDetails", []) if ts]
        self.thirdLastJoinDate = dictionary.get("thirdLastJoinDate", 0)

    @property
    def summoner_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()
        ids.add(self.roster.ownerId)
        for member in self.roster.memberList:
            ids.add(member.playerId)
        return ids


@cassiopeia.type.core.common.inheritdocs
class MatchHistorySummary(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all summoner IDs contained in this object
    """
    def __init__(self, dictionary):
        self.assists = dictionary.get("assists", 0)
        self.date = dictionary.get("date", 0)
        self.deaths = dictionary.get("deaths", 0)
        self.gameId = dictionary.get("gameId", 0)
        self.gameMode = dictionary.get("gameMode", "")
        self.invalid = dictionary.get("invalid", False)
        self.kills = dictionary.get("kills", 0)
        self.mapId = dictionary.get("mapId", 0)
        self.opposingTeamKills = dictionary.get("opposingTeamKills", 0)
        self.opposingTeamName = dictionary.get("opposingTeamName", "")
        self.win = dictionary.get("win", False)


@cassiopeia.type.core.common.inheritdocs
class Roster(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        assists (int): assists
        date (int): date that match was completed specified as epoch milliseconds
        deaths (int): deaths
        gameId (int): gameId
        gameMode (str): gameMode
        invalid (bool): invalid
        kills (int): kills
        mapId (int): mapId
        opposingTeamKills (int): opposingTeamKills
        opposingTeamName (str): opposingTeamName
        win (bool): win
    """
    def __init__(self, dictionary):
        self.memberList = [(TeamMemberInfo(ts) if not isinstance(ts, TeamMemberInfo) else ts) for ts in dictionary.get("memberList", []) if ts]
        self.ownerId = dictionary.get("ownerId", 0)


@cassiopeia.type.core.common.inheritdocs
class TeamStatDetail(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        memberList (list<TeamMemberInfo>): memberList
        ownerId (int): ownerId
    """
    def __init__(self, dictionary):
        self.averageGamesPlayed = dictionary.get("averageGamesPlayed", 0)
        self.losses = dictionary.get("losses", 0)
        self.teamStatType = dictionary.get("teamStatType", "")
        self.wins = dictionary.get("wins", 0)


@cassiopeia.type.core.common.inheritdocs
class TeamMemberInfo(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        averageGamesPlayed (int): averageGamesPlayed
        losses (int): losses
        teamStatType (str): teamStatType
        wins (int): wins
    """
    def __init__(self, dictionary):
        self.inviteDate = dictionary.get("inviteDate", 0)
        self.joinDate = dictionary.get("joinDate", 0)
        self.playerId = dictionary.get("playerId", 0)
        self.status = dictionary.get("status", "")


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
