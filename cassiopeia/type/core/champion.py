import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.champion

class ChampionStatus(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.champion.Champion

    def __str__(self):
        return "Status ({champ})".format(champ=self.champion)

    @property
    def enabled(self):
        return self.data.active

    @property
    def custom_enabled(self):
        return self.data.botEnabled

    @property
    def coop_ai_enabled(self):
        return self.data.botMmEnabled

    @property
    def free(self):
        return self.data.freeToPlay

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_id(self.data.id) if self.data.id else None

    @property
    def ranked_enabled(self):
        return self.data.rankedPlayEnabled