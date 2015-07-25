import cassiopeia.dto.requests
import cassiopeia.type.dto.matchlist

# @param summoner_id # int # The ID of the summoner to get the match list for
# @param begin_index # int # The game index to start from
# @param begin_time # int # The begin time to use for fetching games specified as epoch milliseconds.
# @param end_time # int # The end time to use for fetching games specified as epoch milliseconds.
# @param champion_ids # list<int> or int # The champion ID(s) to limit the results to
# @param ranked_queue # list<str> or str # The ranked queue(s) to limit the results to ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")
# @param seasons # list<str> or str # The season(s) to limit the results to ("PRESEASON3", "SEASON3", "PRESEASON2014", "SEASON2014", "PRESEASON2015", "SEASON2015")
# @return # PlayerHistory # The match history for that summoner
def get_match_list(summoner_id, begin_index=0, begin_time=-1, end_time=0, champion_ids=None, ranked_queues=None, seasons=None):
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