import cassiopeia.dto.requests
import cassiopeia.type.dto.staticdata

_locale = None


def get_champion(id_):
    """
    https://developer.riotgames.com/api/methods#!/968/3322

    Args:
        id_ (int): the ID of the champion to get

    Returns:
        Champion: the champion
    """
    request = "{version}/champion/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"champData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Champion(cassiopeia.dto.requests.get(request, params, True))


def get_champions():
    """
    https://developer.riotgames.com/api/methods#!/968/3326

    Returns:
        ChampionList: all the champions
    """
    request = "{version}/champion".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"champData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.ChampionList(cassiopeia.dto.requests.get(request, params, True))


def get_item(id_):
    """
    https://developer.riotgames.com/api/methods#!/968/3319

    Args:
        id_ (int): the ID of the item to get

    Returns:
        Item: the item
    """
    request = "{version}/item/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"itemData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Item(cassiopeia.dto.requests.get(request, params, True))


def get_items():
    """
    https://developer.riotgames.com/api/methods#!/968/3314

    Returns:
        ItemList: all the items
    """
    request = "{version}/item".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"itemListData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.ItemList(cassiopeia.dto.requests.get(request, params, True))


def get_language_strings():
    """
    https://developer.riotgames.com/api/methods#!/968/3316

    Returns:
        LanguageStrings: the locale-based string replacements for various game constants
    """
    request = "{version}/language-strings".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.LanguageStrings(cassiopeia.dto.requests.get(request, params, True))


def get_languages():
    """
    https://developer.riotgames.com/api/methods#!/968/3324

    Returns:
        list<str>: the valid locale strings for the API
    """
    request = "{version}/languages".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.dto.requests.get(request, {}, True)


def get_maps():
    """
    https://developer.riotgames.com/api/methods#!/968/3328

    Returns:
        MapData: specific information about each map
    """
    request = "{version}/map".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.MapData(cassiopeia.dto.requests.get(request, params, True))


def get_mastery(id_):
    """
    https://developer.riotgames.com/api/methods#!/968/3318

    Args:
        id_ (int): the ID of the mastery to get

    Returns:
        Mastery: the mastery
    """
    request = "{version}/mastery/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"masteryData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Mastery(cassiopeia.dto.requests.get(request, params, True))


def get_masteries():
    """
    https://developer.riotgames.com/api/methods#!/968/3317

    Returns:
        MasteryList: all the masteries
    """
    request = "{version}/mastery".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"masteryListData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.MasteryList(cassiopeia.dto.requests.get(request, params, True))


def get_realm():
    """
    https://developer.riotgames.com/api/methods#!/968/3325

    Returns:
        Realm: the realm for the current region
    """
    request = "{version}/realm".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.type.dto.staticdata.Realm(cassiopeia.dto.requests.get(request, {}, True))


def get_rune(id_):
    """
    https://developer.riotgames.com/api/methods#!/968/3321

    Args:
        id_ (int): the ID of the rune to get

    Returns:
        Rune: the rune
    """
    request = "{version}/rune/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"runeData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.Rune(cassiopeia.dto.requests.get(request, params, True))


def get_runes():
    """
    https://developer.riotgames.com/api/methods#!/968/3315

    Returns:
        RuneList: all the runes
    """
    request = "{version}/rune".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"runeListData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.RuneList(cassiopeia.dto.requests.get(request, params, True))


def get_summoner_spell(id_):
    """
    https://developer.riotgames.com/api/methods#!/968/3320

    Args:
        id_ (int): the ID of the summoner spell to get

    Returns:
        SummonerSpell: the summoner spell
    """
    request = "{version}/summoner-spell/{id_}".format(version=cassiopeia.dto.requests.api_versions["staticdata"], id_=id_)

    params = {"spellData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.SummonerSpell(cassiopeia.dto.requests.get(request, params, True))


def get_summoner_spells():
    """
    https://developer.riotgames.com/api/methods#!/968/3327

    Returns:
        SummonerSpellList: all the summoner spells
    """
    request = "{version}/summoner-spell".format(version=cassiopeia.dto.requests.api_versions["staticdata"])

    params = {"spellData": "all"}
    if _locale:
        params["locale"] = _locale

    return cassiopeia.type.dto.staticdata.SummonerSpellList(cassiopeia.dto.requests.get(request, params, True))


def get_versions():
    """
    https://developer.riotgames.com/api/methods#!/968/3323

    Returns:
        list<str>: the valid API versions
    """
    request = "{version}/versions".format(version=cassiopeia.dto.requests.api_versions["staticdata"])
    return cassiopeia.dto.requests.get(request, {}, True)
