import cassiopeia.riotapi
import cassiopeia.type.core.common

class Series(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return progress

    # int # Number of current losses in the series.
    @property
    def losses(self):
        return self.data.losses

    # str # String showing the current, sequential mini series progress where 'W' represents a win, 'L' epresents a loss, and 'N' represents a game that hasn't been played yet.
    @property
    def progress(self):
        return self.data.progress

    # int # Number of wins required for promotion.
    @property
    def target(self):
        return self.data.target

    # int # Number of current wins in the series.
    @property
    def wins(self):
        return self.data.wins


class Entry(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "{player} ({lp} LP)".format(player=self.player_name, lp=self.league_points)

    # cassiopeia.type.core.common.Division # The league division of the participant.
    @property
    def division(self):
        return cassiopeia.type.core.common.Division(self.data.division) if self.data.division else None

    # bool # Specifies if the participant is fresh blood.
    @property
    def fresh_blood(self):
        return self.data.isFreshBlood

    # bool # Specifies if the participant is on a hot streak.
    @property
    def hot_streak(self):
        return self.data.isHotStreak

    # bool # Specifies if the participant is inactive.
    @property
    def inactive(self):
        return self.data.isInactive

    # bool # Specifies if the participant is a veteran.
    @property
    def veteran(self):
        return self.data.isVeteran

    # int # The league points of the participant.
    @property
    def league_points(self):
        return self.data.leaguePoints

    # int # The number of losses for the participant.
    @property
    def losses(self):
        return self.data.losses

    # Series # Series data for the participant. Only present if the participant is currently in a mini series.
    @cassiopeia.type.core.common.lazyproperty
    def series(self):
        return Series(self.data.miniSeries) if self.data.miniSeries else None

    # Summoner # The summoner represented by this entry. None if this entry is for a team.
    @cassiopeia.type.core.common.lazyproperty
    def player(self):
        if(not self.data.playerOrTeamId):
            return None

        try:
            id_ = int(self.data.playerOrTeamId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except(ValueError):
            return None

    # Team # The team represented by this entry. None if this entry is for a summoner.
    @cassiopeia.type.core.common.lazyproperty
    def team(self):
        if(not self.data.playerOrTeamId):
            return None

        try:
            int(self.data.playerOrTeamId)
            return None
        except(ValueError):
            return cassiopeia.riotapi.get_team_by_id(self.data.playerOrTeamId)

    # str # The name of the summoner represented by this entry. "" if this entry is for a team. 
    @property
    def player_name(self):
        if(not self.data.playerOrTeamId):
            return ""

        try:
            int(self.data.playerOrTeamId)
            return self.data.playerOrTeamName
        except(ValueError):
            return ""

    # str # The name of the team represented by this entry. "" if this entry is for a summoner.
    @property
    def team_name(self):
        try:
            int(self.data.playerOrTeamId)
            return ""
        except(ValueError):
            return self.data.playerOrTeamName

    # int # The number of wins for the participant.
    @property
    def wins(self):
        return self.data.wins


class League(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "{name} ({tier})".format(name=self.name, tier=self.tier)

    def __iter__(self):
        return iter(self.entries)

    # list<Entry> # The requested league entries, sorted by LP.
    @cassiopeia.type.core.common.lazyproperty
    def entries(self):
        return sorted([Entry(entry) for entry in self.data.entries], key=lambda entry: entry.league_points, reverse=True)

    # str # This name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
    @property
    def name(self):
        return self.data.name

    # Entry # The entry for the relevant team or summoner that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested.
    @cassiopeia.type.core.common.lazyproperty
    def participant_entry(self):
        for entry in self.entries:
            if(entry.data.playerOrTeamId == self.data.participantId):
                return entry
        return None

    # Summoner # The relevant summoner that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested or the participant is a team.
    @cassiopeia.type.core.common.lazyproperty
    def player(self):
        if(not self.data.participantId):
            return None

        try:
            id_ = int(self.data.participantId)
            return cassiopeia.riotapi.get_summoner_by_id(id_)
        except(ValueError):
            return None

    # Team # The relevant team that is a member of this league. Only present when full league is requested so that participant's entry can be identified. None when individual entry is requested or the participant is a summoner.
    @cassiopeia.type.core.common.lazyproperty
    def team(self):
        if(not self.data.participantId):
            return None

        try:
            int(self.data.participantId)
            return None
        except(ValueError):
            return cassiopeia.riotapi.get_team_by_id(self.data.participantId)

    # cassiopeia.type.core.common.Queue # The league's queue type.
    @property
    def queue(self):
        return cassiopeia.type.core.common.Queue(self.data.queue) if self.data.queue else None

    # cassiopeia.type.core.common.Tier # The league's tier.
    @property
    def tier(self):
        return cassiopeia.type.core.common.Tier(self.data.tier) if self.data.tier else None