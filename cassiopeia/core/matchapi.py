import cassiopeia.riotapi
import cassiopeia.dto.matchapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.match
import cassiopeia.type.core.matchlist


def get_match(id_, include_timeline=True, tournament_code=""):
    """
    Gets a match

    Args:
        id_ (int | MatchReference): the ID of or reference to the match to get
        include_timeline (bool): whether to include timeline data in the returned match
        tournament_code (str): the tournament code if the match to be retrieved is from a tournament

    Returns:
        Match: the match
    """
    if isinstance(id_, cassiopeia.type.core.matchlist.MatchReference):
        id_ = id_.id

    match = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.match.Match, id_, "matchId")
    if match and (match.timeline or not include_timeline):
        return match

    match = cassiopeia.dto.matchapi.get_match(id_, include_timeline, tournament_code)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_items() if match.item_ids else None
        cassiopeia.riotapi.get_champions() if match.champion_ids else None
        cassiopeia.riotapi.get_masteries() if match.mastery_ids else None
        cassiopeia.riotapi.get_runes() if match.rune_ids else None
        summoner_ids = match.summoner_ids
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_summoner_spells() if match.summoner_spell_ids else None

    match = cassiopeia.type.core.match.Match(match)
    cassiopeia.core.requests.data_store.store(match, id_)
    return match


def get_matches(ids, include_timeline=True, tournament_code=""):
    """
    Gets a bunch of matches

    Args:
        ids (list<int> | list<MatchReference>): the IDs of or references to the matches to get
        include_timeline (bool): whether to include timeline data in the returned matches
        tournament_code (str): the tournament code if the match to be retrieved is from a tournament

    Returns:
        list<Match>: the matches
    """
    ids = [ref.id if isinstance(ref, cassiopeia.type.core.matchlist.MatchReference) else ref for ref in ids]

    matches = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.match.Match, ids, "matchId")

    # Find which matches weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if not matches[i] or (include_timeline and not matches[i].timeline):
            missing.append(ids[i])
            loc.append(i)

    if not missing:
        return matches

    # Initialize eager loading variables appropriately
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        item_ids = set()
        champion_ids = set()
        mastery_ids = set()
        rune_ids = set()
        summoner_ids = set()
        summoner_spell_ids = set()

    # Make requests to get them
    for i in range(len(missing)):
        match = cassiopeia.type.core.match.Match(cassiopeia.dto.matchapi.get_match(missing[i], include_timeline, tournament_code))
        matches[loc[i]] = match
        missing[i] = match

        if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
            item_ids = item_ids | match.data.item_ids
            champion_ids = champion_ids | match.data.champion_ids
            mastery_ids = mastery_ids | match.data.mastery_ids
            rune_ids = rune_ids | match.data.rune_ids
            summoner_ids = summoner_ids | match.data.summoner_ids
            summoner_spell_ids = summoner_spell_ids | match.data.summoner_spell_ids

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_items() if item_ids else None
        cassiopeia.riotapi.get_champions() if champion_ids else None
        cassiopeia.riotapi.get_masteries() if mastery_ids else None
        cassiopeia.riotapi.get_runes() if rune_ids else None
        cassiopeia.riotapi.get_summoners_by_id(list(summoner_ids)) if summoner_ids else None
        cassiopeia.riotapi.get_summoner_spells() if summoner_spell_ids else None

    cassiopeia.core.requests.data_store.store(missing, [match.id for match in missing])
    return matches


def get_tournament_match_ids(tournament_code):
    """
    Gets the IDs for a tournament's matches

    Args:
        tournament_code (str): the tournament code

    Returns:
        list<int>: the match ids for the tournament
    """
    return cassiopeia.dto.matchapi.get_tournament_match_ids(tournament_code)
