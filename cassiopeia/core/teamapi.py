import cassiopeia.riotapi
import cassiopeia.dto.teamapi
import cassiopeia.core.requests
import cassiopeia.type.core.team

# @param summoners # cassiopeia.type.core.summoner.Summoner or list<cassiopeia.type.core.summoner.Summoner> # The summoner(s) to look up teams for
# @return # list<cassiopeia.type.core.team.Team> or list<list<cassiopeia.type.core.team.Team>> # The summoner's teams
def get_teams_by_summoner(summoners):
    ids = [summoner.id for summoner in summoners] if isinstance(summoners, list) else summoners.id
    teams = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.teamapi.get_teams_by_summoner_id, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        for _, lst in teams.items():
            for team in lst:
                summoner_ids |= team.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.team.Team(team) for team in teams[str(ids)]]
    else:
        return [[cassiopeia.type.core.team.Team(team) for team in teams[str(id_)]] for id_ in ids]

# @param ids # str or list<str> # The team IDs to look up
# @return # list<cassiopeia.type.core.team.Team> or Team # The team(s)
def get_teams(ids):
    teams = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.teamapi.get_teams_by_id, 10, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        summoner_ids = set()
        for _, team in teams.items():
            summoner_ids |= team.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None

    if(not isinstance(ids, list)):
        return cassiopeia.type.core.team.Team(teams[ids])
    else:
        return [cassiopeia.type.core.team.Team(teams[id_]) for id_ in ids]