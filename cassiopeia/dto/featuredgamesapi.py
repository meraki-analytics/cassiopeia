import cassiopeia.dto.requests
import cassiopeia.type.dto.featuredgames

def get_featured_games():
    """https://developer.riotgames.com/api/methods#!/977/3337

    return    FeaturedGames    the current featured game list
    """
    request = "https://{server}.api.pvp.net/observer-mode/rest/featured".format(server=cassiopeia.dto.requests.region.lower())
    return cassiopeia.type.dto.featuredgames.FeaturedGames(cassiopeia.dto.requests.get(request, include_base=False))