from cassiopeia import requests
from cassiopeia.type.dto.match import *

# @param id_ # int # The ID of the match to get
# @return # MatchDetail # The match
def get_match(id_):
    request = "{version}/match/{id_}".format(version=requests.api_versions["match"], id_=id_)
    return MatchDetail(requests.get(request, {"includeTimeline": True}))