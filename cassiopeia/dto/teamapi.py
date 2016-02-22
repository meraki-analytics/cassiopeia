import cassiopeia.dto.requests
import cassiopeia.type.dto.team


def get_teams_by_summoner_id(summoner_ids):
    """
    https://developer.riotgames.com/api/methods#!/986/3358

    Args:
        summoner_ids (int | list<int>): the summoner ID(s) to look up teams for

    Returns:
        dict<str, list<Team>>: the requested summoners' teams
    """
    # Can only have 10 summoners max if it's a list
    if isinstance(summoner_ids, list) and len(summoner_ids) > 10:
        raise ValueError("Can only get up to 10 summoners' teams at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/team/by-summoner/{ids}".format(version=cassiopeia.dto.requests.api_versions["team"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, teams in response.items():
        response[id_] = [cassiopeia.type.dto.team.Team(team) for team in teams]

    return response


def get_teams_by_id(team_ids):
    """
    https://developer.riotgames.com/api/methods#!/986/3358

    Args:
        team_ids (str | list<str>): the team ID(s) to look up

    Returns:
        dict<str, Team>: the requested teams
    """
    # Can only have 10 teams max if it's a list
    if isinstance(team_ids, list) and len(team_ids) > 10:
        raise ValueError("Can only get up to 10 teams at once.")

    id_string = ",".join(team_ids) if isinstance(team_ids, list) else team_ids

    # Get JSON response
    request = "{version}/team/{ids}".format(version=cassiopeia.dto.requests.api_versions["team"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, team in response.items():
        response[id_] = cassiopeia.type.dto.team.Team(team)

    return response
