import cassiopeia.riotapi
import cassiopeia.dto.leagueapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.league

# @param queue_type # cassiopeia.type.core.common.Queue # The queue type to get the challenger league for
# @return # cassiopeia.type.core.league.League # The challenger league
def get_challenger(queue_type=cassiopeia.type.core.common.Queue.ranked_solo):
    if(queue_type not in cassiopeia.type.core.common.ranked_queues):
        raise ValueError("Must use a ranked queue type to get ranked leagues")

    league = cassiopeia.dto.leagueapi.get_challenger(queue_type.value)
    
    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_summoners_by_id(list(league.summoner_ids))
        # cassiopeia.riotapi.get_teams(list(league.team_ids))

    return cassiopeia.type.core.league.League(league)

# @param queue_type # cassiopeia.type.core.common.Queue # The queue type to get the master league for
# @return # cassiopeia.type.core.league.League # The master league
def get_master(queue_type=cassiopeia.type.core.common.Queue.ranked_solo):
    if(queue_type not in cassiopeia.type.core.common.ranked_queues):
        raise ValueError("Must use a ranked queue type to get ranked leagues")

    league = cassiopeia.dto.leagueapi.get_master(queue_type.value)
    
    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_summoners_by_id(list(league.summoner_ids))
        # cassiopeia.riotapi.get_teams(list(league.team_ids))

    return cassiopeia.type.core.league.League(league)

# @param ids # list<int> or int # The summoner ID(s) to get leagues for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The leagues for the requested summoner(s)
def _get_leagues_by_summoner_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_leagues_by_summoner, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        team_ids = set()
        for summoner in leagues.items():
            for league in summoner[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids))
        # cassiopeia.riotapi.get_teams(list(team_ids))

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues[str(id_)]] for id_ in ids]

# @param summoners # list<cassiopeia.type.core.summoner.Summoner> or cassiopeia.type.core.summoner.Summoner # The summoner(s) to get leagues for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The leagues for the requested summoner(s)
def get_leagues_by_summoner(summoners):
    if(isinstance(summoners, list)):
        return _get_leagues_by_summoner_id([summoner.id for summoner in summoners])
    else:
        return _get_leagues_by_summoner_id(summoners.id)

# @param ids # list<int> or int # The summoner ID(s) to get league entries for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The league entries for the requested summoner(s)
def _get_league_entries_by_summoner_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_league_entries_by_summoner, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        team_ids = set()
        for summoner in leagues.items():
            for league in summoner[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids))
        # cassiopeia.riotapi.get_teams(list(team_ids))


    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues[str(id_)]] for id_ in ids]

# @param summoners # list<cassiopeia.type.core.summoner.Summoner> or cassiopeia.type.core.summoner.Summoner # The summoner(s) to get league entries for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The league entries for the requested summoner(s)
def get_league_entries_by_summoner(summoners):
    if(isinstance(summoners, list)):
        return _get_league_entries_by_summoner_id([summoner.id for summoner in summoners])
    else:
        return _get_league_entries_by_summoner_id(summoners.id)

# @param ids # list<str> or str # The team ID(s) to get leagues for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The leagues for the requested team(s)
def _get_leagues_by_team_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_leagues_by_team, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        team_ids = set()
        for team in leagues.items():
            for league in team[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids))
        # cassiopeia.riotapi.get_teams(list(team_ids))

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues[str(id_)]] for id_ in ids]

# @param teams # list<cassiopeia.type.core.team.Team> or cassiopeia.type.core.team.Team # The team(s) to get leagues for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The leagues for the requested team(s)
def get_leagues_by_team(teams):
    if(isinstance(teams, list)):
        return _get_leagues_by_team_id([team.id for team in teams])
    else:
        return _get_leagues_by_team_id(teams.id)

# @param ids # list<str> or str # The team ID(s) to get league entries for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The league entries for the requested team(s)
def _get_league_entries_by_team_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_league_entries_by_team, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        team_ids = set()
        for team in leagues.items():
            for league in team[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids))
        # cassiopeia.riotapi.get_teams(list(team_ids))

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues[str(id_)]] for id_ in ids]

# @param teams # list<cassiopeia.type.core.team.Team> or cassiopeia.type.core.team.Team # The team(s) to get league entries for
# @return # list<list<cassiopeia.type.core.league.League>> or list<cassiopeia.type.core.league.League> # The league entries for the requested team(s)
def get_league_entries_by_team(teams):
    if(isinstance(teams, list)):
        return _get_league_entries_by_team_id([team.id for team in teams])
    else:
        return _get_league_entries_by_team_id(teams.id)