import cassiopeia.dto.requests
import cassiopeia.type.dto.league


def get_leagues_by_summoner(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/985/3351

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to get leagues for

    Returns:
        dict<str, list<League>>: the summoner(s)' leagues
    """
    # Can only have 10 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 10:
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/league/by-summoner/{ids}".format(version=cassiopeia.dto.requests.api_versions["league"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = cassiopeia.type.dto.league.League(league)

    return response


def get_league_entries_by_summoner(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/985/3356

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to get league entries for

    Returns:
        dict<str, list<League>>: the summoner(s)' league entries
    """
    # Can only have 10 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 10:
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/league/by-summoner/{ids}/entry".format(version=cassiopeia.dto.requests.api_versions["league"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = cassiopeia.type.dto.league.League(league)

    return response


def get_leagues_by_team(team_ids):
    """
    https://developer.riotgames.com/api/methods#!/985/3352

    Args:
        team_ids (str | list<str>): the team ID(s) to get leagues for

    Returns:
        dict<str, list<League>>: the team(s)' leagues
    """
    # Can only have 10 teams max if it's a list
    if isinstance(team_ids, list) and len(team_ids) > 10:
        raise ValueError("Can only get leagues for up to 10 teams at once.")

    id_string = ",".join(team_ids) if isinstance(team_ids, list) else str(team_ids)

    # Get JSON response
    request = "{version}/league/by-team/{ids}".format(version=cassiopeia.dto.requests.api_versions["league"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        response[id_] = [cassiopeia.type.dto.league.League(league) for league in leagues]

    return response


def get_league_entries_by_team(team_ids):
    """
    https://developer.riotgames.com/api/methods#!/985/3355

    Args:
        team_ids (str | list<str>): the team ID(s) to get league entries for

    Returns:
        dict<str, list<League>>: the team(s)' league entries
    """
    # Can only have 10 teams max if it's a list
    if isinstance(team_ids, list) and len(team_ids) > 10:
        raise ValueError("Can only get league entries for up to 10 teams at once.")

    id_string = ",".join(team_ids) if isinstance(team_ids, list) else str(team_ids)

    # Get JSON response
    request = "{version}/league/by-team/{ids}/entry".format(version=cassiopeia.dto.requests.api_versions["league"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        response[id_] = [cassiopeia.type.dto.league.League(league) for league in leagues]

    return response


def get_challenger(queue_type):
    """
    https://developer.riotgames.com/api/methods#!/985/3353

    Args:
        queue_type (str): the queue type to get the challenger league for ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")

    Returns:
        League: the challenger league
    """
    request = "{version}/league/challenger".format(version=cassiopeia.dto.requests.api_versions["league"])
    return cassiopeia.type.dto.league.League(cassiopeia.dto.requests.get(request, {"type": queue_type}))


def get_master(queue_type):
    """
    https://developer.riotgames.com/api/methods#!/985/3354

    Args:
        queue_type (str): the queue type to get the master league for ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")

    Returns:
        League: the master league
    """
    request = "{version}/league/master".format(version=cassiopeia.dto.requests.api_versions["league"])
    return cassiopeia.type.dto.league.League(cassiopeia.dto.requests.get(request, {"type": queue_type}))
