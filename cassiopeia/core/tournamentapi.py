import cassiopeia.dto.tournamentapi
import cassiopeia.type.core.tournament
import cassiopeia.type.dto.tournament


def create_tournament_codes(tournament_id, team_size, spectator_type, pick_type, map_type, allowed_summoners=[], meta_data="", count=1):
    """
    Creates tournament codes for a tournament

    Args:
        tournament_id (int): the tournament ID to generate codes for
        team_size (int): the team size for the tournament (1-5)
        spectator_type (str | SpectatorType): the spectator availability for the tournament
        pick_type (str | PickType): the pick type for the tournament
        map_type (str | MapType): the map the tournament is played on
        allowed_summoners (list<Summoner>): the summoners who are allowed to participate in the tournament (default [])
        meta_data (str | object): meta data to be included with the tournament. Any non-string value will be cast to a string. (default "")
        count (int): the number of codes to generate (max 1000) (default 1)

    Returns:
        list<str>: the created tournament codes
    """
    if team_size < 1 or team_size > 5:
        raise ValueError("Team Size must be between 1 and 5!")
    if not isinstance(spectator_type, cassiopeia.type.core.tournament.SpectatorType):
        spectator_type = cassiopeia.type.core.tournament.SpectatorType(spectator_type.upper())
    if not isinstance(pick_type, cassiopeia.type.core.tournament.PickType):
        pick_type = cassiopeia.type.core.tournament.PickType(pick_type.upper())
    if not isinstance(map_type, cassiopeia.type.core.tournament.MapType):
        map_type = cassiopeia.type.core.tournament.MapType(map_type.upper())

    summoners = cassiopeia.type.dto.tournament.SummonerIdParams([summoner.id for summoner in allowed_summoners]) if allowed_summoners else None
    parameters = cassiopeia.type.dto.tournament.TournamentCodeParameters(team_size, spectator_type.value, pick_type.value, map_type.value, summoners, str(meta_data))

    return cassiopeia.dto.tournamentapi.create_tournament_codes(tournament_id, parameters, count)


def get_tournament_code(tournament_code):
    """
    Gets information about the tournament code

    Args:
        tournament_code (str): the tournament code

    Returns:
        TournamentCode: the tournament code information
    """
    return cassiopeia.type.core.tournament.TournamentCode(cassiopeia.dto.tournamentapi.get_tournament_code(tournament_code))


def update_tournament_code(tournament_code, allowed_summoners=[], spectator_type=None, pick_type=None, map_type=None):
    """
    Updates a tournament code

Args:
        tournament_code (str | TournamentCode): the tournament code to update
        allowed_summoners (list<Summoner>): the summoners who are allowed to participate in the tournament (default [])
        spectator_type (str | SpectatorType): the spectator availability for the tournament (default None)
        pick_type (str | PickType): the pick type for the tournament (default None)
        map_type (str | MapType): the map the tournament is played on (default None)
    """
    if isinstance(tournament_code, cassiopeia.type.core.tournament.TournamentCode):
        tournament_code = tournament_code.code
    if spectator_type and not isinstance(spectator_type, cassiopeia.type.core.tournament.SpectatorType):
        spectator_type = cassiopeia.type.core.tournament.SpectatorType(spectator_type.upper())
    if pick_type and not isinstance(pick_type, cassiopeia.type.core.tournament.PickType):
        pick_type = cassiopeia.type.core.tournament.PickType(pick_type.upper())
    if map_type and not isinstance(map_type, cassiopeia.type.core.tournament.MapType):
        map_type = cassiopeia.type.core.tournament.MapType(map_type.upper())
    summoners = ",".join([str(summoner.id) for summoner in allowed_summoners])
    parameters = cassiopeia.type.dto.tournament.TournamentCodeUpdateParameters(summoners, spectator_type.value if spectator_type else "", pick_type.value if pick_type else "", map_type.value if map_type else "")
    cassiopeia.dto.tournamentapi.update_tournament_code(tournament_code, parameters)


def get_lobby_events(tournament_code):
    """
    Gets the lobby events that have occurred for the tournament code

    Args:
        tournament_code (str | TournamentCode): the tournament code to get lobby events for

    Returns:
        list<LobbyEvent>: the lobby events for that tournament code
    """
    if isinstance(tournament_code, cassiopeia.type.core.tournament.TournamentCode):
        tournament_code = tournament_code.code
    return [cassiopeia.type.core.tournament.LobbyEvent(event) for event in cassiopeia.dto.tournamentapi.get_lobby_events(tournament_code).eventList]


def create_tournament_provider(region, url):
    """
    Creates a tournament provider

    Args:
        region (str | TournamentRegion): the region in which the provider will be running tournaments
        url (str): the provider's callback URL to which tournament game results in this region should be posted. The URL must be well-formed, use the http or https protocol, and use the default port for the protocol (http URLs must use port 80, https URLs must use port 443).

    Returns:
        int: the tournament provider ID
    """
    if isinstance(region, cassiopeia.type.core.common.Region):
        region = cassiopeia.type.core.tournament.TournamentRegion(region.value.upper())
    elif not isinstance(region, cassiopeia.type.core.tournament.TournamentRegion):
        region = cassiopeia.type.core.tournament.TournamentRegion(region.upper())

    parameters = cassiopeia.type.dto.tournament.ProviderRegistrationParameters(region.value, url)
    return cassiopeia.dto.tournamentapi.create_tournament_provider(parameters)


def create_tournament(provider_id, name=""):
    """
    Creates a tournament

    Args:
        provider_id (int): the provider ID to specify the regional registered provider data to associate this tournament
        name (str): the optional name of the tournament (default "")

    Returns:
        int: the tournament ID
    """
    parameters = cassiopeia.type.dto.tournament.TournamentRegistrationParameters(provider_id, name)
    return cassiopeia.dto.tournamentapi.create_tournament(parameters)
