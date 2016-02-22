import cassiopeia.dto.currentgameapi
import cassiopeia.core.requests
import cassiopeia.type.core.currentgame


def get_current_game(summoner):
    """
    Gets the game a summoner is currently in, if they're in one

    Args:
        summoner (Summoner): the summoner to find an active game for

    Returns:
        Game: the game they're in (or None if they aren't in one)
    """
    game = cassiopeia.dto.currentgameapi.get_current_game(summoner.id)

    # Load required data if loading policy is eager
    if game and cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_champions() if game.champion_ids else None
        cassiopeia.riotapi.get_masteries() if game.mastery_ids else None
        cassiopeia.riotapi.get_runes() if game.rune_ids else None
        summoner_ids = game.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_summoner_spells() if game.summoner_spell_ids else None

    return cassiopeia.type.core.currentgame.Game(game) if game else None
