from cassiopeia.type.dto.common import CassiopeiaDto

class MiniSeries(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Number of current losses in the mini series.
        self.losses = dictionary.get("losses", 0)

        # str # String showing the current, sequential mini series progress where 'W' represents a win, 'L' represents a loss, and 'N' represents a game that hasn't been played yet.
        self.progress = dictionary.get("progress", "")

        # int # Number of wins required for promotion.
        self.target = dictionary.get("target", 0)

        # int # Number of current wins in the mini series.
        self.wins = dictionary.get("wins", 0)


class LeagueEntry(CassiopeiaDto):
    def __init__(self, dictionary):
        # str # The league division of the participant.
        self.division = dictionary.get("division", "")

        # bool # Specifies if the participant is fresh blood.
        self.isFreshBlood = dictionary.get("isFreshBlood", False)

        # bool # Specifies if the participant is on a hot streak.
        self.isHotStreak = dictionary.get("isHotStreak", False)

        # bool # Specifies if the participant is inactive.
        self.isInactive = dictionary.get("isInactive", False)

        # bool # Specifies if the participant is a veteran.
        self.isVeteran = dictionary.get("isVeteran", False)

        # int # The league points of the participant.
        self.leaguePoints = dictionary.get("leaguePoints", 0)

        # int # The number of losses for the participant.
        self.losses = dictionary.get("losses", 0)

        # MiniSeries # Mini series data for the participant. Only present if the participant is currently in a mini series.
        val = dictionary.get("series", None)
        self.miniSeries = MiniSeries(val) if val and not isinstance(val, MiniSeries) else val

        # str # The ID of the participant (i.e., summoner or team) represented by this entry.
        self.playerOrTeamId = dictionary.get("playerOrTeamId", "")

        # str # The name of the the participant (i.e., summoner or team) represented by this entry.
        self.playerOrTeamName = dictionary.get("playerOrTeamName", "")

        # int # The number of wins for the participant.
        self.wins = dictionary.get("wins", 0)


class League(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<LeagueEntry> # The requested league entries.
        self.entries = [LeagueEntry(entry) if not isinstance(entry, LeagueEntry) else entry for entry in dictionary.get("entries", [])]

        # str # This name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
        self.name = dictionary.get("name", "")

        # str # Specifies the relevant participant that is a member of this league (i.e., a requested summoner ID, a requested team ID, or the ID of a team to which one of the requested summoners belongs). Only present when full league is requested so that participant's entry can be identified. Not present when individual entry is requested.
        self.participantId = dictionary.get("participantId", "")

        # str # The league's queue type. (Legal values: RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5)
        self.queue = dictionary.get("queue", "")

        # str # The league's tier. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE)
        self.tier = dictionary.get("tier", "")