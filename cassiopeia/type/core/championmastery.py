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
        """
        Returns:
            Champion: champion for this entry
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.championId) if self.data.championId else None

    @property
    def level(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.championLevel

    @property
    def points(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.championPoints

    @property
    def points_since_last_level(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.championPointsSinceLastLevel

    @property
    def points_until_next_level(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.championPointsUntilNextLevel

    @property
    def chest_granted(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.chestGranted

    @property
    def highest_grade(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return self.data.highestGrade

    @property
    def last_played(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return datetime.datetime.utcfromtimestamp(self.data.lastPlayTime / 1000) if self.data.lastPlayTime else None

    @property
    def summoner(self):
        """
        Returns:
            Champion: champion for this entry
        """
        return cassiopeia.riotapi.get_summoner_by_id(self.data.playerId) if self.data.playerId else None


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    ChampionMastery.dto_type = cassiopeia.type.dto.championmastery.ChampionMastery
