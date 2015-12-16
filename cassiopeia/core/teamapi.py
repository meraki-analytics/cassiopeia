import cassiopeia.riotapi
import cassiopeia.dto.teamapi
import cassiopeia.core.requests
import cassiopeia.type.core.team


def get_teams_by_summoner(summoners):
    """Gets (a) summoner(s)' teams

    summoners    Summoner | list<Summoner>        the summoner(s) to get teams for

    return       list<Team> | list<list<Team>>    the summoner(s)' teams
    """
    ids = [summoner.id for summoner in summoners] if isinstance(summoners, list) else summoners.id
    teams = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.teamapi.get_teams_by_summoner_id, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        for _, lst in teams.items():
            for team in lst:
                summoner_ids |= team.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.team.Team(team) for team in teams[str(ids)]]
    else:
        return [[cassiopeia.type.core.team.Team(team) for team in teams[str(id_)]] for id_ in ids]


def get_team(id_):
    """Gets a team by ID

    id_       str     the ID of the team

    return    Team    the team
    """
    team = cassiopeia.dto.teamapi.get_teams_by_id(id_)[id_]

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = team.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None

    return cassiopeia.type.core.team.Team(team)


def get_teams(ids):
    """Gets teams by ID

    ids       list<str>     the IDs of the teams

    return    list<Team>    the teams
    """
    teams = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.teamapi.get_teams_by_id, 10, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        summoner_ids = set()
        for _, team in teams.items():
            summoner_ids |= team.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None

    return [cassiopeia.type.core.team.Team(teams[id_]) for id_ in ids]
