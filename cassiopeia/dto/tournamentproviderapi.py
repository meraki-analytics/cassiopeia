import cassiopeia.dto.requests
import cassiopeia.type.dto.tournament

BASE_URL = 'https://global.api.pvp.net/tournament/public/{version}/'


def get_tournament_code(code):
    """ Gets the details of a tournament code
    :param code:
    :return: Code information
    """
    request = (BASE_URL + "code/{code}").format(
            code=code,
            version=cassiopeia.dto.requests.api_versions["tournamentprovider"])

    return cassiopeia.type.dto.tournament.TournamentCode(
            cassiopeia.dto.requests.get(request, include_base=False, tournament=True, key_in_header=True))


def create_tournament_code(tournament_id, team_size=5, spectator_type='ALL', pick_type='TOURNAMENT_DRAFT',
                           map_type='SUMMONERS_RIFT', allowed_summoner_ids=[], metadata=''):
    """ Creates a single tournament code
    :param tournament_id:
    :param team_size:
    :param spectator_type: Any value of the SpectatorType enum
    :param pick_type: Any value of the PickType enum
    :param map_type: Any value of the Map enum
    :param allowed_summoner_ids: List of allowed summoner ids, or false-evaluating value for no restrictions
    :param metadata: Custom string that will be passed back to the callback url
    :return: Generated code
    """
    return create_tournament_codes(tournament_id, team_size, spectator_type, pick_type,
                                   map_type, allowed_summoner_ids, metadata)[0]


def create_tournament_codes(tournament_id, team_size=5, spectator_type='ALL', pick_type='TOURNAMENT_DRAFT',
                            map_type='SUMMONERS_RIFT', allowed_summoner_ids=[], metadata='', count=1):
    """ Creates some tournament codes with the following parameters
    :param tournament_id:
    :param team_size:
    :param spectator_type: Any value of the SpectatorType enum
    :param pick_type: Any value of the PickType enum
    :param map_type: Any value of the Map enum
    :param allowed_summoner_ids: List of allowed summoner ids, or false-evaluating value for no restrictions
    :param metadata: Custom string that will be passed back to the callback url
    :param count: How many codes to generate
    :return: List of generated codes
    """
    payload = cassiopeia.type.dto.tournament.TournamentCodeParameters(
        team_size, spectator_type, pick_type, map_type, allowed_summoner_ids, metadata).to_json()
    params = {
        'tournamentId': tournament_id,
        'count': count
    }
    request = (BASE_URL + "code").format(version=cassiopeia.dto.requests.api_versions["tournamentprovider"])
    return cassiopeia.dto.requests.post(
            request, params=params, data=payload, include_base=False, tournament=True, key_in_header=True)


def update_tournament_code(code, spectator_type, pick_type, map_type, allowed_summoner_ids):
    """ Creates a single tournament code
    :param code: Tournament code to update
    :param spectator_type: Any value of the SpectatorType enum
    :param pick_type: Any value of the PickType enum
    :param map_type: Any value of the Map enum
    :param allowed_summoner_ids: List of allowed summoner ids, or false-evaluating value for no restrictions
    """
    payload = cassiopeia.type.dto.tournament.TournamentCodeUpdateParameters(
            allowed_summoner_ids, spectator_type, pick_type, map_type).to_json()
    request = (BASE_URL + "code/{code}").format(
            code=code,
            version=cassiopeia.dto.requests.api_versions["tournamentprovider"])
    return cassiopeia.dto.requests.put(
            request, data=payload, include_base=False, tournament=True, key_in_header=True)


def get_lobby_events_by_code(code):
    """ Gets the list of lobby events for the given code
    :param code: Tournament code
    :return: Event list
    """
    request = (BASE_URL + "lobby/events/by-code/{code}").format(
            code=code,
            version=cassiopeia.dto.requests.api_versions["tournamentprovider"])

    return cassiopeia.type.dto.tournament.LobbyEventWrapper(
            cassiopeia.dto.requests.get(request, include_base=False, tournament=True, key_in_header=True))


def create_tournament_provider(callback_url):
    """ Creates a new tournament provider
    :param callback_url: Address that the servers will send the data back to. Must be on port 80 or 443!
    :return: Provider id
    """
    request = (BASE_URL + "provider").format(version=cassiopeia.dto.requests.api_versions["tournamentprovider"])
    payload = cassiopeia.type.dto.tournament.ProviderRegistrationParameters(
            cassiopeia.dto.requests.region.upper(), callback_url).to_json()
    return cassiopeia.dto.requests.post(request, data=payload, include_base=False, tournament=True, key_in_header=True)


def create_tournament(provider_id, name):
    """ Creates a tournament for the given provider
    :param provider_id: Provider id, to be obtained via create_tournament_provider (once)
    :param name: Tournament name
    :return: Tournament id
    """
    request = (BASE_URL + "tournament").format(version=cassiopeia.dto.requests.api_versions["tournamentprovider"])
    payload = cassiopeia.type.dto.tournament.TournamentRegistrationParameters(provider_id, name).to_json()
    return cassiopeia.dto.requests.post(request, data=payload, include_base=False, tournament=True, key_in_header=True)