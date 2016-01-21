import datetime

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.championmastery


@cassiopeia.type.core.common.inheritdocs
class ChampionMastery(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.championmastery.ChampionMastery

    def __str__(self):
        return "{champion} ({level})".format(self.champion, self.level)

    @property
    def champion(self):
        """Champion    champion for this entry"""
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def level(self):
        """int    champion level for specified player and champion combination"""
        return self.data.championLevel

    @property
    def points(self):
        """int    total number of champion points for this player and champion combination - they are used to determine champion_level"""
        return self.data.championPoints

    @property
    def points_since_last_level(self):
        """int    number of points earned since current level has been achieved. Zero if player reached maximum champion level for this champion."""
        return self.data.championPointsSinceLastLevel

    @property
    def points_until_next_level(self):
        """int    number of points needed to achieve next level. Zero if player reached maximum champion level for this champion."""
        return self.data.championPointsUntilNextLevel

    @property
    def chest_granted(self):
        """bool    is chest granted for this champion or not in current season"""
        return self.data.chestGranted

    @property
    def highest_grade(self):
        """str    the highest grade of this champion of current season"""
        return self.data.highestGrade

    @property
    def last_played(self):
        """datetime    last time this champion was played by this player"""
        return datetime.datetime.utcfromtimestamp(self.data.lastPlayTime / 1000) if self.data.lastPlayTime else None

    @property
    def summoner(self):
        """Summoner    the player this mastery information is for"""
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId) if self.data.playerId else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    ChampionMastery.dto_type = cassiopeia.type.dto.championmastery.ChampionMastery
