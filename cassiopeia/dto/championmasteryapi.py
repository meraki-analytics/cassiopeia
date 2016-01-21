import cassiopeia.dto.requests
import cassiopeia.type.core.common
import cassiopeia.type.dto.championmastery


def get_champion_mastery(summoner_id, champion_id):
    """https://developer.riotgames.com/api/methods#!/1034/3545

    summoner_id    int                      the summoner ID to get champion mastery for
    champion_id    int                      the champion ID for the desired champion

    return         list<ChampionMastery>    the summoner's champion mastery value for the specified champion
    """

    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/champion/{championId}".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id, championId=champion_id)
    response = cassiopeia.type.dto.championmastery.ChampionMastery(cassiopeia.dto.requests.get(request, include_base=False))

    return response

def get_champion_masteries(summoner_id):
    """https://developer.riotgames.com/api/methods#!/1034/3544

    summoner_id    int                      the summoner ID to get champion masteries for

    return         list<ChampionMastery>    the summoner's champion masteries
    """

    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/champions".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    response = cassiopeia.dto.requests.get(request, include_base=False)

    # Convert response to Dto type
    response = [cassiopeia.type.dto.championmastery.ChampionMastery(cm) for cm in response]

    return response

def get_champion_mastery_score(summoner_id):
    """https://developer.riotgames.com/api/methods#!/1034/3546

    summoner_id    int    the summoner ID to get champion masteries for

    return         int    the summoner's total champion mastery score
    """

    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/score".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    response = cassiopeia.dto.requests.get(request, include_base=False)

    return response

def get_top_champion_masteries(summoner_id):
    """https://developer.riotgames.com/api/methods#!/1034/3540

    summoner_id    int                      the summoner ID to get champion masteries for

    return         list<ChampionMastery>    the summoner's top champion masteries
    """

    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/topchampions".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    response = cassiopeia.dto.requests.get(request, include_base=False)

    # Convert response to Dto type
    response = [cassiopeia.type.dto.championmastery.ChampionMastery(cm) for cm in response]

    return response