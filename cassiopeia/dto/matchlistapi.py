import cassiopeia.dto.requests
import cassiopeia.type.dto.matchlist

def get_match_list(summoner_id, begin_index=0, begin_time=-1, end_time=0, champion_ids=None, ranked_queues=None, seasons=None):
    """https://developer.riotgames.com/api/methods#!/1013/3439

    summoner_id      int                the ID of the summoner to get the match history for
    begin_index      int                the game index to start from (default 0)
    begin_time       int                the begin time to use for fetching games specified as epoch milliseconds (default -1)
    end_time         int                the end time to use for fetching games specified as epoch milliseconds (default 0)
    champion_ids     int | list<int>    the champion ID(s) to limit the results to (default None)
    ranked_queues    str | list<str>    the ranked queue(s) to limit the results to ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5") (default None)
    seasons          str | list<str>    the season(s) to limit the results to ("PRESEASON3", "SEASON3", "PRESEASON2014", "SEASON2014", "PRESEASON2015", "SEASON2015") (default None)

    return           MatchList          the summoner's match history
    """
    request = "{version}/matchlist/by-summoner/{summoner_id}".format(version=cassiopeia.dto.requests.api_versions["matchlist"], summoner_id=summoner_id)

    params = {}
    if(begin_index >= 0):
        params["beginIndex"] = begin_index
        params["endIndex"] = begin_index + 20
    if(begin_time):
        params["beginTime"] = begin_time
    if(end_time):
        params["endTime"] = end_time
    if(champion_ids):
        params["championIds"] = ",".join(champion_ids) if isinstance(champion_ids, list) else str(champion_ids)
    if(ranked_queues):
        params["rankedQueues"] = ",".join(ranked_queues) if isinstance(ranked_queues, list) else str(ranked_queues)
    if(seasons):
        params["seasons"] = ",".join(seasons) if isinstance(seasons, list) else str(seasons)

    return cassiopeia.type.dto.matchlist.MatchList(cassiopeia.dto.requests.get(request, params))