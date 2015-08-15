import cassiopeia.dto.featuredgamesapi
import cassiopeia.core.requests
import cassiopeia.type.core.featuredgames

# @return # list<cassiopeia.type.core.featuredgames.Game> # The current featured game list
def get_featured_games():
    games = cassiopeia.dto.featuredgamesapi.get_featured_games()

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_champions_by_id(list(games.champion_ids))
        cassiopeia.riotapi.get_summoner_spells(list(games.summoner_spell_ids))

    return [cassiopeia.type.core.featuredgames.Game(game) for game in games.gameList]