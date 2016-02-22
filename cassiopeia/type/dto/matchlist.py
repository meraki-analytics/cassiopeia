import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy


@cassiopeia.type.core.common.inheritdocs
class MatchList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        endIndex (int): the last match index from history returned
        matches (list<MatchReference>): list of matches from the player's history
        startIndex (int): the first match index from history returned
        totalGames (int): the number of games provided
    """
    def __init__(self, dictionary):
        self.endIndex = dictionary.get("endIndex", 0)
        self.matches = [(MatchReference(match) if not isinstance(match, MatchReference) else match) for match in dictionary.get("matches", []) if match]
        self.startIndex = dictionary.get("startIndex", 0)
        self.totalGames = dictionary.get("totalGames", 0)

    @property
    def champion_ids(self):
        """
        Gets all champion IDs contained in this object
        """
        ids = set()
        for m in self.matches:
            ids.add(m.champion)
        return ids


@cassiopeia.type.core.common.inheritdocs
class MatchReference(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all champion IDs contained in this object
    """
    def __init__(self, dictionary):
        self.champion = dictionary.get("champion", 0)
        self.lane = dictionary.get("lane", "")
        self.matchId = dictionary.get("matchId", 0)
        self.platformId = dictionary.get("platformId", "")
        self.queue = dictionary.get("queue", "")
        self.role = dictionary.get("role", "")
        self.season = dictionary.get("season", "")
        self.timestamp = dictionary.get("timestamp", 0)


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_match_reference():
    global MatchReference

    @cassiopeia.type.core.common.inheritdocs
    class MatchReference(MatchReference, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchReference"
        champion = sqlalchemy.Column(sqlalchemy.Integer)
        lane = sqlalchemy.Column(sqlalchemy.String(30))
        matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))
        queue = sqlalchemy.Column(sqlalchemy.String(30))
        role = sqlalchemy.Column(sqlalchemy.String(30))
        season = sqlalchemy.Column(sqlalchemy.String(30))
        timestamp = sqlalchemy.Column(sqlalchemy.BigInteger)


def _sa_bind_all():
    _sa_bind_match_reference()
