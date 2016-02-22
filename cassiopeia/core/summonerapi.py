import cassiopeia.riotapi
import cassiopeia.dto.summonerapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.summoner


def __get_mastery_pages_by_id(ids):
    pages = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_masteries, 40, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        mastery_ids = set()
        for page in pages.values():
            mastery_ids |= page.mastery_ids
        cassiopeia.riotapi.get_masteries() if mastery_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.summoner.MasteryPage(page) for page in pages[str(ids)].pages]
    else:
        return [[cassiopeia.type.core.summoner.MasteryPage(page) for page in pages[str(id_)].pages] for id_ in ids]


def get_mastery_pages(summoners):
    """
    Get the mastery pages for (a) summoner(s).

    Args:
        ids (Summoner | list<Summoner>): the summoner(s) to get mastery pages for

    Returns:
        list<MasteryPage> | list<list<MasteryPage>>: the requested summoner(s)' mastery pages
    """
    if isinstance(summoners, list):
        return __get_mastery_pages_by_id([summoner.id for summoner in summoners])
    else:
        return __get_mastery_pages_by_id(summoners.id)


def __get_rune_pages_by_id(ids):
    pages = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_runes, 40, ids)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        rune_ids = set()
        for page in pages.values():
            rune_ids |= page.rune_ids
        cassiopeia.riotapi.get_runes() if rune_ids else None

    if not isinstance(ids, list):
        return [cassiopeia.type.core.summoner.RunePage(page) for page in pages[str(ids)].pages]
    else:
        return [[cassiopeia.type.core.summoner.RunePage(page) for page in pages[str(id_)].pages] for id_ in ids]


def get_rune_pages(summoners):
    """
    Get the rune pages for (a) summoner(s).

    Args:
        ids (Summoner | list<Summoner>): the summoner(s) to get rune pages for

    Returns:
        list<RunePage> | list<list<RunePage>>: the requested summoner(s)' rune pages
    """
    if isinstance(summoners, list):
        return __get_rune_pages_by_id([summoner.id for summoner in summoners])
    else:
        return __get_rune_pages_by_id(summoners.id)


def get_summoner_by_id(id_):
    """
    Gets a summoner by ID

    Args:
        id_ (int): the ID of the summoner

    Returns:
        Summoner: the summoner
    """
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, id_, "id")
    if summoner:
        return summoner

    try:
        summoner = cassiopeia.dto.summonerapi.get_summoners_by_id(id_)[str(id_)]
        summoner = cassiopeia.type.core.summoner.Summoner(summoner)
    except KeyError:
        return None

    cassiopeia.core.requests.data_store.store(summoner, id_)
    cassiopeia.core.requests.data_store.store(summoner, summoner.name)
    return summoner


def get_summoner_by_name(name):
    """
    Gets a summoner by name

    Args:
        name (str): the name of the summoner

    Returns:
        Summoner: the summoner
    """
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, name, "name")
    if summoner:
        return summoner

    try:
        summoner = cassiopeia.dto.summonerapi.get_summoners_by_name(name)[__standardize(name)]
        summoner = cassiopeia.type.core.summoner.Summoner(summoner)
    except KeyError:
        return None

    cassiopeia.core.requests.data_store.store(summoner, name)
    cassiopeia.core.requests.data_store.store(summoner, summoner.id)
    return summoner


def get_summoners_by_id(ids):
    """
    Gets a bunch of summoners by ID

    Args:
        ids (list<int>): the IDs of the summoners

    Returns:
        list<Summoner>: the summoners
    """
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, ids, "id")

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if not summoners[i]:
            missing.append(ids[i])
            loc.append(i)

    if not missing:
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoners_by_id, 40, missing)
    to_store = []
    for i in range(len(missing)):
        try:
            summoner = cassiopeia.type.core.summoner.Summoner(new[str(missing[i])])
            to_store.append(summoner)
        except KeyError:
            summoner = None
        summoners[loc[i]] = summoner

    cassiopeia.core.requests.data_store.store(to_store, [summoner.id for summoner in to_store])
    cassiopeia.core.requests.data_store.store(to_store, [summoner.name for summoner in to_store])
    return summoners


def get_summoners_by_name(names):
    """
    Gets a bunch of summoners by name

    Args:
        names (list<str>): the names of the summoners

    Returns:
        list<Summoner>: the summoners
    """
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, names, "name")

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(names)):
        if not summoners[i]:
            missing.append(names[i])
            loc.append(i)

    if not missing:
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoners_by_name, 40, missing)
    to_store = []
    for i in range(len(missing)):
        try:
            summoner = cassiopeia.type.core.summoner.Summoner(new[__standardize(missing[i])])
            to_store.append(summoner)
        except KeyError:
            summoner = None
        summoners[loc[i]] = summoner

    cassiopeia.core.requests.data_store.store(to_store, [summoner.id for summoner in to_store])
    cassiopeia.core.requests.data_store.store(to_store, [summoner.name for summoner in to_store])
    return summoners


def get_summoner_name(id_):
    """
    Gets the name of a summoner by ID

    Args:
        id_ (id): the summoner's ID

    Returns:
        str: the summoner's name
    """
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, id_, "id")
    if summoner:
        return summoner.name

    return cassiopeia.dto.summonerapi.get_summoner_names(id_)[str(id_)]


def get_summoner_names(ids):
    """
    Gets the names of a bunch of summoners by ID

    Args:
        ids (list<id>): the summoners' IDs

    Returns:
        list<str>: the summoners' names
    """
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, ids, "id")
    summoners = [summoner.name if summoner else "" for summoner in summoners]

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if not summoners[i]:
            missing.append(ids[i])
            loc.append(i)

    if not missing:
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_names, 40, missing)
    for i in range(len(missing)):
        summoners[loc[i]] = new[str(missing[i])]

    return summoners


def __standardize(name):
    return name.replace(" ", "").lower()
