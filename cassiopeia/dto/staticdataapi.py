import cassiopeia.dto.requests
import cassiopeia.type.dto.staticdata

_locale = None

# @param locale # str # The locale to use for returned text. Use get_languages() to find valid locales.
def set_locale(locale):
    _locale = locale

# @param id_ # int # The ID of the champion to get
# @return # Champion # The champion
def get_champion(id_):
    request = "{version}/champion/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"champData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Champion(cassiopeia.dto.requests.get(request, params, True))

# @return # ChampionList # All the champions
def get_champions():
    request = "{version}/champion".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"champData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.ChampionList(cassiopeia.dto.requests.get(request, params, True))

# @param id_ # int # The ID of the item to get
# @return # Item # The item
def get_item(id_):
    request = "{version}/item/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"itemData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Item(cassiopeia.dto.requests.get(request, params, True))

# @return # ItemList # All the items
def get_items():
    request = "{version}/item".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"itemListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.ItemList(cassiopeia.dto.requests.get(request, params, True))

# @return # LanguageStrings # The locale-based string replacements for various game constants
def get_language_strings():
    request = "{version}/language-strings".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.LanguageStrings(cassiopeia.dto.requests.get(request, params, True))

# @return # list<str> # The valid locale strings for the API
def get_languages():
    request = "{version}/languages".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.dto.requests.get(request, {}, True)

# @return # MapData # Specific information about each map
def get_maps():
    request = "{version}/map".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.MapData(cassiopeia.dto.requests.get(request, params, True))

# @param id_ # int # The ID of the mastery to get
# @return # Mastery # The mastery
def get_mastery(id_):
    request = "{version}/mastery/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"masteryData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Mastery(cassiopeia.dto.requests.get(request, params, True))

# @return # MasteryList # All the masteries and associated metadata
def get_masteries():
    request = "{version}/mastery".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"masteryListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.MasteryList(cassiopeia.dto.requests.get(request, params, True))

# @return # Realm # The realm for the current region
def get_realm():
    request = "{version}/realm".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.type.dto.staticdata.Realm(cassiopeia.dto.requests.get(request, {}, True))

# @param id_ # int # The ID of the rune to get
# @return # Rune # The rune
def get_rune(id_):
    request = "{version}/rune/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"runeData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Rune(cassiopeia.dto.requests.get(request, params, True))

# @return # RuneList # All the runes
def get_runes():
    request = "{version}/rune".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"runeListData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.RuneList(cassiopeia.dto.requests.get(request, params, True))

# @param id_ # int # The ID of the summoner spell to get
# @return # SummonerSpell # The summoner spell
def get_summoner_spell(id_):
    request = "{version}/summoner-spell/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"spellData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.SummonerSpell(cassiopeia.dto.requests.get(request, params, True))

# @return # SummonerSpellList # All the summoner spells
def get_summoner_spells():
    request = "{version}/summoner-spell".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"spellData": "all"}
    if(_locale):
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.SummonerSpellList(cassiopeia.dto.requests.get(request, params, True))

# @return # list<str> # The valid API versions
def get_versions():
    request = "{version}/versions".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.dto.requests.get(request, {}, True)
