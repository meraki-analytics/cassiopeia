import cassiopeia.dto.requests
import cassiopeia.type.dto.match

def get_match(id_):
    """https://developer.riotgames.com/api/methods#!/1014/3442

    id_       int            the ID of the match to get

    return    MatchDetail    the match
    """
    request = "{version}/match/{id_}".format(version=cassiopeia.dto.requests.api_versions["match"], id_=id_)
    return cassiopeia.type.dto.match.MatchDetail(cassiopeia.dto.requests.get(request, {"includeTimeline": True}))