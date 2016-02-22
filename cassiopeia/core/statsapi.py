import cassiopeia.riotapi
import cassiopeia.dto.statsapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.stats


def get_ranked_stats(summoner, season=None):
    """
    Gets a summoner's ranked stats

    Args:
        summoner (Summoner): the summoner to get ranked stats for
        season (Season): the season to get ranked stats for (None will give current season stats) (default None)

    Returns:
        dict<Champion, AggregatedStats>: the summoner's ranked stats divided by champion. The entry for None contains combined stats for all champions.
    """
    if season and season not in cassiopeia.type.core.common.stats_seasons:
        raise ValueError("Must use a valid season to get ranked stats for")

    stats = cassiopeia.dto.statsapi.get_ranked_stats(summoner.id, season.value if season else None)
    champions = {champion.id: champion for champion in cassiopeia.riotapi.get_champions_by_id(list(stats.champion_ids))}
    champions[0] = None

    return {champions[stat.id]: cassiopeia.type.core.stats.AggregatedStats(stat.stats) for stat in stats.champions}


def get_stats(summoner, season=None):
    """
    Gets a summoner's stats

    Args:
        summoner (Summoner): the summoner to get stats for
        season (Season): the season to get stats for (None will give current season stats) (default None)

    Returns:
        dict<StatSummaryType, StatsSummary>: the summoner's stats divided by queue type
    """
    if season and season not in cassiopeia.type.core.common.stats_seasons:
        raise ValueError("Must use a valid season to get stats for")

    stats = cassiopeia.dto.statsapi.get_stats(summoner.id, season.value if season else None)
    return {cassiopeia.type.core.common.StatSummaryType(summary.playerStatSummaryType): cassiopeia.type.core.stats.StatsSummary(summary) for summary in stats.playerStatSummaries}
