import cassiopeia.riotapi
import cassiopeia.dto.matchhistoryapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.matchhistory

def get_match_history(summoner, begin_index=0, champions=None, ranked_queues=None):
    """Gets a summoner's match history

    summoner        Summoner                     the summoner to get match history for
    begin_index     int                          the game index to start from (default 0)
    champions       Champion | list<Champion>    the champion(s) to limit the results to (default None)
    ranked_queue    Queue | list<Queue>          the ranked queue(s) to limit the results to (default None)

    return          list<MatchSummary>           the summoner's match history
    """
    if(ranked_queues):
        for queue in ranked_queues:
            if queue not in cassiopeia.type.core.common.ranked_queues:
                raise ValueError("{queue} is not a ranked queue".format(queue=queue))

    # Convert core types to API-ready types
    champion_ids = [champion.id for champion in champions] if champions else None
    queues = [queue.value for queue in ranked_queues] if ranked_queues else None

    history = cassiopeia.dto.matchhistoryapi.get_match_history(summoner.id, begin_index, champion_ids, queues)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        ids = history.item_ids
        cassiopeia.riotapi.get_items(list(ids)) if ids else None
        ids = history.champion_ids
        cassiopeia.riotapi.get_champions_by_id(list(ids)) if ids else None
        ids = history.mastery_ids
        cassiopeia.riotapi.get_masteries(list(ids)) if ids else None
        ids = history.rune_ids
        cassiopeia.riotapi.get_runes(list(ids)) if ids else None
        ids = history.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(ids)) if ids else None
        ids = history.summoner_spell_ids
        cassiopeia.riotapi.get_summoner_spells(list(ids)) if ids else None

    result = [cassiopeia.type.core.matchhistory.MatchSummary(summary) for summary in history.matches]
    result.reverse()
    return result