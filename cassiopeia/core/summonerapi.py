import urllib.parse

import cassiopeia.riotapi
import cassiopeia.dto.summonerapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.core.summoner

# @param ids # list<int> or int # The summoner ID(s) to get mastery pages for
# @return # list<list<cassiopeia.type.core.summoner.MasteryPage>> or list<cassiopeia.type.core.summoner.MasteryPage> # The requested mastery pages
def __get_mastery_pages_by_id(ids):
    pages = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_masteries, 40, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_masteries(list(pages.mastery_ids))

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.summoner.MasteryPage(page) for page in pages[str(ids)].pages]
    else:
        return [[cassiopeia.type.core.summoner.MasteryPage(page) for page in pages[str(id_)].pages] for id_ in ids]

# @param ids # list<int> or int # The summoner ID(s) to get mastery pages for
# @return # list<list<cassiopeia.type.core.summoner.MasteryPage>> or list<cassiopeia.type.core.summoner.MasteryPage> # The requested mastery pages
def get_mastery_pages(summoners):
    if(isinstance(summoners, list)):
        return __get_mastery_pages_by_id([summoner.id for summoner in summoners])
    else:
        return __get_mastery_pages_by_id(summoners.id)

# @param ids # list<int> or int # The summoner ID(s) to get rune pages for
# @return # list<list<cassiopeia.type.core.summoner.RunePage>> or list<cassiopeia.type.core.summoner.RunePage> # The requested rune pages
def __get_rune_pages_by_id(ids):
    pages = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_runes, 40, ids)

    # Load required data if loading policy is eager
    if(cassiopeia.core.requests.load_policy is cassiopeia.type.core.common.LoadPolicy.eager):
        cassiopeia.riotapi.get_runes(list(pages.rune_ids))

    if(not isinstance(ids, list)):
        return [cassiopeia.type.core.summoner.RunePage(page) for page in pages[str(ids)].pages]
    else:
        return [[cassiopeia.type.core.summoner.RunePage(page) for page in pages[str(id_)].pages] for id_ in ids]

# @param ids # list<int> or int # The summoner ID(s) to get rune pages for
# @return # list<list<cassiopeia.type.core.summoner.RunePage>> or list<cassiopeia.type.core.summoner.RunePage> # The requested rune pages
def get_rune_pages(summoners):
    if(isinstance(summoners, list)):
        return __get_rune_pages_by_id([summoner.id for summoner in summoners])
    else:
        return __get_rune_pages_by_id(summoners.id)

# @param id_ # int # The ID of the summoner to get
# @return # cassiopeia.type.core.summoner.Summoner # The summoner
def get_summoner_by_id(id_):
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, id_, "id")
    if(summoner):
        return summoner

    summoner = cassiopeia.dto.summonerapi.get_summoners_by_id(id_)[str(id_)]
    summoner = cassiopeia.type.core.summoner.Summoner(summoner)

    cassiopeia.core.requests.data_store.store(summoner, id_)
    cassiopeia.core.requests.data_store.store(summoner, summoner.name)
    return summoner

# @param name # str # The name of the summoner to get
# @return # cassiopeia.type.core.summoner.Summoner # The summoner
def get_summoner_by_name(name):
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, name, "name")
    if(summoner):
        return summoner

    summoner = cassiopeia.dto.summonerapi.get_summoners_by_name(urllib.parse.quote(name))[__standardize(name)]
    summoner = cassiopeia.type.core.summoner.Summoner(summoner)

    cassiopeia.core.requests.data_store.store(summoner, name)
    cassiopeia.core.requests.data_store.store(summoner, summoner.id)
    return summoner

# @param ids # list<int> # The IDs of the summoners to get
# @return # list<cassiopeia.type.core.summoner.Summoner> # The summoners
def get_summoners_by_id(ids):
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, ids, "id")

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if(not summoners[i]):
            missing.append(ids[i])
            loc.append(i)

    if(not missing):
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoners_by_id, 40, missing)
    for i in range(len(missing)):
        summoner = cassiopeia.type.core.summoner.Summoner(new[str(missing[i])])
        summoners[loc[i]] = summoner
        missing[i] = summoner

    cassiopeia.core.requests.data_store.store(missing, [summoner.id for summoner in missing])
    cassiopeia.core.requests.data_store.store(missing, [summoner.name for summoner in missing])
    return summoners

# @param names # list<str> # The names of the summoners to get
# @return # list<cassiopeia.type.core.summoner.Summoner> # The summoners
def get_summoners_by_name(names):
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, names, "name")

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(names)):
        if(not summoners[i]):
            missing.append(names[i])
            loc.append(i)

    if(not missing):
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoners_by_name, 40, [urllib.parse.quote(name) for name in missing])
    for i in range(len(missing)):
        summoner = cassiopeia.type.core.summoner.Summoner(new[__standardize(missing[i])])
        summoners[loc[i]] = summoner
        missing[i] = summoner

    cassiopeia.core.requests.data_store.store(missing, [summoner.id for summoner in missing])
    cassiopeia.core.requests.data_store.store(missing, [summoner.name for summoner in missing])
    return summoners

# @param id_ # int # The summoner ID to get name for
# @return # str # The summoner's name
def get_summoner_name(id_):
    summoner = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, id_, "id")
    if(summoner):
        return summoner.name

    return cassiopeia.dto.summonerapi.get_summoner_names(id_)[str(id_)]

# @param ids # list<int> # The summoner IDs to get names for
# @return # list<str> # The summoners' names
def get_summoner_names(ids):
    summoners = cassiopeia.core.requests.data_store.get(cassiopeia.type.core.summoner.Summoner, ids, "id")
    summoners = [summoner.name if summoner else "" for summoner in summoners]

    # Find which summoners weren't cached
    missing = []
    loc = []
    for i in range(len(ids)):
        if(not summoners[i]):
            missing.append(ids[i])
            loc.append(i)

    if(not missing):
        return summoners

    # Make requests to get them
    new = cassiopeia.core.requests.call_with_ensured_size(cassiopeia.dto.summonerapi.get_summoner_names, 40, missing)
    for i in range(len(missing)):
        summoners[loc[i]] = new[str(missing[i])]

    return summoners

# @param name # str # A summoner name
# @return # str # The standardized version of the name
def __standardize(name):
    return name.replace(" ", "").lower()