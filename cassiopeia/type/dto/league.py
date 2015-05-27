from cassiopeia.type.dto.common import CassiopeiaDto

class MiniSeries(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Number of current losses in the mini series.
        self.losses = dictionary["losses"]

        # string # String showing the current, sequential mini series progress where 'W' represents a win, 'L' represents a loss, and 'N' represents a game that hasn't been played yet.
        self.progress = dictionary["progress"]

        # int # Number of wins required for promotion.
        self.target = dictionary["target"]

        # int # Number of current wins in the mini series.
        self.wins = dictionary["wins"]


class LeagueEntry(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The league division of the participant.
        self.division = dictionary["division"]

        # boolean # Specifies if the participant is fresh blood.
        self.isFreshBlood = dictionary["isFreshBlood"]

        # boolean # Specifies if the participant is on a hot streak.
        self.isHotStreak = dictionary["isHotStreak"]

        # boolean # Specifies if the participant is inactive.
        self.isInactive = dictionary["isInactive"]

        # boolean # Specifies if the participant is a veteran.
        self.isVeteran = dictionary["isVeteran"]

        # int # The league points of the participant.
        self.leaguePoints = dictionary["leaguePoints"]

        # int # The number of losses for the participant.
        self.losses = dictionary["losses"]

        # MiniSeries # Mini series data for the participant. Only present if the participant is currently in a mini series.
        self.miniSeries = MiniSeries(dictionary["series"]) if not isinstance(dictionary["series"], MiniSeries) else dictionary["series"]

        # string # The ID of the participant (i.e., summoner or team) represented by this entry.
        self.playerOrTeamId = dictionary["playerOrTeamId"]

        # string # The name of the the participant (i.e., summoner or team) represented by this entry.
        self.playerOrTeamName = dictionary["playerOrTeamName"]

        # int # The number of wins for the participant.
        self.wins = dictionary["wins"]


class League(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<LeagueEntry> # The requested league entries.
        self.entries = [LeagueEntry(entry) if not isinstance(entry, LeagueEntry) else entry for entry in dictionary["entries"]]

        # string # This name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
        self.name = dictionary["name"]

        # string # Specifies the relevant participant that is a member of this league (i.e., a requested summoner ID, a requested team ID, or the ID of a team to which one of the requested summoners belongs). Only present when full league is requested so that participant's entry can be identified. Not present when individual entry is requested.
        self.participantId = dictionary["participantId"]

        # string # The league's queue type. (Legal values: RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5)
        self.queue = dictionary["queue"]

        # string # The league's tier. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE)
        self.tier = dictionary["tier"]