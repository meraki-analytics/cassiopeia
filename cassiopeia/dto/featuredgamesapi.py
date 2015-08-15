import cassiopeia.dto.requests
import cassiopeia.type.dto.featuredgames

# @return # cassiopeia.type.dto.featuredgames.FeaturedGames # The current featured game list
def get_featured_games():
    request = "observer-mode/rest/featured"
    return cassiopeia.type.dto.featuredgames.FeaturedGames(cassiopeia.dto.requests.get(request, include_base=False))