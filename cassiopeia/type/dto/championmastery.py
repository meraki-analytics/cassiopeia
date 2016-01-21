import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class ChampionMastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    championId                      int     Champion ID for this entry.
    championLevel                   int     Champion level for specified player and champion combination.
    championPoints                  int     Total number of champion points for this player and champion combination - they are used to determine championLevel.
    championPointsSinceLastLevel    int     Number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion.
    championPointsUntilNextLevel    int     Number of points needed to achieve next level. Zero if player reached maximum champion level for this champion.
    chestGranted                    bool    Is chest granted for this champion or not in current season.
    highestGrade                    str     The highest grade of this champion of current season.
    lastPlayTime                    int     Last time this champion was played by this player - in Unix milliseconds time format.
    playerId                        int     Player ID for this entry.
    """
    def __init__(self, dictionary):
        self.championId = dictionary.get("championId", 0)
        self.championLevel = dictionary.get("championLevel", "")
        self.championPoints = dictionary.get("championPoints", 0)
        self.championPointsSinceLastLevel = dictionary.get("championPointsSinceLastLevel", 0)
        self.championPointsUntilNextLevel = dictionary.get("championPointsUntilNextLevel", 0)
        self.chestGranted = dictionary.get("chestGranted", 0)
        self.highestGrade = dictionary.get("highestGrade", 0)
        self.lastPlayTime = dictionary.get("lastPlayTime", 0)
        self.playerId = dictionary.get("playerId", 0)


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_champion_mastery():
    global ChampionMastery

    @cassiopeia.type.core.common.inheritdocs
    class ChampionMastery(ChampionMastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ChampionMastery"
        championId = sqlalchemy.Column(sqlalchemy.BigInteger)
        championLevel = sqlalchemy.Column(sqlalchemy.Integer)
        championPoints = sqlalchemy.Column(sqlalchemy.Integer)
        championPointsSinceLastLevel = sqlalchemy.Column(sqlalchemy.BigInteger)
        championPointsUntilNextLevel = sqlalchemy.Column(sqlalchemy.BigInteger)
        chestGranted = sqlalchemy.Column(sqlalchemy.Boolean)
        highestGrade = sqlalchemy.Column(sqlalchemy.String(30))
        lastPlayTime = sqlalchemy.Column(sqlalchemy.BigInteger)
        playerId = sqlalchemy.Column(sqlalchemy.sqlalchemy.BigInteger, primary_key=True)


def _sa_bind_all():
    _sa_bind_champion_mastery()
