import datetime

import cassiopeia.riotapi
import cassiopeia.dto.matchlistapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.matchlist

def get_match_list(summoner, begin_index=-1, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
    """Gets a summoner's match history

    summoner        Summoner                     the summoner to get match history for
    begin_index     int                          the game index to start from (default -1)
    begin_time      int | datetime               the begin time to use for fetching games (default 0)
    end_time        int | datetime               the end time to use for fetching games (default 0)
    champions       Champion | list<Champion>    the champion(s) to limit the results to (default None)
    ranked_queue    Queue | list<Queue>          the ranked queue(s) to limit the results to (default None)
    seasons         Season | list<Season>        the season(s) to limit the results to (default None)

    return          list<MatchSummary>           the summoner's match history
    """
    if(ranked_queues):
        for queue in ranked_queues:
            if queue not in cassiopeia.type.core.common.ranked_queues:
                raise ValueError("{queue} is not a ranked queue".format(queue=queue))

    # Convert core types to API-ready types
    if(isinstance(begin_time, datetime.datetime)):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = begin_time - epoch
        begin_time = int(delta.total_seconds() * 1000)
    if(isinstance(end_time, datetime.datetime)):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = end_time - epoch
        end_time = int(delta.total_seconds() * 1000)

    champion_ids = [champion.id for champion in champions] if isinstance(champions, list) else champions.id if champions else None
    queues = [queue.value for queue in ranked_queues] if isinstance(ranked_queues, list) else ranked_queues.value if ranked_queues else None
    seasons = [season.value for season in seasons] if isinstance(seasons, list) else seasons.value if seasons else None

    history = cassiopeia.dto.matchlistapi.get_match_list(summoner.id, begin_index, begin_time, end_time, champion_ids, queues, seasons)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_champions() if history.champion_ids else None

    return [cassiopeia.type.core.matchlist.MatchReference(ref) for ref in history.matches]