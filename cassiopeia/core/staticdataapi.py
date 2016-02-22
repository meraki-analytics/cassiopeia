import cassiopeia.riotapi
import cassiopeia.dto.staticdataapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.staticdata

_ignore_items = {0, 1080, 1304, 1309, 1314, 1319, 1324, 1329, 2004, 2037, 2039, 2040, 3005, 3039, 3123, 3128, 3131, 3160, 3166, 3167, 3168, 3169, 3175, 3176, 3171, 3186, 3188, 3205, 3206, 3207, 3209, 3210, 3244, 3405, 3406, 3407, 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3419, 3420}
_ignore_runes = {8028}
_ignore_summoner_spells = {10}


def get_champion_by_id(id_):
    """
    Gets a champion by ID

    Args:
        id_ (int): the ID of the champion to get

    Returns:
        Champion: the champion
    """
    champion = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Champion, id_, "id")
    if champion:
        return champion

    champion = cassiopeia.dto.staticdataapi.get_champion(id_)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_items() if champion.item_ids else None

    champion = cassiopeia.type.core.staticdata.Champion(champion)
    cassiopeia.core.requests.data_store.store(champion, id_)
    return champion


def get_champion_by_name(name):
    """
    Gets a champion by name

    Args:
        name (str): the name of the champion to get

    Returns:
        Champion: the champion
    """
    champions = get_champions()
    for champion in champions:
        if champion.name == name:
            return champion
    return None


def get_champions():
    """
    Gets all the champions

    Returns:
        list<Champion>: all the champions
    """
    if cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Champion):
        return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Champion)

    champions = cassiopeia.dto.staticdataapi.get_champions()

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_items() if champions.item_ids else None

    champions = [cassiopeia.type.core.staticdata.Champion(champ[1]) for champ in champions.data.items()]
    cassiopeia.core.requests.data_store.store(champions, [champ.id for champ in champions], [cassiopeia.type.core.staticdata.Champion])
    return champions


def get_champions_by_id(ids):
    """
    Gets a bunch of champions by ID

    Args:
        ids (list<int>): the IDs of the champions to get

    Returns:
        list<Champion>: the requested champions
    """
    champions = {champ.id: champ for champ in get_champions()}
    results = []
    for id_ in ids:
        try:
            champ = champions[id_]
        except KeyError:
            champ = None
        results.append(champ)
    return results


def get_champions_by_name(names):
    """
    Gets a bunch of champions by name

    Args:
        names (list<str>): the names of the champions to get

    Returns:
        list<Champion>: the requested champions
    """
    indices = {names[i]: i for i in range(len(names))}

    champions = get_champions()
    results = [None for _ in range(len(names))]
    for champion in champions:
        try:
            index = indices[champion.name]
            results[index] = champion
        except KeyError:
            pass

    return results


def get_item(id_):
    """
    Gets an item

    Args:
        id_ (int): the ID of the item to get

    Returns:
        Item: the item
    """
    if id_ in _ignore_items:
        return None

    item = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Item, id_, "id")
    if item:
        return item

    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        items = cassiopeia.riotapi.get_items()
        item = None
        for itm in items:
            if itm.id == id_:
                item = itm
                break
    else:
        item = cassiopeia.dto.staticdataapi.get_item(id_)
        item = cassiopeia.type.core.staticdata.Item(item)
        cassiopeia.core.requests.data_store.store(item, id_)

    return item


def get_items(ids=None):
    """
    Gets a bunch of items (or all of them)

    Args:
        ids (list<int>): the IDs of the items to get (or None to get all items) (default None)

    Returns:
        list<Item>: the items
    """
    if ids is not None:
        items = {item.id: item for item in get_items()}
        results = []
        for id_ in ids:
            try:
                item = items[id_]
            except KeyError:
                item = None
            results.append(item)
        return results
    else:
        if cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Item):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Item)

        items = cassiopeia.dto.staticdataapi.get_items()
        items = [cassiopeia.type.core.staticdata.Item(item[1]) for item in items.data.items()]

        cassiopeia.core.requests.data_store.store(items, [item.id for item in items], [cassiopeia.type.core.staticdata.Item])
        return items


def get_language_strings():
    """
    Gets the locale-based string replacements for various game constants

    Returns:
        return: dict<str, str>   the replacements
    """
    return cassiopeia.dto.staticdataapi.get_language_strings().data


def get_languages():
    """
    Gets the valid locales (languages) that can be used with the API

    Returns:
        list<str>: the valid locales
    """
    return cassiopeia.dto.staticdataapi.get_languages()


def get_map_information():
    """
    Gets specific information about each map

    Returns:
        list<MapDetails>: the map information
    """
    return [cassiopeia.type.core.staticdata.MapDetails(map_[1]) for map_ in cassiopeia.dto.staticdataapi.get_maps().data.items()]


def get_mastery(id_):
    """
    Gets a mastery

    Args:
        id_ (int): the ID of the mastery to get

    Returns:
        Mastery: the mastery
    """
    mastery = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Mastery, id_, "id")
    if mastery:
        return mastery

    mastery = cassiopeia.dto.staticdataapi.get_mastery(id_)

    # Load required data if loading policy is eager
    if cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager:
        cassiopeia.riotapi.get_masteries() if mastery.mastery_ids else None

    mastery = cassiopeia.type.core.staticdata.Mastery(mastery)

    cassiopeia.core.requests.data_store.store(mastery, id_)
    return mastery


def get_masteries(ids=None):
    """
    Gets a bunch of masteries (or all of them)

    Args:
        ids (list<int>): the IDs of the masteries to get (or None to get all masteries) (default None)

    Returns:
        list<Mastery>: the masteries
    """
    if ids is not None:
        masteries = {mastery.id: mastery for mastery in get_masteries()}
        results = []
        for id_ in ids:
            try:
                mastery = masteries[id_]
            except KeyError:
                mastery = None
            results.append(mastery)
        return results
    else:
        if cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Mastery):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Mastery)

        masteries = cassiopeia.dto.staticdataapi.get_masteries()
        masteries = [cassiopeia.type.core.staticdata.Mastery(mastery[1]) for mastery in masteries.data.items()]

        cassiopeia.core.requests.data_store.store(masteries, [mastery.id for mastery in masteries], [cassiopeia.type.core.staticdata.Mastery])
        return masteries


def get_realm():
    """
    Gets the realm for the current region

    Returns:
        Realm: the realm
    """
    return cassiopeia.type.core.staticdata.Realm(cassiopeia.dto.staticdataapi.get_realm())


def get_rune(id_):
    """
    Gets a rune

    Args:
        id_ (int): the ID of the rune to get

    Returns:
        Rune: the rune
    """
    if id_ in _ignore_runes:
        return None

    rune = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Rune, id_, "id")
    if rune:
        return rune

    rune = cassiopeia.dto.staticdataapi.get_rune(id_)
    rune = cassiopeia.type.core.staticdata.Rune(rune)

    cassiopeia.core.requests.data_store.store(rune, id_)
    return rune


def get_runes(ids=None):
    """
    Gets a bunch of runes (or all of them)

    Args:
        ids (list<int>): the IDs of the runes to get (or None to get all runes) (default None)

    Returns:
        list<Rune>: the runes
    """
    if ids is not None:
        runes = {rune.id: rune for rune in get_runes()}
        results = []
        for id_ in ids:
            try:
                rune = runes[id_]
            except KeyError:
                rune = None
            results.append(rune)
        return results
    else:
        if cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Rune):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Rune)

        runes = cassiopeia.dto.staticdataapi.get_runes()
        runes = [cassiopeia.type.core.staticdata.Rune(rune[1]) for rune in runes.data.items()]

        cassiopeia.core.requests.data_store.store(runes, [rune.id for rune in runes], [cassiopeia.type.core.staticdata.Rune])
        return runes


def get_summoner_spell(id_):
    """
    Gets a summoner spell

    Args:
        id_ (int): the ID of the summoner spell to get

    Returns:
        SummonerSpell: the summoner spell
    """
    if id_ in _ignore_summoner_spells:
        return None

    summoner_spell = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.SummonerSpell, id_, "id")
    if summoner_spell:
        return summoner_spell

    summoner_spell = cassiopeia.dto.staticdataapi.get_summoner_spell(id_)
    summoner_spell = cassiopeia.type.core.staticdata.SummonerSpell(summoner_spell)

    cassiopeia.core.requests.data_store.store(summoner_spell, id_)
    return summoner_spell


def get_summoner_spells(ids=None):
    """
    Gets a bunch of summoner spells (or all of them)

    Args:
        ids (list<int>): the IDs of the summoner spells to get (or None to get all summoner spells) (default None)

    Returns:
        list<SummonerSpell>: the summoner spells
    """
    if ids is not None:
        summoner_spells = {summoner_spell.id: summoner_spell for summoner_spell in get_summoner_spells()}
        results = []
        for id_ in ids:
            try:
                summoner_spell = summoner_spells[id_]
            except KeyError:
                summoner_spell = None
            results.append(summoner_spell)
        return results
    else:
        if cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.SummonerSpell):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.SummonerSpell)

        summoner_spells = cassiopeia.dto.staticdataapi.get_summoner_spells()
        summoner_spells = [cassiopeia.type.core.staticdata.SummonerSpell(summoner_spell[1]) for summoner_spell in summoner_spells.data.items()]

        cassiopeia.core.requests.data_store.store(summoner_spells, [summoner_spell.id for summoner_spell in summoner_spells], [cassiopeia.type.core.staticdata.SummonerSpell])
        return summoner_spells


def get_versions():
    """
    Gets the valid versions of the API

    Returns:
        list<str>: the valid versions
    """
    return cassiopeia.dto.staticdataapi.get_versions()
