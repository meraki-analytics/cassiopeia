import cassiopeia.riotapi
import cassiopeia.dto.statsapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.stats

# @param summoner # cassiopeia.type.core.summoner.Summoner # The summoner to get stats for
# @param season # cassiopeia.type.core.common.Season # The season to get stats for. Current is default.
# @return # dict<cassiopeia.type.core.staticdata.Champion, cassiopeia.type.core.stats.AggregatedStats> # The ranked stats divided by champion. The entry for None has combined stats for all champions.
def get_ranked_stats(summoner, season=None):
    if(season and season not in cassiopeia.type.core.common.stats_seasons):
        raise ValueError("Must use a valid season to get ranked stats for")

    stats = cassiopeia.dto.statsapi.get_ranked_stats(summoner.id, season)
    champions = {champion.id: champion for champion in cassiopeia.riotapi.get_champions_by_id(list(stats.champion_ids))}
    champions[0] = None

    return {champions[stat.id]: cassiopeia.type.core.stats.AggregatedStats(stat.stats) for stat in stats.champions}

# @param summoner # cassiopeia.type.core.summoner.Summoner # The summoner to get stats for
# @param season # cassiopeia.type.core.common.Season # The season to get stats for. Current is default.
# @return # dict<cassiopeia.type.core.common.StatSummaryType, cassiopeia.type.core.stats.StatsSummary> # The ranked stats divided by champion. The entry for None has combined stats for all champions.
def get_stats(summoner, season=None):
    if(season and season not in cassiopeia.type.core.common.stats_seasons):
        raise ValueError("Must use a valid season to get stats for")

    stats = cassiopeia.dto.statsapi.get_stats(summoner.id, season)
    return {cassiopeia.type.core.common.StatSummaryType(summary.playerStatSummaryType): cassiopeia.type.core.stats.StatsSummary(summary) for summary in stats.playerStatSummaries}