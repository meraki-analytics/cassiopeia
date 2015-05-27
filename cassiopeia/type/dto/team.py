from cassiopeia.type.dto.common import CassiopeiaDto

class Team(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Date that team was created specified as epoch milliseconds.
        self.createDate = dictionary.get("createDate",0)

        # string # FullId
        self.fullId = dictionary.get("fullId",'')

        # long # Date that last game played by team ended specified as epoch milliseconds.
        self.lastGameDate = dictionary.get("lastGameDate",0)

        # long # Date that last member joined specified as epoch milliseconds.
        self.lastJoinDate = dictionary.get("lastJoinDate",0)

        # long # Date that team last joined the ranked team queue specified as epoch milliseconds.
        self.lastJoinedRankedTeamQueueDate = dictionary.get("lastJoinedRankedTeamQueueDate",0)

        # list<MatchHistorySummary> # MatchHistory
        self.matchHistory = [MatchHistorySummary(mh) if not isinstance(mh,MatchHistorySummary) else mh for mh in dictionary.get("matchHistory",[])]

        # long # Date that team was last modified specified as epoch milliseconds.
        self.modifyDate = dictionary.get("modifyDate",0)

        # string # Name
        self.name = dictionary.get("name",'')

        # Roster # Roster
        val = dictionary.get("roster", None)
        self.roster = Roster(val) if val and not isinstance(val, Roster) else val

        # long # Date that second to last member joined specified as epoch milliseconds.
        self.secondLastJoinDate = dictionary.get("secondLastJoinDate",0)

        # string # Status
        self.status = dictionary.get("status",'')

        # string # Tag
         self.tag = dictionary.get("tag",'')

        # list<TeamStatDetail> # Stat details
        self.teamStatDetails = [TeamStatDetail(ts) if not isinstance(ts,TeamStatDetail) else ts for ts in dictionary.get("teamStatDetails",[])]

        # long # Date that third to last member joined specified as epoch milliseconds.
        self.thirdLastJoinDate = dictionary.get("thirdLastJoinDate",0)


class MatchHistorySummary(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Assists
        self.assists = dictionary.get("assists",0)

        # long # Date that match was completed specified as epoch milliseconds.
        self.date = dictionary.get("date",0)

        # int # Deaths
        self.deaths = dictionary.get("deaths",0)

        # long # GameId
        self.gameId = dictionary.get("gameId",0)

        # string # GameMode
        self.gameMode = dictionary.get("gameMode",'')

        # boolean # Invalid
        self.invalid = dictionary.get("invalid",False)

        # int # Kills
        self.kills = dictionary.get("kills",0)

        # int # MapId
        self.mapId = dictionary.get("mapId",0)

        # int # OpposingTeamKills
        self.opposingTeamKills = dictionary.get("opposingTeamKills",0)

        # string # OpposingTeamName
        self.opposingTeamName = dictionary.get("opposingTeamName",'')

        # boolean # Win
        self.win = dictionary.get("win",False)


class Roster(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<TeamMemberInfo> # MemberList
        self.memberList = [TeamStatDetail(ts) if not isinstance(ts,TeamStatDetail) else ts for ts in dictionary.get("memberList",[])]

        # long # OwnerId
        self.ownerId = dictionary.get("ownerId",0)


class TeamStatDetail(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # AverageGamesPlayed
        self.averageGamesPlayed = dictionary.get("averageGamesPlayed",0)

        # int # Losses
        self.losses = dictionary.get("losses",0)

        # string # TeamStatType
        self.teamStatType = dictionary.get("teamStatType",'')

        # int # Wins
        self.wins = dictionary.get("wins",0)


class TeamMemberInfo(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Date that team member was invited to team specified as epoch milliseconds.
        self.inviteDate = dictionary.get("inviteDate",0)

        # long # Date that team member joined team specified as epoch milliseconds.
        self.joinDate = dictionary.get("joinDate",0)

        # long # PlayerId
        self.playerId = dictionary.get("playerId",0)

        # string # Status
        self.status = dictionary.get("status",'')