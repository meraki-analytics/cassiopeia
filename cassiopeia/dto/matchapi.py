import cassiopeia.dto.requests
import cassiopeia.type.dto.match


def get_match(id_, include_timeline=True, tournament_code=""):
    """
    https://developer.riotgames.com/api/methods#!/1014/3442

    Args:
        id_ (int): the ID of the match to get
        include_timeline (bool): whether to include timeline data in the returned match
        tournament_code (str): the tournament code if the match to be retrieved is from a tournament

    Returns:
        MatchDetail: the match
    """
    request = "{version}/match/for-tournament/{id_}" if tournament_code else "{version}/match/{id_}"
    request = request.format(version=cassiopeia.dto.requests.api_versions["match"], id_=id_)

    params = {"includeTimeline": include_timeline}
    if tournament_code:
        params["tournamentCode"] = tournament_code

    return cassiopeia.type.dto.match.MatchDetail(cassiopeia.dto.requests.get(request, params, tournament=bool(tournament_code)))


def get_tournament_match_ids(tournament_code):
    """
    https://developer.riotgames.com/api/methods#!/1058/3656

    Args:
        tournament_code (str): the tournament code

    Returns:
        list<int>: the match ids for the tournament
    """
    request = "{version}/match/by-tournament/{tournament_code}/ids".format(version=cassiopeia.dto.requests.api_versions["match"], tournament_code=tournament_code)
    return cassiopeia.dto.requests.get(request, tournament=True)
