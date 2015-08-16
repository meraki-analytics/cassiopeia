import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.team

class Team(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.Team

    def __str__(self):
        return self.name

    def __iter__(self):
        return iter(self.roster)

    def __len__(self):
        return len(self.roster)

    def __getitem__(self, index):
        return self.roster[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @cassiopeia.type.core.common.lazyproperty
    def creation(self):
        """The creation date of the team"""
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @property
    def id(self):
        """The team's ID"""
        return self.data.fullId

    @cassiopeia.type.core.common.lazyproperty
    def last_game(self):
        """The date and time for the team's last game in epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.lastGameDate / 1000) if self.data.lastGameDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_join(self):
        """The date and time for when the most recent team member joined in epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinDate / 1000) if self.data.lastJoinDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_queue(self):
        """The date the team last joined the ranked team queue in epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinedRankedTeamQueueDate / 1000) if self.data.lastJoinedRankedTeamQueueDate else None

    @cassiopeia.type.core.common.lazyproperty
    def match_history(self):
        """The match history of the team"""
        return [MatchSummary(summary) for summary in self.data.matchHistory]

    @cassiopeia.type.core.common.lazyproperty
    def modify(self):
        """The date that team was last modified specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def name(self):
        """The name of the team"""
        return self.data.name

    @property
    def captain(self):
        """The captain of the team (returns a Summoner)"""
        return cassiopeia.riotapi.get_summoner_by_id(self.data.roster.ownerId)

    @property
    def roster(self):
        """A list of the team members"""
        return [TeamMember(member) for member in self.data.roster.memberList]

    @cassiopeia.type.core.common.lazyproperty
    def second_to_last_join(self):
        """The date the second to last member joined specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.secondLastJoinDate / 1000) if self.data.secondLastJoinDate else None

    @property
    def status(self):
        """The status of the team"""
        return self.data.status

    @property
    def tag(self):
        """The team's tag"""
        return self.data.tag

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """The team's Stats"""
        return [Stats(stats) for stats in self.data.teamStatDetails]

    @cassiopeia.type.core.common.lazyproperty
    def third_to_last_join(self):
        """The date the third to last member joined specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.thirdLastJoinDate / 1000) if self.data.thirdLastJoinDate else None

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        """The team's League"""
        return cassiopeia.riotapi.get_leagues_by_team(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        """The team's league Entries"""
        return cassiopeia.riotapi.get_league_entries_by_team(self)


class MatchSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.MatchHistorySummary

    def __str__(self):
        return "Match #{id_}".format(id_=self.id)

    @property
    def kda(self):
        """The participant's kda"""
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        """The number of assists the team had"""
        return self.data.assists

    @cassiopeia.type.core.common.lazyproperty
    def date(self):
        """The date that match was completed specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.date / 1000) if self.data.date else None

    @property
    def deaths(self):
        """The number of deaths the team had"""
        return self.data.deaths

    @property
    def id(self):
        """The team's ID"""
        return self.data.gameId

    @property
    def mode(self):
        """The game Mode of the match"""
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def invalid(self):
        """Whether or not the data is valid?"""
        return self.data.invalid

    @property
    def kills(self):
        """The number of kills the team had"""
        return self.data.kills

    @property
    def map(self):
        """The map that the game was played on"""
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def opponent_kills(self):
        """The number of kills that the opponent had"""
        return self.data.opposingTeamKills

    @property
    def opponent(self):
        """The name of the opposing team"""
        return self.data.opposingTeamName

    @property
    def win(self):
        """Whether or not the team won this match"""
        return self.data.win

    @cassiopeia.type.core.common.immutablemethod
    def match(self):
        """Gets the full Match information for this match"""
        return cassiopeia.riotapi.get_match(self.id)


class Stats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamStatDetail

    def __str__(self):
        return "Stats ({q})".format(q=self.queue)

    @property
    def average_games_played(self):
        """The average number of games played"""
        return self.data.averageGamesPlayed

    @property
    def losses(self):
        """The number of times this team has lost"""
        return self.data.losses

    @property
    def queue(self):
        """The Queue type that these stats were aggregated for"""
        return cassiopeia.type.core.common.Queue(self.data.teamStatType) if self.data.teamStatType else None

    @property
    def wins(self):
        """The number of times this team has won"""
        return self.data.wins


class TeamMember(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamMemberInfo

    def __str__(self):
        return str(self.summoner)

    @cassiopeia.type.core.common.lazyproperty
    def invite(self):
        "The date that team member was invited to team specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.inviteDate / 1000) if self.data.inviteDate else None

    @cassiopeia.type.core.common.lazyproperty
    def join(self):
        "The date that team member joined the team specified as epoch milliseconds"""
        return datetime.datetime.utcfromtimestamp(self.data.joinDate / 1000) if self.data.joinDate else None

    @property
    def summoner(self):
        """The Summoner associated with this TeamMember"""
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId)

    @property
    def status(self):
        """The status of the TeamMember"""
        return self.data.status

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Team.dto_type = cassiopeia.type.dto.team.Team
    MatchSummary.dto_type = cassiopeia.type.dto.team.MatchHistorySummary
    Stats.dto_type = cassiopeia.type.dto.team.TeamStatDetail
    TeamMember.dto_type = cassiopeia.type.dto.team.TeamMemberInfo
