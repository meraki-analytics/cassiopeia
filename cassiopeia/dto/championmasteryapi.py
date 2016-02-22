import cassiopeia.dto.requests
import cassiopeia.type.core.common
import cassiopeia.type.dto.championmastery


def get_champion_mastery(summoner_id, champion_id):
    """
    https://developer.riotgames.com/api/methods#!/1034/3545

    Args:
        summoner_id (int): the summoner ID to get champion mastery for
        champion_id (int): the champion ID for the desired champion

    Returns:
        list<ChampionMastery>: the summoner's champion mastery value for the specified champion
    """
    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/champion/{championId}".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id, championId=champion_id)
    return cassiopeia.type.dto.championmastery.ChampionMastery(cassiopeia.dto.requests.get(request, include_base=False))


def get_champion_masteries(summoner_id):
    """
    https://developer.riotgames.com/api/methods#!/1034/3544

    Args:
        summoner_id (int): the summoner ID to get champion masteries for

    Returns:
        list<ChampionMastery>: the summoner's champion masteries
    """
    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/champions".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    response = cassiopeia.dto.requests.get(request, include_base=False)

    # Convert response to Dto type
    return [cassiopeia.type.dto.championmastery.ChampionMastery(cm) for cm in response]


def get_champion_mastery_score(summoner_id):
    """
    https://developer.riotgames.com/api/methods#!/1034/3546

    Args:
        summoner_id (int): the summoner ID to get champion masteries for

    Returns:
        int: the summoner's total champion mastery score
    """
    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/score".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    return cassiopeia.dto.requests.get(request, include_base=False)


def get_top_champion_masteries(summoner_id, count=3):
    """
    https://developer.riotgames.com/api/methods#!/1034/3540

    Args:
        summoner_id (int): the summoner ID to get champion masteries for
        count (int): the maximum number of entires to retrieve (default 3)

    Returns:
        list<ChampionMastery>: the summoner's top champion masteries
    """
    region = cassiopeia.type.core.common.Region(cassiopeia.dto.requests.region)
    platform = cassiopeia.type.core.common.Platform[region.name]

    # Get JSON response
    request = "https://{server}.api.pvp.net/championmastery/location/{platform}/player/{summonerId}/topchampions".format(server=cassiopeia.dto.requests.region, platform=platform.value, summonerId=summoner_id)
    response = cassiopeia.dto.requests.get(request, {"count": count}, include_base=False)

    # Convert response to Dto type
    return [cassiopeia.type.dto.championmastery.ChampionMastery(cm) for cm in response]
