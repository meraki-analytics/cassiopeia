from cassiopeia.dto.staticdataapi import get_languages, get_versions
import cassiopeia.riotapi
import cassiopeia.dto.staticdataapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.staticdata

_ignore_items = {0, 1080, 2037, 2039, 2040, 3005, 3039, 3123, 3128, 3131, 3160, 3166, 3167, 3168, 3169, 3175, 3176, 3171, 3186, 3188, 3205, 3206, 3207, 3209, 3210, 3405, 3406, 3407, 3408, 3409, 3410, 3411, 3412, 3413, 3414, 3415, 3416, 3417, 3419, 3420}
_ignore_runes = {8028}
_ignore_summoner_spells = {10}

# @param id_ # int # The ID of the champion to get
# @return # cassiopeia.type.core.staticdata.Champion # The champion
def get_champion_by_id(id_):
    champion = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Champion, id_, "id")
    if(champion):
        return champion

    champion = cassiopeia.dto.staticdataapi.get_champion(id_)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        ids = champion.item_ids
        cassiopeia.riotapi.get_items(list(ids)) if ids else None

    champion = cassiopeia.type.core.staticdata.Champion(champion)
    cassiopeia.core.requests.data_store.store(champion, id_)
    return champion

# @param name # str # The name of the champion to get
# @return # cassiopeia.type.core.staticdata.Champion # The champion
def get_champion_by_name(name):
    champions = get_champions()
    for champion in champions:
        if(champion.name == name):
            return champion
    return None

# @return # list<cassiopeia.type.core.staticdata.Champion> # All champions in the game
def get_champions():
    if(cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Champion)):
        return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Champion)

    champions = cassiopeia.dto.staticdataapi.get_champions()

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        ids = champions.item_ids
        cassiopeia.riotapi.get_items(list(ids)) if ids else None

    champions = [cassiopeia.type.core.staticdata.Champion(champ[1]) for champ in champions.data.items()]
    cassiopeia.core.requests.data_store.store(champions, [champ.id for champ in champions], [cassiopeia.type.core.staticdata.Champion])
    return champions

# @param ids # list<int> # The IDs of the champions to get
# @return # list<cassiopeia.type.core.staticdata.Champion> # The champions
def get_champions_by_id(ids):
    get_champions()
    return cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Champion, ids, "id")

# @param names # list<str> # The names of the champions to get
# @return # list<cassiopeia.type.core.staticdata.Champion> # The champions
def get_champions_by_name(names):
    indices = {names[i]: i for i in range(len(names))}
    
    champions = get_champions()
    results = [None for _ in range(len(names))]
    for champion in champions:
        try:
            index = indices[champion.name]
            results[index] = champion
        except(KeyError):
            pass

    return results

# @param id_ # int # The ID of the item to get
# @return # cassiopeia.type.core.staticdata.Item # The item
def get_item(id_):
    if(id_ in _ignore_items):
        return None

    item = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Item, id_, "id")
    if(item):
        return item

    item = cassiopeia.dto.staticdataapi.get_item(id_)
    item = cassiopeia.type.core.staticdata.Item(item)

    cassiopeia.core.requests.data_store.store(item, id_)
    return item

# @param ids # list<int> # The list of ids to limit results to
# @return # list<cassiopeia.type.core.staticdata.Item> # The requested items (or all if no ids are provided)
def get_items(ids=None):
    if(ids):
        get_items()
        return cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Item, ids, "id")
    else:
        if(cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Item)):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Item)

        items = cassiopeia.dto.staticdataapi.get_items()
        items = [cassiopeia.type.core.staticdata.Item(item[1]) for item in items.data.items()]

        cassiopeia.core.requests.data_store.store(items, [item.id for item in items], [cassiopeia.type.core.staticdata.Item])
        return items

# @return # dict<str, str> # The locale-based string replacements for various game constants
def get_language_strings():
    return cassiopeia.dto.staticdataapi.get_language_strings().data

# @return # list<cassiopeia.type.core.staticdata.MapDetails> # Specific information about each map
def get_map_information():
    return [cassiopeia.type.core.staticdata.MapDetails(map_[1]) for map_ in cassiopeia.dto.staticdataapi.get_maps().data.items()]

# @param id_ # int # The ID of the mastery to get
# @return # cassiopeia.type.core.staticdata.Mastery # The mastery
def get_mastery(id_):
    mastery = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Mastery, id_, "id")
    if(mastery):
        return mastery

    mastery = cassiopeia.dto.staticdataapi.get_mastery(id_)
    mastery = cassiopeia.type.core.staticdata.Mastery(mastery)

    cassiopeia.core.requests.data_store.store(mastery, id_)
    return mastery

# @param ids # list<int> # The list of ids to limit results to
# @return # list<cassiopeia.type.core.staticdata.Mastery> # The requested masteries (or all if no ids are provided)
def get_masteries(ids=None):
    if(ids):
        get_masteries()
        return cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Mastery, ids, "id")
    else:
        if(cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Mastery)):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Mastery)

        masteries = cassiopeia.dto.staticdataapi.get_masteries()
        masteries = [cassiopeia.type.core.staticdata.Mastery(mastery[1]) for mastery in masteries.data.items()]

        cassiopeia.core.requests.data_store.store(masteries, [mastery.id for mastery in masteries], [cassiopeia.type.core.staticdata.Mastery])
        return masteries

# @return # cassiopeia.type.core.staticdata.Realm # The realm for the current region
def get_realm():
    return cassiopeia.type.core.staticdata.Realm(cassiopeia.dto.staticdataapi.get_realm())

# @param id_ # int # The ID of the rune to get
# @return # cassiopeia.type.core.staticdata.Rune # The rune
def get_rune(id_):
    if(id_ in _ignore_runes):
        return None

    rune = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Rune, id_, "id")
    if(rune):
        return rune

    rune = cassiopeia.dto.staticdataapi.get_rune(id_)
    rune = cassiopeia.type.core.staticdata.Rune(rune)

    cassiopeia.core.requests.data_store.store(rune, id_)
    return rune

# @param ids # list<int> # The list of ids to limit results to
# @return # list<cassiopeia.type.core.staticdata.Rune> # The requested runes (or all if no ids are provided)
def get_runes(ids=None):
    if(ids):
        get_runes()
        return cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.Rune, ids, "id")
    else:
        if(cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.Rune)):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.Rune)

        runes = cassiopeia.dto.staticdataapi.get_runes()
        runes = [cassiopeia.type.core.staticdata.Rune(rune[1]) for rune in runes.data.items()]

        cassiopeia.core.requests.data_store.store(runes, [rune.id for rune in runes], [cassiopeia.type.core.staticdata.Rune])
        return runes

# @param id_ # int # The ID of the summoner spell to get
# @return # cassiopeia.type.core.staticdata.SummonerSpell # The summoner spell
def get_summoner_spell(id_):
    if(id_ in _ignore_summoner_spells):
        return None

    summoner_spell = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.SummonerSpell, id_, "id")
    if(summoner_spell):
        return summoner_spell

    summoner_spell = cassiopeia.dto.staticdataapi.get_summoner_spell(id_)
    summoner_spell = cassiopeia.type.core.staticdata.SummonerSpell(summoner_spell)

    cassiopeia.core.requests.data_store.store(summoner_spell, id_)
    return summoner_spell

# @param ids # list<int> # The list of ids to limit results to
# @return # list<cassiopeia.type.core.staticdata.SummonerSpell> # The requested summoner spells (or all if no ids are provided)
def get_summoner_spells(ids=None):
    if(ids):
        get_summoner_spells()
        return cassiopeia.core.requests.data_store.get(cassiopeia.type.core.staticdata.SummonerSpell, ids, "id")
    else:
        if(cassiopeia.core.requests.data_store.has_all(cassiopeia.type.core.staticdata.SummonerSpell)):
            return cassiopeia.core.requests.data_store.get_all(cassiopeia.type.core.staticdata.SummonerSpell)

        summoner_spells = cassiopeia.dto.staticdataapi.get_summoner_spells()
        summoner_spells = [cassiopeia.type.core.staticdata.SummonerSpell(summoner_spell[1]) for summoner_spell in summoner_spells.data.items()]

        cassiopeia.core.requests.data_store.store(summoner_spells, [summoner_spell.id for summoner_spell in summoner_spells], [cassiopeia.type.core.staticdata.SummonerSpell])
        return summoner_spells