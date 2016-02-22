import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.team


@cassiopeia.type.core.common.inheritdocs
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
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @property
    def id(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return self.data.fullId

    @cassiopeia.type.core.common.lazyproperty
    def last_game(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.lastGameDate / 1000) if self.data.lastGameDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_join(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinDate / 1000) if self.data.lastJoinDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_queue(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinedRankedTeamQueueDate / 1000) if self.data.lastJoinedRankedTeamQueueDate else None

    @cassiopeia.type.core.common.lazyproperty
    def match_history(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return [MatchSummary(summary) for summary in self.data.matchHistory]

    @cassiopeia.type.core.common.lazyproperty
    def modify(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def name(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return self.data.name

    @property
    def captain(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.roster.ownerId)

    @property
    def roster(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return [TeamMember(member) for member in self.data.roster.memberList]

    @cassiopeia.type.core.common.lazyproperty
    def second_to_last_join(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.secondLastJoinDate / 1000) if self.data.secondLastJoinDate else None

    @property
    def status(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return self.data.status

    @property
    def tag(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return self.data.tag

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return [Stats(stats) for stats in self.data.teamStatDetails]

    @cassiopeia.type.core.common.lazyproperty
    def third_to_last_join(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return datetime.datetime.utcfromtimestamp(self.data.thirdLastJoinDate / 1000) if self.data.thirdLastJoinDate else None

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        """
        Returns:
            datetime: the creation date of the team
        """
        return cassiopeia.riotapi.get_leagues_by_team(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        """
        Returns:
            int: the team's id
        """
        return cassiopeia.riotapi.get_league_entries_by_team(self)


@cassiopeia.type.core.common.inheritdocs
class MatchSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.MatchHistorySummary

    def __str__(self):
        return "Match #{id_}".format(id_=self.id)

    @property
    def kda(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.assists

    @cassiopeia.type.core.common.lazyproperty
    def date(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return datetime.datetime.utcfromtimestamp(self.data.date / 1000) if self.data.date else None

    @property
    def deaths(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.deaths

    @property
    def id(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.gameId

    @property
    def mode(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def invalid(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.invalid

    @property
    def kills(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.kills

    @property
    def map(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def opponent_kills(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.opposingTeamKills

    @property
    def opponent(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.opposingTeamName

    @property
    def win(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return self.data.win

    @cassiopeia.type.core.common.immutablemethod
    def match(self):
        """
        Returns:
            datetime: the date and time for the team's last game in epoch milliseconds
        """
        return cassiopeia.riotapi.get_match(self.id)


@cassiopeia.type.core.common.inheritdocs
class Stats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamStatDetail

    def __str__(self):
        return "Stats ({q})".format(q=self.queue)

    @property
    def average_games_played(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return self.data.averageGamesPlayed

    @property
    def losses(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return self.data.losses

    @property
    def queue(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return cassiopeia.type.core.common.Queue(self.data.teamStatType) if self.data.teamStatType else None

    @property
    def wins(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return self.data.wins


@cassiopeia.type.core.common.inheritdocs
class TeamMember(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamMemberInfo

    def __str__(self):
        return str(self.summoner)

    @cassiopeia.type.core.common.lazyproperty
    def invite(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return datetime.datetime.utcfromtimestamp(self.data.inviteDate / 1000) if self.data.inviteDate else None

    @cassiopeia.type.core.common.lazyproperty
    def join(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return datetime.datetime.utcfromtimestamp(self.data.joinDate / 1000) if self.data.joinDate else None

    @property
    def summoner(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId)

    @property
    def status(self):
        """
        Returns:
            datetime: the date and time for when the most recent team member joined in epoch milliseconds
        """
        return self.data.status


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    Team.dto_type = cassiopeia.type.dto.team.Team
    MatchSummary.dto_type = cassiopeia.type.dto.team.MatchHistorySummary
    Stats.dto_type = cassiopeia.type.dto.team.TeamStatDetail
    TeamMember.dto_type = cassiopeia.type.dto.team.TeamMemberInfo
