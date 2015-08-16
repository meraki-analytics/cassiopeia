import cassiopeia.dto.requests
import cassiopeia.type.dto.matchhistory

def get_match_history(summoner_id, begin_index=0, champion_ids=None, ranked_queues=None):
    """https://developer.riotgames.com/api/methods#!/1012/3438

    summoner_id      int                the ID of the summoner to get the match history for
    begin_index      int                the game index to start from (default 0)
    champion_ids     int | list<int>    the champion ID(s) to limit the results to (default None)
    ranked_queues    str | list<str>    the ranked queue(s) to limit the results to ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5") (default None)

    return           PlayerHistory      the summoner's match history
    """
    request = "{version}/matchhistory/{summoner_id}".format(version=cassiopeia.dto.requests.api_versions["matchhistory"], summoner_id=summoner_id)

    params = {
        "beginIndex": begin_index,
        "endIndex": begin_index + 15
    }
    if(champion_ids):
        params["championIds"] = ",".join(champion_ids) if isinstance(champion_ids, list) else str(champion_ids)
    if(ranked_queues):
        params["rankedQueues"] = ",".join(ranked_queues) if isinstance(ranked_queues, list) else str(ranked_queues)

    return cassiopeia.type.dto.matchhistory.PlayerHistory(cassiopeia.dto.requests.get(request, params))