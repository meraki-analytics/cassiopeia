import cassiopeia.dto.requests
import cassiopeia.type.core.common
import cassiopeia.type.dto.currentgame
import cassiopeia.type.api.exception


def get_current_game(summoner_id):
    """
    https://developer.riotgames.com/api/methods#!/976/3336

    Args:
        summoner_id (int): the ID of the summoner to find an active game for

    Returns:
        CurrentGameInfo: the summoner's current game (or None if they aren't in one)
    """
    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]
    request = "https://{server}.api.pvp.net/observer-mode/rest/consumer/getSpectatorGameInfo/{platform}/{summoner_id}".format(server=cassiopeia.dto.requests.region, platform=platform.value, summoner_id=summoner_id)
    try:
        return cassiopeia.type.dto.currentgame.CurrentGameInfo(cassiopeia.dto.requests.get(request, include_base=False))
    except cassiopeia.type.api.exception.APIError as e:
        if e.error_code == 404:
            return None
        raise e
