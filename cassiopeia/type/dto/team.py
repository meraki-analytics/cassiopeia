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
        self.memberList = [(TeamStatDetail(ts) if not isinstance(ts, TeamStatDetail) else ts) for ts in dictionary.get("memberList", []) if ts]

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