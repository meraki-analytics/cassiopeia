from cassiopeia.dto import requests
from cassiopeia.type.dto.champion import *

# @param id # int # The ID of the champion to look up
# @return # Champion # The champion
def get_champion_status(id_):
    request = "{version}/champion/{id_}".format(version=requests.api_versions["champion"], id_=id_)
    return Champion(requests.get(request))

# @param freeToPlay # bool # Whether to only return free champions
# @return # list<Champion> # All champions
def get_champion_statuses(freeToPlay=False):
    request = "{version}/champion".format(version=requests.api_versions["champion"])
    return ChampionList(requests.get(request, {"freeToPlay": freeToPlay}))