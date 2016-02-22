import cassiopeia.riotapi
import cassiopeia.dto.leagueapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.league


def get_challenger(queue_type=cassiopeia.type.core.common.Queue.ranked_solo):
    """
    Gets the challenger league

    Args:
        queue_type (Queue): the queue to get the challenger league for (default Queue.ranked_solo)

    Returns:
        League: the challenger league for that queue
    """
    if queue_type not in cassiopeia.type.core.common.ranked_queues:
        raise ValueError("Must use a ranked queue type to get ranked leagues")

    league = cassiopeia.dto.leagueapi.get_challenger(queue_type.value)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = league.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        team_ids = league.team_ids
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    return cassiopeia.type.core.league.League(league)


def get_master(queue_type=cassiopeia.type.core.common.Queue.ranked_solo):
    """
    Gets the master league

    Args:
        queue_type (Queue): the queue to get the master league for (default Queue.ranked_solo)

    Returns:
        League: the master league for that queue
    """
    if queue_type not in cassiopeia.type.core.common.ranked_queues:
        raise ValueError("Must use a ranked queue type to get ranked leagues")

    league = cassiopeia.dto.leagueapi.get_master(queue_type.value)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = league.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        team_ids = league.team_ids
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    return cassiopeia.type.core.league.League(league)


def __get_leagues_by_summoner_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_leagues_by_summoner, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        team_ids = set()
        for summoner in leagues.items():
            for league in summoner[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues.get(str(id_), []) if leagues.get(str(id_), [])] for id_ in ids]


def get_leagues_by_summoner(summoners):
    """
    Gets the leagues that the summoner(s) belong(s) to. You probably don't want to call this with LoadPolicy.eager set.

    Args:
        summoners (Summoner | list<Summoner>): the summoner(s) to get leagues for

    Returns:
        list<League> | list<list<League>>: the leagues that the requested summoner(s) belong(s) to
    """
    if isinstance(summoners, list):
        return __get_leagues_by_summoner_id([summoner.id for summoner in summoners])
    else:
        return __get_leagues_by_summoner_id(summoners.id)


def __get_league_entries_by_summoner_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_league_entries_by_summoner, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        team_ids = set()
        for summoner in leagues.items():
            for league in summoner[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.league.League(league) for league in leagues[str(ids)]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues.get(str(id_), []) if leagues.get(str(id_), [])] for id_ in ids]


def get_league_entries_by_summoner(summoners):
    """
    Gets the leagues that the summoner(s) belong(s) to, including only the requested summoner(s)' entries

    Args:
        summoners (Summoner | list<Summoner>): the summoner(s) to get leagues for

    Returns:
        list<League> | list<list<League>>: the leagues that the requested summoner(s) belong(s) to
    """
    if isinstance(summoners, list):
        return __get_league_entries_by_summoner_id([summoner.id for summoner in summoners])
    else:
        return __get_league_entries_by_summoner_id(summoners.id)


def __get_leagues_by_team_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_leagues_by_team, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        team_ids = set()
        for team in leagues.items():
            for league in team[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.league.League(league) for league in leagues[ids]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues.get(id_, []) if leagues.get(id_, [])] for id_ in ids]


def get_leagues_by_team(teams):
    """
    Gets the leagues that the team(s) belong(s) to. You probably don't want to call this with LoadPolicy.eager set.

    Args:
        teams (Team | list<Team>): the team(s) to get leagues for

    Returns:
        list<League> | list<list<League>>: the leagues that the requested team(s) belong(s) to
    """
    if isinstance(teams, list):
        return __get_leagues_by_team_id([team.id for team in teams])
    else:
        return __get_leagues_by_team_id(teams.id)


def __get_league_entries_by_team_id(ids):
    leagues = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.leagueapi.get_league_entries_by_team, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        team_ids = set()
        for team in leagues.items():
            for league in team[1]:
                summoner_ids = summoner_ids | league.summoner_ids
                team_ids = team_ids | league.team_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_teams(list(team_ids)) if team_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.league.League(league) for league in leagues[ids]]
    else:
        return [[cassiopeia.type.core.league.League(league) for league in leagues.get(id_, []) if leagues.get(id_, [])] for id_ in ids]


def get_league_entries_by_team(teams):
    """
    Gets the leagues that the team(s) belong(s) to, including only the requested team(s)' entries

    Args:
        teams (Team | list<Team>): the team(s) to get leagues for

    Returns:
        list<League> | list<list<League>>: the leagues that the requested team(s) belong(s) to
    """
    if isinstance(teams, list):
        return __get_league_entries_by_team_id([team.id for team in teams])
    else:
        return __get_league_entries_by_team_id(teams.id)
