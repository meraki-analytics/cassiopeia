import cassiopeia.dto.requests
import cassiopeia.type.dto.team

# @param summoner_ids # list<int> or int # The summoner ID(s) to look up teams for
# @return # dict<str, list<cassiopeia.type.dto.team.Team>> # The requested teams
def get_teams_by_summoner_id(summoner_ids):
    # Can only have 10 summoners max if it's a list
    if(isinstance(summoner_ids, list) and len(summoner_ids) > 10):
        raise ValueError("Can only get up to 10 summoners' teams at once.")

    id_string = ",".join(str(x) for x in summoner_ids) if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/team/by-summoner/{ids}".format(version=cassiopeia.dto.requests.api_versions["team"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, teams in response.items():
        response[id_] = [cassiopeia.type.dto.team.Team(team) for team in teams]

    return response

# @param team_ids # list<str> or str # The team ID(s) to look up
# @return # dict<str, cassiopeia.type.dto.team.Team> # The requested teams
def get_teams_by_id(team_ids):
    # Can only have 10 teams max if it's a list
    if(isinstance(team_ids, list) and len(team_ids) > 10):
        raise ValueError("Can only get up to 10 teams at once.")

    id_string = ",".join(team_ids) if isinstance(team_ids, list) else team_ids

    # Get JSON response
    request = "{version}/team/{ids}".format(version=cassiopeia.dto.requests.api_versions["team"], ids=id_string)
    response = cassiopeia.dto.requests.get(request)

    # Convert response to Dto type
    for id_, team in response.items():
        response[id_] = cassiopeia.type.dto.team.Team(team)

    return response