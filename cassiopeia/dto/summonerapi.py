import urllib.parse

import cassiopeia.dto.requests
import cassiopeia.type.dto.summoner


def get_summoners_by_name(summoner_names):
    """
    https://developer.riotgames.com/api/methods#!/1017/3446

    Args:
        summoner_names (str | list<str>): the summoner name(s) to look up

    Returns:
        dict<str, Summoner>: the requested summoners
    """
    # Can only have 40 summoners max if it's a list
    if isinstance(summoner_names, list) and len(summoner_names) > 40:
        raise ValueError("Can only get up to 40 summoners at once.")

    name_string = ",".join(urllib.parse.quote(x) for x in summoner_names) if isinstance(summoner_names, list) else urllib.parse.quote(summoner_names)

    # Get JSON response
    request = "{version}/summoner/by-name/{names}".format(version=cassiopeia.dto.requests.api_versions["summoner"], names=name_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for name, summoner in response.items():
        response[name] = cassiopeia.type.dto.summoner.Summoner(summoner)

    return response


def get_summoners_by_id(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/1017/3447

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to look up

    Returns:
        dict<str, Summoner>: the requested summoners
    """
    # Can only have 40 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 40:
        raise ValueError("Can only get up to 40 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/summoner/{ids}".format(version=cassiopeia.dto.requests.api_versions["summoner"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, summoner in response.items():
        response[id_] = cassiopeia.type.dto.summoner.Summoner(summoner)

    return response


def get_summoner_masteries(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/1017/3450

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to get mastery pages for

    Returns:
        dict<str, MasteryPages>: the requested summoners' mastery pages
    """
    # Can only have 40 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 40:
        raise ValueError("Can only get masteries for up to 40 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/summoner/{ids}/masteries".format(version=cassiopeia.dto.requests.api_versions["summoner"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, masteries in response.items():
        response[id_] = cassiopeia.type.dto.summoner.MasteryPages(masteries)

    return response


def get_summoner_names(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/1017/3451

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to get names for

    Returns:
        dict<str, str>: the requested summoners' names
    """
    # Can only have 40 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 40:
        raise ValueError("Can only get names for up to 40 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/summoner/{ids}/name".format(version=cassiopeia.dto.requests.api_versions["summoner"], ids=id_string)
    return cassiopeia.dto.requests.get(request)


def get_summoner_runes(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/1017/3449

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to get rune pages for

    Returns:
        dict<str, RunePages>: the requested summoners' rune pages
    """
    # Can only have 40 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 40:
        raise ValueError("Can only get runes for up to 40 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/summoner/{ids}/runes".format(version=cassiopeia.dto.requests.api_versions["summoner"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, runes in response.items():
        response[id_] = cassiopeia.type.dto.summoner.RunePages(runes)

    return response
