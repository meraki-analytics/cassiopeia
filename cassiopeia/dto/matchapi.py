import cassiopeia.dto.requests
import cassiopeia.type.dto.match

# @param id_ # int # The ID of the match to get
# @return # MatchDetail # The match
def get_match(id_):
    request = "{version}/match/{id_}".format(version=cassiopeia.dto.requests.api_versions["match"], id_=id_)
    return cassiopeia.type.dto.match.MatchDetail(cassiopeia.dto.requests.get(request, {"includeTimeline": True}))