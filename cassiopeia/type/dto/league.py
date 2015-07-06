import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class MiniSeries(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MiniSeries"
    losses = sqlalchemy.Column(sqlalchemy.Integer)
    progress = sqlalchemy.Column(sqlalchemy.String)
    target = sqlalchemy.Column(sqlalchemy.Integer)
    wins = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _entry_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("LeagueEntry._id"))

    def __init__(self, dictionary):
        # int # Number of current losses in the mini series.
        self.losses = dictionary.get("losses", 0)

        # str # String showing the current, sequential mini series progress where 'W' represents a win, 'L' represents a loss, and 'N' represents a game that hasn't been played yet.
        self.progress = dictionary.get("progress", "")

        # int # Number of wins required for promotion.
        self.target = dictionary.get("target", 0)

        # int # Number of current wins in the mini series.
        self.wins = dictionary.get("wins", 0)


class LeagueEntry(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "LeagueEntry"
    division = sqlalchemy.Column(sqlalchemy.String)
    isFreshBlood = sqlalchemy.Column(sqlalchemy.Boolean)
    isHotStreak = sqlalchemy.Column(sqlalchemy.Boolean)
    isInactive = sqlalchemy.Column(sqlalchemy.Boolean)
    isVeteran = sqlalchemy.Column(sqlalchemy.Boolean)
    leaguePoints = sqlalchemy.Column(sqlalchemy.Integer)
    losses = sqlalchemy.Column(sqlalchemy.Integer)
    miniSeries = sqlalchemy.orm.relationship("MiniSeries", uselist=False)
    playerOrTeamId = sqlalchemy.Column(sqlalchemy.String)
    playerOrTeamName = sqlalchemy.Column(sqlalchemy.String)
    wins = sqlalchemy.Column(sqlalchemy.Integer)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    _league_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("League._id"))

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


class League(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "League"
    entries = sqlalchemy.orm.relationship("LeagueEntry", cascade="all, delete-orphan", passive_deletes=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    participantId = sqlalchemy.Column(sqlalchemy.String)
    queue = sqlalchemy.Column(sqlalchemy.String)
    tier = sqlalchemy.Column(sqlalchemy.String)
    _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, dictionary):
        # list<LeagueEntry> # The requested league entries.
        self.entries = [(LeagueEntry(entry) if not isinstance(entry, LeagueEntry) else entry) for entry in dictionary.get("entries", []) if entry]

        # str # This name is an internal place-holder name only. Display and localization of names in the game client are handled client-side.
        self.name = dictionary.get("name", "")

        # str # Specifies the relevant participant that is a member of this league (i.e., a requested summoner ID, a requested team ID, or the ID of a team to which one of the requested summoners belongs). Only present when full league is requested so that participant's entry can be identified. Not present when individual entry is requested.
        self.participantId = dictionary.get("participantId", "")

        # str # The league's queue type. (Legal values: RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5)
        self.queue = dictionary.get("queue", "")

        # str # The league's tier. (Legal values: CHALLENGER, MASTER, DIAMOND, PLATINUM, GOLD, SILVER, BRONZE)
        self.tier = dictionary.get("tier", "")

    @property
    def summoner_ids(self):
        ids = set()

        if(self.participantId): 
            try:
                id_ = int(self.data.participantId)
                ids.add(id_)
            except(ValueError):
                pass

        for entry in self.entries:
            if(entry.playerOrTeamId): 
                try:
                    id_ = int(entry.playerOrTeamId)
                    ids.add(id_)
                except(ValueError):
                    pass
        return ids

    @property
    def team_ids(self):
        ids = set()

        if(self.participantId): 
            try:
                int(self.participantId)
            except(ValueError):
                ids.add(self.participantId)

        for entry in self.entries:
            if(entry.playerOrTeamId):
                try:
                    int(entry.playerOrTeamId)
                except(ValueError):
                    ids.add(entry.playerOrTeamId)
        return ids