import cassiopeia.type.dto.common
import cassiopeia.type.core.common


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
