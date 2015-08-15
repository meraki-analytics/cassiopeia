import cassiopeia.dto.gameapi
import cassiopeia.core.requests
import cassiopeia.type.core.game

# @param # cassiopeia.type.core.summoner.Summoner # A Summoner
# @return # list<cassiopeia.type.core.game.Game> # The summoner's recent games
def get_recent_games(summoner):
    games = cassiopeia.dto.gameapi.get_recent_games(summoner.id)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_items(list(games.item_ids))
        cassiopeia.riotapi.get_champions_by_id(list(games.champion_ids))
        cassiopeia.riotapi.get_summoners_by_id(list(games.summoner_ids))
        cassiopeia.riotapi.get_summoner_spells(list(games.summoner_spell_ids))

    return [cassiopeia.type.core.game.Game(game, games.summonerId) for game in games.games]