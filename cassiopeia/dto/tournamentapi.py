import cassiopeia.dto.requests
import cassiopeia.type.dto.tournament


def create_tournament_codes(tournament_id, parameters, count=1):
    """
    https://developer.riotgames.com/api/methods#!/1063

    Args:
        tournament_id (int): the tournament ID to generate codes for
        parameters (TournamentCodeParameters): the parameters for the tournament codes
        count (int): the number of codes to generate (max 1000) (default 1)

    Returns:
        list<str>: the created tournament codes
    """
    if count < 1 or count > 1000:
        raise ValueError("Count must be between 1 and 1000")
    request = "https://{server}.api.pvp.net/tournament/public/{version}/code".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"])

    query_params = {
        "tournamentId": tournament_id,
        "count": count
    }
    return cassiopeia.dto.requests.post(request, parameters, query_params, False, True)


def get_tournament_code(tournament_code):
    """
    https://developer.riotgames.com/api/methods#!/1057/3643

    Args:
        tournament_code (str): the tournament code to get information about

    Returns:
        TournamentCode: information about the tournament code
    """
    request = "https://{server}.api.pvp.net/tournament/public/{version}/code/{code}".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"], code=tournament_code)
    return cassiopeia.type.dto.tournament.TournamentCode(cassiopeia.dto.requests.get(request, include_base=False, tournament=True))


def update_tournament_code(tournament_code, parameters):
    """
    https://developer.riotgames.com/api/methods#!/1057/3647

    Args:
        tournament_code (str): the tournament code to update
        parameters (TournamentCodeUpdateParameters): the new parameters for the tournament code
    """
    request = "https://{server}.api.pvp.net/tournament/public/{version}/code/{code}".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"], code=tournament_code)
    cassiopeia.dto.requests.put(request, parameters, include_base=False, tournament=True)


def get_lobby_events(tournament_code):
    """
    https://developer.riotgames.com/api/methods#!/1057/3653

    Args:
        tournament_code (str): the tournament code to get lobby events for

    Returns:
        LobbyEventWrapper: the lobby events for that tournament code
    """
    request = "https://{server}.api.pvp.net/tournament/public/{version}/lobby/events/by-code/{code}".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"], code=tournament_code)
    return cassiopeia.type.dto.tournament.LobbyEventWrapper(cassiopeia.dto.requests.get(request, include_base=False, tournament=True))


def create_tournament_provider(parameters):
    """
    https://developer.riotgames.com/api/methods#!/1057/3646

    Args:
        parameters (ProviderRegistrationParameters): the parameters for the provider

    Returns:
        int: the provider ID
    """
    request = "https://{server}.api.pvp.net/tournament/public/{version}/provider".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"])
    return cassiopeia.dto.requests.post(request, parameters, include_base=False, tournament=True)


def create_tournament(parameters):
    """
    https://developer.riotgames.com/api/methods#!/1057/3649

    Args:
        parameters (TournamentRegistrationParameters): the parameters for the tournament

    Returns:
        int: the tournament ID
    """
    request = "https://{server}.api.pvp.net/tournament/public/{version}/tournament".format(server=cassiopeia.dto.requests.region, version=cassiopeia.dto.requests.api_versions["tournament"])
    return cassiopeia.dto.requests.post(request, parameters, include_base=False, tournament=True)
