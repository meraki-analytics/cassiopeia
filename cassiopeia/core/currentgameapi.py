import cassiopeia.dto.currentgameapi
import cassiopeia.core.requests
import cassiopeia.type.core.currentgame

# @param summoner # cassiopeia.type.core.summoner.Summoner # The summoner to find an active game for
# @return # cassiopeia.type.core.currentgame.Game # The summoner's current game (or None if they aren't in one)
def get_current_game(summoner):
    game = cassiopeia.dto.currentgameapi.get_current_game(summoner.id)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_champions_by_id(list(game.champion_ids))
        cassiopeia.riotapi.get_masteries(list(game.mastery_ids))
        cassiopeia.riotapi.get_runes(list(game.rune_ids))
        cassiopeia.riotapi.get_summoners_by_id(list(game.summoner_ids))
        cassiopeia.riotapi.get_summoner_spells(list(game.summoner_spell_ids))

    return cassiopeia.type.core.currentgame.Game(game) if game else None