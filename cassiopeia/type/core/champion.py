import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.champion


@cassiopeia.type.core.common.inheritdocs
class ChampionStatus(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.champion.Champion

    def __str__(self):
        return "Status ({champ})".format(champ=self.champion)

    @property
    def enabled(self):
        """
        Returns:
            bool: whether the champion is currently enabled
        """
        return self.data.active

    @property
    def custom_enabled(self):
        """
        Returns:
            bool: whether the champion is currently enabled for custom games
        """
        return self.data.botEnabled

    @property
    def coop_ai_enabled(self):
        """
        Returns:
            bool: whether the champion is currently enabled for coop vs ai games
        """
        return self.data.botMmEnabled

    @property
    def free(self):
        """
        Returns:
            bool: whether the champion is currently free this week
        """
        return self.data.freeToPlay

    @property
    def champion(self):
        """
        Returns:
            Champion: the Champion this status is for
        """
        return cassiopeia.riotapi.get_champion_by_id(self.data.id) if self.data.id else None

    @property
    def ranked_enabled(self):
        """
        Returns:
            bool: whether the champion is currently enabled for ranked games
        """
        return self.data.rankedPlayEnabled


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    ChampionStatus.dto_type = cassiopeia.type.dto.champion.Champion
