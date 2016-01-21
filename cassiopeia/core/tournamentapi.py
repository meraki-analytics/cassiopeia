import cassiopeia.dto.tournamentapi
import cassiopeia.type.core.tournament
import cassiopeia.type.dto.tournament


def create_tournament_codes(tournament_id, count, team_size, spectator_type, pick_type, map_type, allowed_summoners=[], meta_data=""):
    """Creates tournament codes for a tournament

    tournament_id        int               the tournament ID to generate codes for
    count                int               the number of codes to generate (max 1000)
    team_size            int               the team size for the tournament (1-5)
    spectator_type       SpectatorType     the spectator availability for the tournament
    pick_type            PickType          the pick type for the tournament
    map_type             MapType           the map the tournament is played on
    allowed_summoners    list<Summoner>    the summoners who are allowed to participate in the tournament (default [])
    meta_data            str | object      meta data to be included with the tournament. Any non-string value will be cast to a string. (default "")

    return               list<str>         the created tournament codes
    """
    if team_size < 1 or team_size > 5:
            raise ValueError("Team Size must be between 1 and 5!")

    summoners = cassiopeia.type.dto.tournament.SummonerIdParams([summoner.id for summoner in allowed_summoners]) if allowed_summoners else None
    parameters = cassiopeia.type.dto.tournament.TournamentCodeParameters(team_size, spectator_type.value, pick_type.value, map_type.value, summoners, str(meta_data))

    return cassiopeia.dto.tournamentapi.create_tournament_codes(tournament_id, count, parameters)


def get_tournament_code(tournament_code):
    """Gets information about the tournament code

    tournament_code    str               the tournament code

    return             TournamentCode    the tournament code information
    """
    return cassiopeia.type.core.tournament.TournamentCode(cassiopeia.dto.tournamentapi.get_tournament_code(tournament_code))


def update_tournament_code(tournament_code, allowed_summoners=[], spectator_type=None, pick_type=None, map_type=None):
    """Updates a tournament code

    tournament_code      str               the tournament code to update
    allowed_summoners    list<Summoner>    the summoners who are allowed to participate in the tournament (default [])
    spectator_type       SpectatorType     the spectator availability for the tournament (default None)
    pick_type            PickType          the pick type for the tournament (default None)
    map_type             MapType           the map the tournament is played on (default None)
    """
    summoners = ",".join([str(summoner.id) for summoner in allowed_summoners])
    parameters = cassiopeia.type.dto.tournament.TournamentCodeUpdateParameters(summoners, spectator_type.value if spectator_type else "", pick_type.value if pick_type else "", map_type.value if map_type else "")
    cassiopeia.dto.tournamentapi.update_tournament_code(tournament_code, parameters)


def get_lobby_events(tournament_code):
    """Gets the lobby events that have occurred for the tournament code

    tournament_code    str                  the tournament code to get lobby events for

    return             list<LobbyEvent>     the lobby events for that tournament code
    """
    return [cassiopeia.type.core.tournament.LobbyEvent(event) for event in cassiopeia.dto.tournamentapi.get_lobby_events(tournament_code)]


def create_tournament_provider(region, url):
    """Creates a tournament provider

    region    TournamentRegion    the region in which the provider will be running tournaments
    url       str                 the provider's callback URL to which tournament game results in this region should be posted. The URL must be well-formed, use the http or https protocol, and use the default port for the protocol (http URLs must use port 80, https URLs must use port 443).

    return    int                 the tournament provider ID
    """
    parameters = cassiopeia.type.dto.tournament.ProviderRegistrationParameters(region.value, url)
    return cassiopeia.dto.tournamentapi.create_tournament_provider(parameters)


def create_tournament(provider_id, name=""):
    """Creates a tournament

    provider_id    int    the provider ID to specify the regional registered provider data to associate this tournament
    name           str    the optional name of the tournament (default "")

    return         int    the tournament ID
    """
    parameters = cassiopeia.type.dto.tournament.TournamentRegistrationParameters(provider_id, name)
    return cassiopeia.dto.tournamentapi.create_tournament(parameters)
