from cassiopeia import requests
from cassiopeia.type.dto.matchhistory import *

# @param summoner_id # int # The ID of the summoner to get the match history for
# @param champion_ids # list<int> or int # The champion ID(s) to limit the results to
# @param ranked_queue # list<str> or str # The ranked queue(s) to limit the results to ("RANKED_SOLO_5x5", "RANKED_TEAM_3x3", "RANKED_TEAM_5x5")
# @param begin_index # int # The game index to start from
# @return # PlayerHistory # The match history for that summoner
def get_match_history(summoner_id, begin_index=0, champion_ids=None, ranked_queues=None):
    request = "{version}/matchhistory/{summoner_id}".format(version=requests.api_versions["matchhistory"], summoner_id=summoner_id)

    params = {
        "beginIndex": begin_index,
        "endIndex": begin_index + 15
    }
    if(champion_ids):
        params["championIds"] = str(champion_ids).replace(" ", "")[1:-1] if isinstance(champion_ids, list) else str(champion_ids)
    if(ranked_queues):
        params["rankedQueues"] = str(ranked_queues).replace(" ", "")[1:-1] if isinstance(ranked_queues, list) else str(ranked_queues)

    return PlayerHistory(requests.get(request, params))