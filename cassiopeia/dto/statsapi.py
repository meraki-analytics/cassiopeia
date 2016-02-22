import cassiopeia.dto.requests
import cassiopeia.type.dto.stats


def get_ranked_stats(summoner_id, season=None):
    """
    https://developer.riotgames.com/api/methods#!/1018/3452

    Args:
        summoner_id (int): the summoner to get ranked stats for
        season (str): the season to get ranked stats for ("SEASON2015", "SEASON2014", "SEASON3") (default None)

    Returns:
        RankedStats: the ranked stats for the summoner and season specified
    """
    request = "{version}/stats/by-summoner/{id_}/ranked".format(version=cassiopeia.dto.requests.api_versions["stats"], id_=summoner_id)

    params = {}
    if season:
        params["season"] = season

    return cassiopeia.type.dto.stats.RankedStats(cassiopeia.dto.requests.get(request, params))


def get_stats(summoner_id, season=None):
    """
    https://developer.riotgames.com/api/methods#!/1018/3453

    Args:
        summoner_id (int): the summoner to get ranked stats for
        season (str): the season to get ranked stats for ("SEASON2015", "SEASON2014", "SEASON3") (default None)

    Returns:
        PlayerStatsSummaryList: the ranked stats for the summoner and season specified
    """
    request = "{version}/stats/by-summoner/{id_}/summary".format(version=cassiopeia.dto.requests.api_versions["stats"], id_=summoner_id)

    params = {}
    if season:
        params["season"] = season

    return cassiopeia.type.dto.stats.PlayerStatsSummaryList(cassiopeia.dto.requests.get(request, params))
