import cassiopeia.dto.requests
import cassiopeia.type.dto.stats

# @param summoner_id # int # The summoner to get ranked stats for
# @param season # str # The season to get ranked stats for ("SEASON2015", "SEASON2014", "SEASON3")
# @return # RankedStats # The ranked stats for the summoner and season specified
def get_ranked_stats(summoner_id, season=None):
    request = "{version}/stats/by-summoner/{id_}/ranked".format(version=cassiopeia.dto.requests.api_versions["stats"], id_=summoner_id)

    params = {}
    if(season):
        params["season"] = season

    return cassiopeia.type.dto.stats.RankedStats(cassiopeia.dto.requests.get(request, params))

# @param summoner_id # int # The summoner to get stats for
# @param season # str # The season to get stats for ("SEASON2015", "SEASON2014", "SEASON3")
# @return # PlayerStatsSummaryList # The stats for the summoner and season specified
def get_stats(summoner_id, season=None):
    request = "{version}/stats/by-summoner/{id_}/summary".format(version=cassiopeia.dto.requests.api_versions["stats"], id_=summoner_id)

    params = {}
    if(season):
        params["season"] = season

    return cassiopeia.type.dto.stats.PlayerStatsSummaryList(cassiopeia.dto.requests.get(request, params))