from cassiopeia.type.dto.common import CassiopeiaDto

class Team(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Date that team was created specified as epoch milliseconds.
        self.createDate = dictionary["createDate"]

        # string # FullId
        self.fullId = dictionary["fullId"]

        # long # Date that last game played by team ended specified as epoch milliseconds.
        self.lastGameDate = dictionary["lastGameDate"]

        # long # Date that last member joined specified as epoch milliseconds.
        self.lastJoinDate = dictionary["lastJoinDate"]

        # long # Date that team last joined the ranked team queue specified as epoch milliseconds.
        self.lastJoinedRankedTeamQueueDate = dictionary["lastJoinedRankedTeamQueueDate"]

        # list<MatchHistorySummary> # MatchHistory
        self.matchHistory = [MatchHistorySummary(mh) if not isinstance(mh,MatchHistorySummary) else mh for mh in dictionary["matchHistory"]]

        # long # Date that team was last modified specified as epoch milliseconds.
        self.modifyDate = dictionary["modifyDate"]

        # string # Name
        self.name = dictionary["name"]

        # Roster # Roster
        self.roster = Roster(dictionary["roster"]) if not isinstance(dictionary["roster"],Roster) else dictionary["roster"]

        # long # Date that second to last member joined specified as epoch milliseconds.
        self.secondLastJoinDate = dictionary["secondLastJoinDate"]

        # string # Status
        self.status = dictionary["status"]

        # string # Tag
         self.tag = dictionary["tag"]

        # list<TeamStatDetail> # Stat details
        self.teamStatDetails = [TeamStatDetail(ts) if not isinstance(ts,TeamStatDetail) else ts for ts in dictionary["teamStatDetails"]]

        # long # Date that third to last member joined specified as epoch milliseconds.
        self.thirdLastJoinDate = dictionary["thirdLastJoinDate"]


class MatchHistorySummary(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Assists
        self.assists = dictionary["assists"]

        # long # Date that match was completed specified as epoch milliseconds.
        self.date = dictionary["date"]

        # int # Deaths
        self.deaths = dictionary["deaths"]

        # long # GameId
        self.gameId = dictionary["gameId"]

        # string # GameMode
        self.gameMode = dictionary["gameMode"]

        # boolean # Invalid
        self.invalid = dictionary["invalid"]

        # int # Kills
        self.kills = dictionary["kills"]

        # int # MapId
        self.mapId = dictionary["mapId"]

        # int # OpposingTeamKills
        self.opposingTeamKills = dictionary["opposingTeamKills"]

        # string # OpposingTeamName
        self.opposingTeamName = dictionary["opposingTeamName"]

        # boolean # Win
        self.win = dictionary["win"]


class Roster(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<TeamMemberInfo> # MemberList
        self.memberList = [TeamStatDetail(ts) if not isinstance(ts,TeamStatDetail) else ts for ts in dictionary["memberList"]]

        # long # OwnerId
        self.ownerId = dictionary["ownerId"]


class TeamStatDetail(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # AverageGamesPlayed
        self.averageGamesPlayed = dictionary["averageGamesPlayed"]

        # int # Losses
        self.losses = dictionary["losses"]

        # string # TeamStatType
        self.teamStatType = dictionary["teamStatType"]

        # int # Wins
        self.wins = dictionary["wins"]


class TeamMemberInfo(CassiopeiaDto):
    def __init__(self, dictionary):
        # long # Date that team member was invited to team specified as epoch milliseconds.
        self.inviteDate = dictionary["inviteDate"]

        # long # Date that team member joined team specified as epoch milliseconds.
        self.joinDate = dictionary["joinDate"]

        # long # PlayerId
        self.playerId = dictionary["playerId"]

        # string # Status
        self.status = dictionary["status"]