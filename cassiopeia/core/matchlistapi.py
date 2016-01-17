import datetime

import cassiopeia.riotapi
import cassiopeia.dto.matchlistapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.matchlist


def get_match_list(summoner, num_matches=0, begin_index=0, begin_time=0, end_time=0, champions=None, ranked_queues=None, seasons=None):
    """Gets a summoner's match history

    summoner        Summoner                     the summoner to get match history for
    num_matches     int                          the maximum number of matches to retrieve. 0 will get as many as possible. (default 0)
    begin_index     int                          the game index to start from (default 0)
    begin_time      int | datetime               the begin time to use for fetching games (default 0)
    end_time        int | datetime               the end time to use for fetching games (default 0)
    champions       Champion | list<Champion>    the champion(s) to limit the results to (default None)
    ranked_queues   Queue | list<Queue>          the ranked queue(s) to limit the results to (default None)
    seasons         Season | list<Season>        the season(s) to limit the results to (default None)

    return          list<MatchReference>         the summoner's match history
    """
    # Convert strings that should be enums into enums
    if isinstance(seasons, str):
        _seasons = cassiopeia.type.core.common.Season(seasons.upper())
    elif isinstance(seasons, list) and all(isinstance(s, str) for s in seasons):
        _seasons = [cassiopeia.type.core.common.Season(s.upper()) for s in seasons]
    else:
        _seasons = seasons

    if isinstance(ranked_queues, str):
        _ranked_queues = cassiopeia.type.core.common.Queue(ranked_queues.upper().replace('5X5', '5x5').replace('3X3', '3x3'))
    elif isinstance(ranked_queues, list) and all(isinstance(q, str) for q in ranked_queues):
        _ranked_queues = [cassiopeia.type.core.common.Queue(q.upper().replace('5X5', '5x5').replace('3X3', '3x3')) for q in ranked_queues]
    else:
        _ranked_queues = ranked_queues

    if _ranked_queues and isinstance(_ranked_queues, list):
        for queue in _ranked_queues:
            if queue not in cassiopeia.type.core.common.ranked_queues:
                raise ValueError("{queue} is not a ranked queue".format(queue=queue))
    elif _ranked_queues:
        if _ranked_queues not in cassiopeia.type.core.common.ranked_queues:
            raise ValueError("{queue} is not a ranked queue".format(queue=_ranked_queues))

    # Convert core types to API-ready types
    if isinstance(begin_time, datetime.datetime):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = begin_time - epoch
        begin_time = int(delta.total_seconds() * 1000)
    if isinstance(end_time, datetime.datetime):
        epoch = datetime.datetime.utcfromtimestamp(0)
        delta = end_time - epoch
        end_time = int(delta.total_seconds() * 1000)

    champion_ids = [champion.id for champion in champions] if isinstance(champions, list) else champions.id if champions else None
    _ranked_queues = [queue.value for queue in _ranked_queues] if isinstance(_ranked_queues, list) else _ranked_queues.value if _ranked_queues else None
    _seasons = [season.value for season in _seasons] if isinstance(_seasons, list) else _seasons.value if _seasons else None

    history = cassiopeia.dto.matchlistapi.get_match_list(summoner.id, num_matches, begin_index, begin_time, end_time, champion_ids, _ranked_queues, _seasons)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_champions() if history.champion_ids else None

    return [cassiopeia.type.core.matchlist.MatchReference(ref) for ref in history.matches]
