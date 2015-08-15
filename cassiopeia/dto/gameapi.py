import cassiopeia.dto.requests
import cassiopeia.type.dto.game

# @param summoner_id # int # The ID of the summoner to get recent games for
# @return # cassiopeia.type.dto.game.RecentGames # The summoner's recent games
def get_recent_games(summoner_id):
    request = "{version}/game/by-summoner/{summoner_id}/recent".format(version=cassiopeia.dto.requests.api_versions["game"], summoner_id=summoner_id)
    return cassiopeia.type.dto.game.RecentGames(cassiopeia.dto.requests.get(request))