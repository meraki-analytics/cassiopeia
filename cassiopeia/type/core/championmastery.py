import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.championmastery


@cassiopeia.type.core.common.inheritdocs
class ChampionMastery(cassiopeia.type.core.common.CassiopeiaObject):
    """
    champion                            Champion    Champion for this entry.
    champion_level                      int         Champion level for specified player and champion combination.
    champion_points                     int         Total number of champion points for this player and champion combination - they are used to determine championLevel.
    champion_points_since_last_level    int         Number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion.
    champion_points_until_next_level    int         Number of points needed to achieve next level. Zero if player reached maximum champion level for this champion.
    chest_granted                       bool        Is chest granted for this champion or not in current season.
    highest_grade                       str         The highest grade of this champion of current season.
    last_play_time                      int         Last time this champion was played by this player - in Unix milliseconds time format.
    summoner                            Summoner    Summoner for this entry.
    """
    dto_type = cassiopeia.type.dto.championmastery.ChampionMastery

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def champion_level(self):
        return self.data.championLevel

    @property
    def champion_points(self):
        return self.data.championPoints

    @property
    def champion_points_since_next_level(self):
        return self.data.championPointsSinceLastLevel

    @property
    def champion_points_until_next_level(self):
        return self.data.championPointsUntilNextLevel

    @property
    def chest_granted(self):
        return self.data.chestGranted

    @property
    def highest_grade(self):
        return self.data.highestGrade

    @property
    def last_play_time(self):
        return self.data.lastPlayTime

    @property
    def summoner(self):
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId) if self.data.playerId else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    ChampionMastery.dto_type = cassiopeia.type.dto.championmastery.ChampionMastery
