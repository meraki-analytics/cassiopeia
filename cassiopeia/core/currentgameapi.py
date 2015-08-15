import cassiopeia.dto.currentgameapi
import cassiopeia.core.requests
import cassiopeia.type.core.currentgame

# @param summoner # cassiopeia.type.core.summoner.Summoner # The summoner to find an active game for
# @return # cassiopeia.type.core.currentgame.Game # The summoner's current game (or None if they aren't in one)
def get_current_game(summoner):
    game = cassiopeia.dto.currentgameapi.get_current_game(summoner.id)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        ids = game.champion_ids
        cassiopeia.riotapi.get_champions_by_id(list(ids)) if ids else None
        ids = game.mastery_ids
        cassiopeia.riotapi.get_masteries(list(ids)) if ids else None
        ids = game.rune_ids
        cassiopeia.riotapi.get_runes(list(ids)) if ids else None
        ids = game.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(ids)) if ids else None
        ids = game.summoner_spell_ids
        cassiopeia.riotapi.get_summoner_spells(list(ids)) if ids else None

    return cassiopeia.type.core.currentgame.Game(game) if game else None