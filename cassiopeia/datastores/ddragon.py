import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query

from ..data import Platform
from ..dto.staticdata.champion import ChampionDto, ChampionListDto
from ..dto.staticdata.mastery import MasteryDto, MasteryListDto
from ..dto.staticdata.rune import RuneDto, RuneListDto
from ..dto.staticdata.item import ItemDto, ItemListDto
from ..dto.staticdata.summonerspell import SummonerSpellDto, SummonerSpellListDto
from ..dto.staticdata.version import VersionListDto
from ..dto.staticdata.profileicon import ProfileIconDataDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.realm import RealmDto
from ..dto.staticdata.map import MapDto, MapListDto
from .common import HTTPClient, HTTPError
from .riotapi.staticdata import _get_latest_version
from .uniquekeys import _hash_included_data, convert_region_to_platform

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class DDragon(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._cache = {ChampionListDto: {}, RuneListDto: {}, MasteryListDto: {}, ItemListDto: {}, SummonerSpellListDto: {}, MapListDto: {}}

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    def calculate_hash(self, query):
        hash = list(value for _, value in sorted(query.items()))
        for i, value in enumerate(hash):
            if isinstance(value, set):
                hash[i] = _hash_included_data(value)
        return tuple(hash)

    #############
    # Champions #
    #############

    _validate_get_champion_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(ChampionDto)
    @validate_query(_validate_get_champion_query, convert_region_to_platform)
    def get_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        champions_query = copy.deepcopy(query)
        if "id" in champions_query:
            champions_query.pop("id")
        if "name" in champions_query:
            champions_query.pop("name")
        champions = context[context.Keys.PIPELINE].get(ChampionListDto, query=champions_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of champion data instances
        if "id" in query:
            find = "id", query["id"]
        elif "name" in query:
            find = "name", query["name"]
        else:
            raise RuntimeError("Impossible!")
        champion = find_matching_attribute(champions["data"].values(), *find)
        if champion is None:
            raise NotFoundError
        champion["region"] = query["platform"].region.value
        champion["version"] = query["version"]
        if "locale" in query:
            champion["locale"] = query["locale"]
        if "includedData" in query:
            champion["includedData"] = query["includedData"]
        return ChampionDto(champion)

    _validate_get_champion_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(ChampionListDto)
    @validate_query(_validate_get_champion_list_query, convert_region_to_platform)
    def get_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[ChampionListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/championFull.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        for champ_name, champ in body["data"].items():
            champ = ChampionDto(champ)
            body["data"][champ_name] = champ
            champ["region"] = query["platform"].region.value
            body["locale"] = locale
            body["includedData"] = {"all"}

            champ["id"], champ["key"] = int(champ["key"]), champ["id"]

            for skin in champ["skins"]:
                # id str in DDragon, int in static data.
                skin["id"] = int(skin["id"])
                # Doesn't exist in static data.
                skin.pop("chromas", None)

            champ["passive"]["sanitizedDescription"] = champ["passive"]["description"]

            for recommended in champ['recommended']:
                # These fields always(?) are the same and don't appear in static data.
                [recommended.pop(key, None) for key in
                 ('sortrank', 'extensionPage', 'customPanel', 'customTag', 'requiredPerk', 'customPanelCurrencyType',
                  'customPanelBuffCurrencyName')]

                for block in recommended['blocks']:
                    # These don't appear in static data for whatever reason.
                    [block.pop(key, None) for key in
                     ("recSteps", "minSummonerLevel", "maxSummonerLevel", "showIfSummonerSpell", "hideIfSummonerSpell")]

                    for item in block["items"]:
                        # id str in DDragon, int in static data.
                        item["id"] = int(item["id"])
                        # Doesn't exist.
                        item.pop("hideCount", None)

            for spell in champ['spells']:
                # id -> key
                spell["key"] = spell.pop("id")
                # effectBurn is null in DDragon, empty string in static data.
                spell["effectBurn"][0] = ""
                # TODO: Sanitizer?
                spell["sanitizedDescription"] = spell["description"]
                spell["sanitizedTooltip"] = spell["tooltip"]
                # non-existent in static data(? used for charge based spells, not sure why static data strips it)
                spell.pop("maxammo", None)

                for var in spell["vars"]:
                    # coeff is always a list, even if just one item
                    if not isinstance(var["coeff"], list):
                        var["coeff"] = [var["coeff"]]

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        body["dataById"] = True
        result = ChampionListDto(body)
        self._cache[ChampionListDto][ahash] = result
        return result

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    @get.register(VersionListDto)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        return VersionListDto({
            "region": query["platform"].region.value,
            "versions": body
        })

    ##########
    # Realms #
    ##########

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    @get.register(RealmDto)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RealmDto:
        region = query["platform"].region
        url = "https://ddragon.leagueoflegends.com/realms/{region}.json".format(region=region.value.lower())
        try:
            body = self._client.get(url)[0]

        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        return RealmDto(body)

    #############
    # Languages #
    #############

    _validate_get_languages_query = Query. \
        has("platform").as_(Platform)

    @get.register(LanguagesDto)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_languages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        data = {"region": query["platform"].region.value, "languages": body}
        return LanguagesDto(data)

    ########
    # Maps #
    ########

    _validate_get_map_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale")

    @get.register(MapDto)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapDto:
        maps_query = copy.deepcopy(query)
        if "id" in maps_query:
            maps_query.pop("id")
        if "name" in maps_query:
            maps_query.pop("name")
        maps = context[context.Keys.PIPELINE].get(MapListDto, query=maps_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of map data instances
        if "id" in query:
            find = "mapId", str(query["id"])
        elif "name" in query:
            find = "mapName", query["name"]
        else:
            raise RuntimeError("Impossible!")
        map = find_matching_attribute(maps["data"].values(), *find)
        if map is None:
            raise NotFoundError
        map["region"] = query["platform"].region.value
        map["version"] = query["version"]
        if "locale" in query:
            map["locale"] = query["locale"]
        return MapDto(map)

    _validate_get_map_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(MapListDto)
    @validate_query(_validate_get_map_list_query, convert_region_to_platform)
    def get_map_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[MapListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/map.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        for key, map in body["data"].items():
            map = MapDto(map)
            body["data"][key] = map
            map["mapName"] = map.pop("MapName")
            map["mapId"] = map.pop("MapId")
        result = MapListDto(body)
        self._cache[MapListDto][ahash] = result
        return result

    ####################
    # Language Strings #
    ####################

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(LanguageStringsDto)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStringsDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/language.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        return LanguageStringsDto(body)

    #############
    # Masteries #
    #############

    _validate_get_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(MasteryDto)
    @validate_query(_validate_get_mastery_query, convert_region_to_platform)
    def get_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasteryDto:
        masteries_query = copy.deepcopy(query)
        if "id" in masteries_query:
            masteries_query.pop("id")
        if "name" in masteries_query:
            masteries_query.pop("name")
        masteries = context[context.Keys.PIPELINE].get(MasteryListDto, query=masteries_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of mastery data instances
        if "id" in query:
            find = "id", query["id"]
        elif "name" in query:
            find = "name", query["name"]
        else:
            raise RuntimeError("Impossible!")
        mastery = find_matching_attribute(masteries["data"].values(), *find)
        if mastery is None:
            raise NotFoundError
        mastery["region"] = query["platform"].region.value
        mastery["version"] = query["version"]
        if "locale" in query:
            mastery["locale"] = query["locale"]
        if "includedData" in query:
            mastery["includedData"] = query["includedData"]
        return MasteryDto(mastery)

    _validate_get_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(MasteryListDto)
    @validate_query(_validate_get_mastery_list_query, convert_region_to_platform)
    def get_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasteryListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[MasteryListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/mastery.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        mastery_map = {}  # mastery ID -> tree name mapping. Supplied by static data but not DDragon.

        # Fix tree structure to match static data.
        for tree in body["tree"]:
            for x, tier in enumerate(body["tree"][tree]):
                for mastery in tier:
                    # In DDragon, masteryId is a str whereas in static data it is an int.
                    mastery_id = int(mastery["masteryId"])
                    mastery["masteryId"] = mastery_id
                    mastery_map[mastery_id] = tree
                # Each tier in the static data mastery tree is encapsulated by a single item dictionary.
                body["tree"][tree][x] = {"masteryTreeItems": tier}

        # Add fields not provided by DDragon
        for key, mastery in body["data"].items():
            mastery = MasteryDto(mastery)
            body["data"][key] = mastery
            mastery["masteryTree"] = mastery_map[mastery["id"]]
            # TODO: Sanitizer?
            mastery["sanitizedDescription"] = mastery["description"]

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        result = MasteryListDto(body)
        self._cache[MasteryListDto][ahash] = result
        return result

    #########
    # Runes #
    #########

    _validate_get_rune_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(RuneDto)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneDto:
        runes_query = copy.deepcopy(query)
        if "id" in runes_query:
            runes_query.pop("id")
        if "name" in runes_query:
            runes_query.pop("name")
        runes = context[context.Keys.PIPELINE].get(RuneListDto, query=runes_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of rune data instances
        if "id" in query:
            find = "id", query["id"]
        elif "name" in query:
            find = "name", query["name"]
        else:
            raise RuntimeError("Impossible!")
        rune = find_matching_attribute(runes["data"].values(), *find)
        if rune is None:
            raise NotFoundError
        rune["region"] = query["platform"].region.value
        rune["version"] = query["version"]
        if "locale" in query:
            rune["locale"] = query["locale"]
        if "includedData" in query:
            rune["includedData"] = query["includedData"]
        return RuneDto(rune)

    _validate_get_rune_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(RuneListDto)
    @validate_query(_validate_get_rune_list_query, convert_region_to_platform)
    def get_rune_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[RuneListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/rune.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body.pop("basic")

        for rune_id, rune in body["data"].items():
            rune = RuneDto(rune)
            body["data"][rune_id] = rune
            rune["id"] = int(rune_id)
            # TODO: Sanitizer?
            rune["sanitizedDescription"] = rune["description"]
            # Some DDragon stats begin with "r", but they don"t in static data.
            rune["stats"] = {k.strip("r"): v for k, v in rune["stats"].items()}
            # isrune on DDragon is isRune on static data.
            rune["rune"]["isRune"] = rune["rune"].pop("isrune")
            # colloq and plaintext are always(?) null, and don"t appear in static data.
            rune.pop("colloq")
            rune.pop("plaintext")

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        result = RuneListDto(body)
        self._cache[RuneListDto][ahash] = result
        return result

    #########
    # Items #
    #########

    _validate_get_item_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(ItemDto)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemDto:
        items_query = copy.deepcopy(query)
        if "id" in items_query:
            items_query.pop("id")
        if "name" in items_query:
            items_query.pop("name")
        items = context[context.Keys.PIPELINE].get(ItemListDto, query=items_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of item data instances
        if "id" in query:
            find = "id", query["id"]
        elif "name" in query:
            find = "name", query["name"]
        else:
            raise RuntimeError("Impossible!")
        item = find_matching_attribute(items["data"].values(), *find)
        if item is None:
            raise NotFoundError
        item["region"] = query["platform"].region.value
        item["version"] = query["version"]
        if "locale" in query:
            item["locale"] = query["locale"]
        if "includedData" in query:
            item["includedData"] = query["includedData"]
        return ItemDto(item)

    _validate_get_item_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(ItemListDto)
    @validate_query(_validate_get_item_list_query, convert_region_to_platform)
    def get_item_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[ItemListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/item.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body.pop("basic")

        for group in body["groups"]:
            # key in static data -> id on DDragon
            group["key"] = group.pop("id")

        for item_id, item in body["data"].items():
            item = ItemDto(item)
            body["data"][item_id] = item
            item["id"] = int(item_id)
            # TODO: Sanitizer?
            item["sanitizedDescription"] = item["description"]
            if item["id"] == 3632:  # This item doesn't have a name.
                item["name"] = ""
            if "tags" not in item:
                item["tags"] = []
            if "depth" not in item:
                item["depth"] = 1
            if "colloq" not in item:
                item["colloq"] = ""
            if "plaintext" not in item:
                item["plaintext"] = ""

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        result = ItemListDto(body)
        self._cache[ItemListDto][ahash] = result
        return result

    ###################
    # Summoner Spells #
    ###################

    _validate_get_summoner_spell_query = Query. \
        has("platform").as_(Platform).also. \
        has("id").as_(int).or_("name").as_(str).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(SummonerSpellDto)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellDto:
        summoner_spells_query = copy.deepcopy(query)
        if "id" in summoner_spells_query:
            summoner_spells_query.pop("id")
        if "name" in summoner_spells_query:
            summoner_spells_query.pop("name")
        summoner_spells = context[context.Keys.PIPELINE].get(SummonerSpellListDto, query=summoner_spells_query)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        # The `data` is a list of summoner_spell data instances
        if "id" in query:
            find = "id", query["id"]
        elif "name" in query:
            find = "name", query["name"]
        else:
            raise RuntimeError("Impossible!")
        summoner_spell = find_matching_attribute(summoner_spells["data"].values(), *find)
        if summoner_spell is None:
            raise NotFoundError
        summoner_spell["region"] = query["platform"].region.value
        summoner_spell["version"] = query["version"]
        if "locale" in query:
            summoner_spell["locale"] = query["locale"]
        if "includedData" in query:
            summoner_spell["includedData"] = query["includedData"]
        return SummonerSpellDto(summoner_spell)

    _validate_get_summoner_spell_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(SummonerSpellListDto)
    @validate_query(_validate_get_summoner_spell_list_query, convert_region_to_platform)
    def get_summoner_spell_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellListDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale
        query["locale"] = locale

        ahash = self.calculate_hash(query)
        try:
            return self._cache[SummonerSpellListDto][ahash]
        except KeyError:
            pass

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/summoner.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        for ss_name, ss in body["data"].items():
            ss = SummonerSpellDto(ss)
            body["data"][ss_name] = ss
            # key and id are switched between DDragon and static data. Also, id is of type int, instead of str.
            ss["id"], ss["key"] = int(ss["key"]), ss["id"]
            # effectBurn"s first element is an null in DDragon, but an empty string in static data..
            ss["effectBurn"][0] = ""
            # Usually -1, doesn"t exist in static data.
            ss.pop("maxammo")
            # TODO: Sanitizer?
            ss["sanitizedDescription"] = ss["description"]
            ss["sanitizedTooltip"] = ss["tooltip"]

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        result = SummonerSpellListDto(body)
        self._cache[SummonerSpellListDto][ahash] = result
        return result

    #################
    # Profile Icons #
    #################

    _validate_get_profile_icon_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(ProfileIconDataDto)
    @validate_query(_validate_get_profile_icon_query, convert_region_to_platform)
    def get_profile_icon(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "https://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/profileicon.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = self._client.get(url)[0]
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        return ProfileIconDataDto(body)
