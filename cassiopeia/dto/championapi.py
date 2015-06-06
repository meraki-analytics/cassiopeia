import cassiopeia.dto.requests
import cassiopeia.type.dto.champion

# @param id # int # The ID of the champion to look up
# @return # Champion # The champion
def get_champion_status(id_):
    request = "{version}/champion/{id_}".format(version=cassiopeia.dto.requests.api_versions["champion"], id_=id_)
    return cassiopeia.type.dto.champion.Champion(cassiopeia.dto.requests.get(request))

# @param freeToPlay # bool # Whether to only return free champions
# @return # list<Champion> # All champions
def get_champion_statuses(freeToPlay=False):
    request = "{version}/champion".format(version=cassiopeia.dto.requests.api_versions["champion"])
    return cassiopeia.type.dto.champion.ChampionList(cassiopeia.dto.requests.get(request, {"freeToPlay": freeToPlay}))