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
        return datetime.datetime.utcfromtimestamp(self.data.createDate / 1000) if self.data.createDate else None

    @property
    def id(self):
        return self.data.fullId

    @cassiopeia.type.core.common.lazyproperty
    def last_game(self):
        return datetime.datetime.utcfromtimestamp(self.data.lastGameDate / 1000) if self.data.lastGameDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_join(self):
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinDate / 1000) if self.data.lastJoinDate else None

    @cassiopeia.type.core.common.lazyproperty
    def last_queue(self):
        return datetime.datetime.utcfromtimestamp(self.data.lastJoinedRankedTeamQueueDate / 1000) if self.data.lastJoinedRankedTeamQueueDate else None

    @cassiopeia.type.core.common.lazyproperty
    def match_history(self):
        return [MatchSummary(summary) for summary in self.data.matchHistory]

    @cassiopeia.type.core.common.lazyproperty
    def modify(self):
        return datetime.datetime.utcfromtimestamp(self.data.modifyDate / 1000) if self.data.modifyDate else None

    @property
    def name(self):
        return self.data.name

    @property
    def captain(self):
        return cassiopeia.riotapi.get_summoner_by_id(self.data.roster.ownerId)

    @property
    def roster(self):
        return [TeamMember(member) for member in self.data.roster.memberList]

    @cassiopeia.type.core.common.lazyproperty
    def second_to_last_join(self):
        return datetime.datetime.utcfromtimestamp(self.data.secondLastJoinDate / 1000) if self.data.secondLastJoinDate else None

    @property
    def status(self):
        return self.data.status

    @property
    def tag(self):
        return self.data.tag

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        return [Stats(stats) for stats in self.data.teamStatDetails]

    @cassiopeia.type.core.common.lazyproperty
    def third_to_last_join(self):
        return datetime.datetime.utcfromtimestamp(self.data.thirdLastJoinDate / 1000) if self.data.thirdLastJoinDate else None

    @cassiopeia.type.core.common.immutablemethod
    def leagues(self):
        return cassiopeia.riotapi.get_leagues_by_team(self)

    @cassiopeia.type.core.common.immutablemethod
    def league_entries(self):
        return cassiopeia.riotapi.get_league_entries_by_team(self)


class MatchSummary(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.MatchHistorySummary

    def __str__(self):
        return "Match #{id_}".format(id_=self.id)

    @property
    def kda(self):
        return (self.kills + self.assists) / (self.deaths if self.deaths else 1)

    @property
    def assists(self):
        return self.data.assists

    @cassiopeia.type.core.common.lazyproperty
    def date(self):
        return datetime.datetime.utcfromtimestamp(self.data.date / 1000) if self.data.date else None

    @property
    def deaths(self):
        return self.data.deaths

    @property
    def id(self):
        return self.data.gameId

    @property
    def mode(self):
        return cassiopeia.type.core.common.GameMode(self.data.gameMode) if self.data.gameMode else None

    @property
    def invalid(self):
        return self.data.invalid

    @property
    def kills(self):
        return self.data.kills

    @property
    def map(self):
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @property
    def opponent_kills(self):
        return self.data.opposingTeamKills

    @property
    def opponent(self):
        return self.data.opposingTeamName

    @property
    def win(self):
        return self.data.win

    @cassiopeia.type.core.common.immutablemethod
    def match(self):
        return cassiopeia.riotapi.get_match(self.id)


class Stats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamStatDetail

    def __str__(self):
        return "Stats ({q})".format(q=self.queue)

    @property
    def average_games_played(self):
        return self.data.averageGamesPlayed

    @property
    def losses(self):
        return self.data.losses

    @property
    def queue(self):
        return cassiopeia.type.core.common.Queue(self.data.teamStatType) if self.data.teamStatType else None

    @property
    def wins(self):
        return self.data.wins


class TeamMember(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.team.TeamMemberInfo

    def __str__(self):
        return str(self.summoner)

    @cassiopeia.type.core.common.lazyproperty
    def invite(self):
        return datetime.datetime.utcfromtimestamp(self.data.inviteDate / 1000) if self.data.inviteDate else None

    @cassiopeia.type.core.common.lazyproperty
    def join(self):
        return datetime.datetime.utcfromtimestamp(self.data.joinDate / 1000) if self.data.joinDate else None

    @property
    def summoner(self):
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId)

    @property
    def status(self):
        return self.data.status