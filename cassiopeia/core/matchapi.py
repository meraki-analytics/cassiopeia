import cassiopeia.riotapi
import cassiopeia.dto.matchapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.match
import cassiopeia.type.core.matchlist

# @param id_ # int or cassiopeia.type.core.matchlist.MatchReference # The match ID or reference to get
# @return # cassiopeia.type.core.match.Match # The match
def get_match(id_):
    if(isinstance(id_, cassiopeia.type.core.matchlist.MatchReference)):
        id_ = id_.id

    match = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.match.Match, id_, "matchId")
    if(match):
        return match

    match = cassiopeia.dto.matchapi.get_match(id_)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        ids = match.item_ids
        cassiopeia.riotapi.get_items(list(ids)) if ids else None
        ids = match.champion_ids
        cassiopeia.riotapi.get_champions_by_id(list(ids)) if ids else None
        ids = match.mastery_ids
        cassiopeia.riotapi.get_masteries(list(ids)) if ids else None
        ids = match.rune_ids
        cassiopeia.riotapi.get_runes(list(ids)) if ids else None
        ids = match.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(ids)) if ids else None
        ids = match.summoner_spell_ids
        cassiopeia.riotapi.get_summoner_spells(list(ids)) if ids else None

    match = cassiopeia.type.core.match.Match(match)
    cassiopeia.core.requests.data_store.store(match, id_)
    return match

# @param ids # list<int> or list<cassiopeia.type.core.matchlist.MatchReference> # The match IDs or references to get
# @return # list<cassiopeia.type.core.match.Match> # The matches
def get_matches(ids):
    ids = [ref.id if isinstance(ref, cassiopeia.type.core.matchlist.MatchReference) else ref for ref in ids]

    matches = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.match.Match, ids, "matchId")

    # Find which matches weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if(not matches[i]):
            missing.append(ids[i])
            loc.append(i)

    if(not missing):
        return matches

    # Initialize eager loading variables appropriately
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        item_ids = set()
        champion_ids = set()
        mastery_ids = set()
        rune_ids = set()
        summoner_ids = set()
        summoner_spell_ids = set()

    # Make requests to get them
    for i in range(len(missing)):
        match = cassiopeia.type.core.match.Match(cassiopeia.dto.matchapi.get_match(missing[i]))
        matches[loc[i]] = match
        missing[i] = match

        if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
            item_ids = item_ids | match.data.item_ids
            champion_ids = champion_ids | match.data.champion_ids
            mastery_ids = mastery_ids | match.data.mastery_ids
            rune_ids = rune_ids | match.data.rune_ids
            summoner_ids = summoner_ids | match.data.summoner_ids
            summoner_spell_ids = summoner_spell_ids | match.data.summoner_spell_ids

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_items(list(item_ids)) if item_ids else None
        cassiopeia.riotapi.get_champions_by_id(list(champion_ids)) if champion_ids else None
        cassiopeia.riotapi.get_masteries(list(mastery_ids)) if mastery_ids else None
        cassiopeia.riotapi.get_runes(list(rune_ids)) if rune_ids else None
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_summoner_spells(list(summoner_spell_ids)) if summoner_spell_ids else None

    cassiopeia.core.requests.data_store.store(missing, [match.id for match in missing])
    return matches