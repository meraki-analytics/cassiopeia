from cassiopeia.type.core.common import CassiopeiaObject, Queue, Tier, Divison, lazyproperty

class Series(CassiopeiaObject):
    def __str__(self):
        return progress

    # int # Number of current losses in the series.
    @property
    def losses(self):
        return self.data.losses

    # str # String showing the current, sequential mini series progress where 'W' represents a win, 'L' represents a loss, and 'N' represents a game that hasn't been played yet.
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


class Entry(CassiopeiaObject):
    def __str__(self):
        return "{player} ({lp} LP)".format(player=self.player_name, lp=self.league_points)

    # Division # The league division of the participant.
    @property
    def divison(self):
        return Division(self.data.division) if self.data.division else None

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
    @lazyproperty
    def series(self):
        return Series(self.data.miniSeries) if self.data.miniSeries else None

    # int # The ID of the summoner represented by this entry. 0 if this entry is for a team.
    @property
    def player_id(self):
        try:
            return int(self.data.playerOrTeamId)
        except(ValueError):
            return 0

    # str # The ID of the team represented by this entry. "" if this entry is for a summoner.
    @property
    def team_id(self):
        try:
            int(self.data.playerOrTeamId)
            return ""
        except(ValueError):
            return self.data.playerOrTeamId

    # str # The name of the summoner represented by this entry. "" if this entry is for a team. 
    @property
    def player_name(self):
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


class League(CassiopeiaObject):
    def __str__(self):
        return "{name} ({tier})".format(name=self.name, tier=self.tier)

    def __iter__(self):
        return iter(self.entries)

    # list<Entry> # The requested league entries, sorted by LP.
    @lazyproperty
    def entries(self):
        return sorted([Entry(entry) for entry in self.data.entries], key=lambda entry: entry.league_points, reverse=True)

    # str # This name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
    @property
    def name(self):
        return self.data.name

    # int # Specifies the relevant summoner that is a member of this league. Only present when full league is requested so that participant's entry can be identified. 0 when individual entry is requested or the participant is a team.
    @property
    def player_id(self):
        try:
            return int(self.data.participantId)
        except(ValueError):
            return 0

    # str # Specifies the relevant team that is a member of this league. Only present when full league is requested so that participant's entry can be identified. "" when individual entry is requested or the participant is a summoner.
    @property
    def team_id(self):
        try:
            int(self.data.participantId)
            return ""
        except(ValueError):
            return self.data.participantId

    # Queue # The league's queue type.
    @property
    def queue(self):
        return Queue(self.data.queue) if self.data.queue else None

    # Tier # The league's tier.
    @property
    def tier(self):
        return Tier(self.data.tier) if self.data.tier else None