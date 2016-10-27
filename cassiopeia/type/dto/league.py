import cassiopeia.type.dto.common
import cassiopeia.type.core.common


@cassiopeia.type.core.common.inheritdocs
class MiniSeries(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        losses (int): number of current losses in the mini series
        progress (str): string showing the current, sequential mini series progress where 'W' represents a win, 'L' represents a loss, and 'N' represents a game that hasn't been played yet
        target (int): number of wins required for promotion
        wins (int): number of current wins in the mini series
    """
    def __init__(self, dictionary):
        self.losses = dictionary.get("losses", 0)
        self.progress = dictionary.get("progress", "")
        self.target = dictionary.get("target", 0)
        self.wins = dictionary.get("wins", 0)


@cassiopeia.type.core.common.inheritdocs
class LeagueEntry(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        division (str): the league division of the participant
        isFreshBlood (bool): specifies if the participant is fresh blood
        isHotStreak (bool): specifies if the participant is on a hot streak
        isInactive (bool): specifies if the participant is inactive
        isVeteran (bool): specifies if the participant is a veteran
        leaguePoints (int): the league points of the participant
        losses (int): the number of losses for the participant
        miniSeries (MiniSeries): mini series data for the participant. Only present if the participant is currently in a mini series.
        playerOrTeamId (str): the ID of the participant (i.e., summoner or team) represented by this entry
        playerOrTeamName (str): the name of the the participant (i.e., summoner or team) represented by this entry
        wins (int): the number of wins for the participant
    """
    def __init__(self, dictionary):
        self.division = dictionary.get("division", "")
        self.isFreshBlood = dictionary.get("isFreshBlood", False)
        self.isHotStreak = dictionary.get("isHotStreak", False)
        self.isInactive = dictionary.get("isInactive", False)
        self.isVeteran = dictionary.get("isVeteran", False)
        self.leaguePoints = dictionary.get("leaguePoints", 0)
        self.losses = dictionary.get("losses", 0)
        val = dictionary.get("miniSeries", None)
        self.miniSeries = MiniSeries(val) if val and not isinstance(val, MiniSeries) else val
        self.playerOrTeamId = dictionary.get("playerOrTeamId", "")
        self.playerOrTeamName = dictionary.get("playerOrTeamName", "")
        self.wins = dictionary.get("wins", 0)


@cassiopeia.type.core.common.inheritdocs
class League(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        entries (list<LeagueEntry>): the requested league entries
        name (str): this name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
        participantId (str): specifies the relevant participant that is a member of this league (i.e., a requested summoner ID, a requested team ID, or the ID of a team to which one of the requested summoners belongs). Only present when full league is requested so that participant's entry can be identified. Not present when individual entry is requested.
        queue (str): the league's queue type (Legal values: RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5)
        tier (str): the league's tier (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE)
    """
    def __init__(self, dictionary):
        self.entries = [(LeagueEntry(entry) if not isinstance(entry, LeagueEntry) else entry) for entry in dictionary.get("entries", []) if entry]
        self.name = dictionary.get("name", "")
        self.participantId = dictionary.get("participantId", "")
        self.queue = dictionary.get("queue", "")
        self.tier = dictionary.get("tier", "")

    @property
    def summoner_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()

        if self.participantId:
            try:
                id_ = int(self.participantId)
                ids.add(id_)
            except ValueError:
                pass

        for entry in self.entries:
            if entry.playerOrTeamId:
                try:
                    id_ = int(entry.playerOrTeamId)
                    ids.add(id_)
                except ValueError:
                    pass
        return ids

    @property
    def team_ids(self):
        """
        Gets all summoner IDs contained in this object
        """
        ids = set()

        if self.participantId:
            try:
                int(self.participantId)
            except ValueError:
                ids.add(self.participantId)

        for entry in self.entries:
            if entry.playerOrTeamId:
                try:
                    int(entry.playerOrTeamId)
                except ValueError:
                    ids.add(entry.playerOrTeamId)
        return ids
