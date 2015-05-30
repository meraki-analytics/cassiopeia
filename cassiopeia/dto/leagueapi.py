from cassiopeia import requests
from cassiopeia.type.dto.league import *

# @param summoner_ids # list<int> or int # A list of summoner IDs to get leagues for or a single ID
# @return # dict<str, list<League>> # A mapping of summoner IDs to the leagues the summoner is in
def get_leagues_by_summoner(summoner_ids):
    # Can only have 10 summoners max if it's a list
    if(isinstance(summoner_ids, list) and len(summoner_ids > 10)):
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = id_string = str(summoner_ids).replace(" ", "")[1:-1] if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/league/by-summoner/{ids}".format(version=requests.api_versions["league"], ids=id_string)
    response = requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = League(league)

    return response

# @param summoner_ids # list<int> or int # A list of summoner IDs to get leagues for or a single ID
# @return # dict<str, list<League>> # A mapping of summoner IDs to the leagues the summoner is in (only including the summoner's own entries)
def get_league_entries_by_summoner(summoner_ids):
    # Can only have 10 summoners max if it's a list
    if(isinstance(summoner_ids, list) and len(summoner_ids > 10)):
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = id_string = str(summoner_ids).replace(" ", "")[1:-1] if isinstance(summoner_ids, list) else str(summoner_ids)

    # Get JSON response
    request = "{version}/league/by-summoner/{ids}/entry".format(version=requests.api_versions["league"], ids=id_string)
    response = requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = League(league)

    return response

# @param team_ids # list<str> or str # A list of team IDs to get leagues for or a single ID
# @return # dict<str, list<League>> # A mapping of team IDs to the leagues the team is in
def get_leagues_by_team(team_ids):
    # Can only have 10 teams max if it's a list
    if(isinstance(team_ids, list) and len(team_ids > 10)):
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = id_string = str(team_ids).replace(" ", "")[1:-1] if isinstance(team_ids, list) else str(team_ids)

    # Get JSON response
    request = "{version}/league/by-team/{ids}".format(version=requests.api_versions["league"], ids=id_string)
    response = requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = League(league)

    return response

# @param team_ids # list<str> or str # A list of team IDs to get leagues for or a single ID
# @return # dict<str, list<League>> # A mapping of team IDs to the leagues the team is in (only including the team's own entries)
def get_league_entries_by_team(team_ids):
    # Can only have 10 teams max if it's a list
    if(isinstance(team_ids, list) and len(team_ids > 10)):
        raise ValueError("Can only get leagues for up to 10 summoners at once.")

    id_string = id_string = str(team_ids).replace(" ", "")[1:-1] if isinstance(team_ids, list) else str(team_ids)

    # Get JSON response
    request = "{version}/league/by-team/{ids}/entry".format(version=requests.api_versions["league"], ids=id_string)
    response = requests.get(request)

    # Convert response to Dto type
    for id_, leagues in response.items():
        for i, league in enumerate(leagues):
            leagues[i] = League(league)

    return response

# @param queue_type # str # The queue type to get the challenger league for ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")
# @return # League # The challenger league
def get_challenger(queue_type):
    request = "{version}/league/challenger".format(version=requests.api_versions["league"])
    return League(requests.get(request, {"type": queue_type}))

# @param queue_type # str # The queue type to get the master league for ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")
# @return # League # The master league
def get_master(queue_type):
    request = "{version}/league/master".format(version=requests.api_versions["league"])
    return League(requests.get(request, {"type": queue_type}))