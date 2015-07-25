import sqlalchemy

import cassiopeia.type.dto.common

class MatchList(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # int # The last match index from history returned
        self.endIndex = dictionary.get("endIndex", 0)

        # list<MatchReference> # List of matches from the player's history
        self.matches = [(MatchReference(match) if not isinstance(match, MatchReference) else match) for match in dictionary.get("matches", []) if match]

        # int # The first match index from history returned
        self.startIndex = dictionary.get("startIndex", 0)

        # int # The number of games provided
        self.totalGames = dictionary.get("totalGames", 0)

    @property
    def champion_ids(self):
        ids = set()
        for m in self.matches:
            ids.add(m.champion)
        return ids


class MatchReference(cassiopeia.type.dto.common.CassiopeiaDto, cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "MatchReference"
    champion = sqlalchemy.Column(sqlalchemy.Integer)
    lane = sqlalchemy.Column(sqlalchemy.String(30))
    matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    platformId = sqlalchemy.Column(sqlalchemy.String(30))
    queue = sqlalchemy.Column(sqlalchemy.String(30))
    role = sqlalchemy.Column(sqlalchemy.String(30))
    season = sqlalchemy.Column(sqlalchemy.String(30))
    timestamp = sqlalchemy.Column(sqlalchemy.BigInteger)

    def __init__(self, dictionary):
        # int # The target player's champion ID
        self.champion = dictionary.get("champion", 0)

        # str # The lane that the player played in. Legal values: MID, MIDDLE, TOP, JUNGLE, BOT, BOTTOM
        self.lane = dictionary.get("lane", "")

        # int # The match ID
        self.matchId = dictionary.get("matchId", 0)

        # str # The platform the match was played on
        self.platformId = dictionary.get("platformId", "")

        # str # The queue of the match. Legal values: RANKED_SOLO_5x5, RANKED_TEAM_3x3, RANKED_TEAM_5x5
        self.queue = dictionary.get("queue", "")

        # str # The role that the player played. Legal values: DUO, NONE, SOLO, DUO_CARRY, DUO_SUPPORT
        self.role = dictionary.get("role", "")

        # str # The season the match was played in. Legal values: PRESEASON3, SEASON3, PRESEASON2014, SEASON2014, PRESEASON2015, SEASON2015
        self.season = dictionary.get("season", "")

        # int # The timestamp for the match
        self.timestamp = dictionary.get("timestamp", 0)