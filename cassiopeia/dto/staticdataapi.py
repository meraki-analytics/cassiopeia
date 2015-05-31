from cassiopeia import requests
from cassiopeia.type.dto.staticdata import *

_locale = None

# @param locale # str # The locale to use for returned text. Use get_languages() to find valid locales.
def set_locale(locale):
    _locale = locale

# @param id_ # int # The ID of the champion to get
# @return # Champion # The champion
def get_champion(id_):
    request = "{version}/champion/{id_}".format(version=requests.api_versions["staticdata"], id_=id_)

    params = {"champData": "all"}
    if(_locale):
        params["locale"] = _locale

    return Champion(requests.get(request, params, True))

# @return # ChampionList # All the champions
def get_champions():
    request = "{version}/champion".format(version=requests.api_versions["staticdata"])

    params = {"champData": "all"}
    if(_locale):
        params["locale"] = _locale

    return ChampionList(requests.get(request, params, True))

# @param id_ # int # The ID of the item to get
# @return # Item # The item
def get_item(id_):
    request = "{version}/item/{id_}".format(version=requests.api_versions["staticdata"], id_=id_)

    params = {"itemData": "all"}
    if(_locale):
        params["locale"] = _locale

    return Item(requests.get(request, params, True))

# @return # ItemList # All the items
def get_items():
    request = "{version}/item".format(version=requests.api_versions["staticdata"])

    params = {"itemListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return ChampionList(requests.get(request, params, True))

# @return # LanguageStrings # The locale-based string replacements for various game constants
def get_language_strings():
    request = "{version}/language-strings".format(version=requests.api_versions["staticdata"])

    params = {}
    if(_locale):
        params["locale"] = _locale

    return LanguageStrings(requests.get(request, params, True))

# @return # list<str> # The valid locale strings for the API
def get_languages():
    request = "{version}/languages".format(version=requests.api_versions["staticdata"])
    return requests.get(request, {}, True)

# @return # MapData # Specific information about each map
def get_maps():
    request = "{version}/map".format(version=requests.api_versions["staticdata"])

    params = {}
    if(_locale):
        params["locale"] = _locale

    return MapData(requests.get(request, params, True))

# @param id_ # int # The ID of the mastery to get
# @return # Mastery # The mastery
def get_mastery(id_):
    request = "{version}/mastery/{id_}".format(version=requests.api_versions["staticdata"], id_=id_)

    params = {"masteryData": "all"}
    if(_locale):
        params["locale"] = _locale

    return Mastery(requests.get(request, params, True))

# @return # MasteryList # All the masteries and associated metadata
def get_masteries():
    request = "{version}/mastery".format(version=requests.api_versions["staticdata"])

    params = {"masteryListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return MasteryList(requests.get(request, params, True))

# @return # Realm # The realm for the current region
def get_realm():
    request = "{version}/realm".format(version=requests.api_versions["staticdata"])
    return Realm(requests.get(request, {}, True))

# @param id_ # int # The ID of the rune to get
# @return # Rune # The rune
def get_rune(id_):
    request = "{version}/rune/{id_}".format(version=requests.api_versions["staticdata"], id_=id_)

    params = {"runeData": "all"}
    if(_locale):
        params["locale"] = _locale

    return Rune(requests.get(request, params, True))

# @return # RuneList # All the runes
def get_runes():
    request = "{version}/rune".format(version=requests.api_versions["staticdata"])

    params = {"runeListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return RuneList(requests.get(request, params, True))

# @param id_ # int # The ID of the summoner spell to get
# @return # SummonerSpell # The summoner spell
def get_summoner_spell(id_):
    request = "{version}/summoner-spell/{id_}".format(version=requests.api_versions["staticdata"], id_=id_)

    params = {"spellData": "all"}
    if(_locale):
        params["locale"] = _locale

    return SummonerSpell(requests.get(request, params, True))

# @return # SummonerSpellList # All the summoner spells
def get_summoner_spells():
    request = "{version}/summoner-spell".format(version=requests.api_versions["staticdata"])

    params = {"spellData": "all"}
    if(_locale):
        params["locale"] = _locale

    return SummonerSpellList(requests.get(request, params, True))

# @return # list<str> # The valid API versions
def get_versions():
    request = "{version}/versions".format(version=requests.api_versions["staticdata"])
    return requests.get(request, {}, True)