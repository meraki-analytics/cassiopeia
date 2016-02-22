import cassiopeia.dto.gameapi
import cassiopeia.core.requests
import cassiopeia.type.core.game


def get_recent_games(summoner):
    """
    Gets the most recent games a summoner played

    Args:
        summoner (Summoner): the summoner to get recent games for

    Returns:
        list<Game>: the summoner's recent games
    """
    games = cassiopeia.dto.gameapi.get_recent_games(summoner.id)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = games.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_summoner_spells() if games.summoner_spell_ids else None

    return [cassiopeia.type.core.game.Game(game, games.summonerId) for game in games.games]
