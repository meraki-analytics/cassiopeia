import datetime

import cassiopeia.riotapi
import cassiopeia.dto.matchlistapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.matchlist

# @param summoner # cassiopeia.type.core.summoner.Summoner # The summoner to get the match list for
# @param begin_index # int # The game index to start from
# @param begin_time # datetime or int # The begin time to use for fetching games
# @param end_time # datetime or int # The end time to use for fetching games
# @param champions # list<cassiopeia.type.core.staticdata.Champion> or cassiopeia.type.core.staticdata.Champion # The champion(s) to limit the results to
# @param ranked_queue # list<cassiopeia.type.core.common.Queue> or cassiopeia.type.core.common.Queue # The ranked queue(s) to limit the results to
# @param seasons # list<cassiopeia.type.core.common.Season> or cassiopeia.type.core.common.Season # The season(s) to limit the results to
# @return # list<cassiopeia.type.core.matchlist.MatchReference> # The match list for that summoner
def get_match_list(summoner, begin_index=0, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
    if(ranked_queues):
        for queue in ranked_queues:
            if queue not in cassiopeia.type.core.common.ranked_queues:
                raise ValueError("{queue} is not a ranked queue".format(queue=queue))

    # Convert core types to API-ready types
    if(isinstance(begin_time, datetime.datetime)):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = begin_time - epoch
        begin_time = delta.total_seconds() * 1000
    if(isinstance(end_time, datetime.datetime)):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = end_time - epoch
        end_time = delta.total_seconds() * 1000

    champion_ids = [champion.id for champion in champions] if champions else None
    queues = [queue.value for queue in ranked_queues] if ranked_queues else None
    seasons = [season.value for season in seasons] if seasons else None

    history = cassiopeia.dto.matchlistapi.get_match_list(summoner.id, begin_index, begin_time, end_time, champion_ids, queues, seasons)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_champions_by_id(list(history.champion_ids))

    return [cassiopeia.type.core.matchlist.MatchReference(ref) for ref in history.matches]