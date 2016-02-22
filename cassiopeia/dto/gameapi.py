import cassiopeia.dto.requests
import cassiopeia.type.dto.game


def get_recent_games(summoner_id):
    """
    https://developer.riotgames.com/api/methods#!/1016/3445

    Args:
        summoner_id (int): the ID of the summoner to find recent games for

    Returns:
        RecentGames: the summoner's recent games
    """
    request = "{version}/game/by-summoner/{summoner_id}/recent".format(version=cassiopeia.dto.requests.api_versions["game"], summoner_id=summoner_id)
    return cassiopeia.type.dto.game.RecentGames(cassiopeia.dto.requests.get(request))
