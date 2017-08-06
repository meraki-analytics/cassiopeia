import json
from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from ..data import Platform
from ..dto.staticdata.champion import ChampionListDto
from ..dto.staticdata.mastery import MasteryListDto
from ..dto.staticdata.rune import RuneListDto
from ..dto.staticdata.item import ItemListDto
from ..dto.staticdata.summonerspell import SummonerSpellListDto
from ..dto.staticdata.version import VersionListDto
from ..dto.staticdata.profileicon import ProfileIconDataDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.realm import RealmDto
from ..dto.staticdata.map import MapListDto

from .common import HTTPClient, HTTPError
from .riotapi.staticdata import _get_default_version

T = TypeVar("T")


class DDragonDataSource(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    #############
    # Champions #
    #############

    _validate_get_champion_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").also. \
        can_have("includedData")

    @get.register(ChampionListDto)
    def get_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        self._validate_get_champion_list_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/championFull.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        for champ_name, champ in body["data"].items():
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
        return ChampionListDto(body)

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    @get.register(VersionListDto)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        self._validate_get_versions_query(query, context)

        url = "https://ddragon.leagueoflegends.com/api/versions.json"
        try:
            body = json.loads(self._client.get(url)[0])
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
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RealmDto:
        self._validate_get_realms_query(query, context)

        region = query["platform"].region
        url = "https://ddragon.leagueoflegends.com/realms/{region}.json".format(region=region.value.lower())
        try:
            body = json.loads(self._client.get(url)[0])

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
    def get_languages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        self._validate_get_languages_query(query, context)

        url = "https://ddragon.leagueoflegends.com/cdn/languages.json"
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        data = {"region": query["platform"].region.value, "languages": body}
        return LanguagesDto(data)

    ########
    # Maps #
    ########

    _validate_get_map_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(MapListDto)
    def get_map_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapListDto:
        self._validate_get_map_list_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/map.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        for map in body["data"].values():
            map["mapName"] = map.pop("MapName")
            map["mapId"] = map.pop("MapId")
        return MapListDto(body)

    ####################
    # Language Strings #
    ####################

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(LanguageStringsDto)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStringsDto:
        self._validate_get_language_strings_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/language.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        return LanguageStringsDto(body)

    #############
    # Masteries #
    #############

    _validate_get_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(MasteryListDto)
    def get_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasteryListDto:
        self._validate_get_mastery_list_query(query,  context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/mastery.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
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
        for mastery in body["data"].values():
            mastery["masteryTree"] = mastery_map[mastery["id"]]
            # TODO: Sanitizer?
            mastery["sanitizedDescription"] = mastery["description"]

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}
        return MasteryListDto(body)

    #########
    # Runes #
    #########

    _validate_get_rune_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(RuneListDto)
    def get_rune_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneListDto:
        self._validate_get_rune_list_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/rune.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body.pop("basic")

        for rune_id, rune in body["data"].items():
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
        return RuneListDto(body)

    #########
    # Items #
    #########

    _validate_get_item_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(ItemListDto)
    def get_item_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemListDto:
        self._validate_get_item_list_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/item.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body.pop("basic")

        for group in body["groups"]:
            # key in static data -> id on DDragon
            group["key"] = group.pop("id")

        for item_id, item in body["data"].items():
            item["id"] = int(item_id)
            # TODO: Sanitizer?
            item["sanitizedDescription"] = item["description"]

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        body["includedData"] = {"all"}

        return ItemListDto(body)

    ###################
    # Summoner Spells #
    ###################

    _validate_get_summoner_spell_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData")

    @get.register(SummonerSpellListDto)
    def get_summoner_spell_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellListDto:
        self._validate_get_summoner_spell_list_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/summoner.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        for ss_name, ss in body["data"].items():
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
        return SummonerSpellListDto(body)

    #################
    # Profile Icons #
    #################

    _validate_get_profile_icon_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").as_(str)

    @get.register(ProfileIconDataDto)
    def get_profile_icon(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        self._validate_get_profile_icon_query(query, context)

        locale = query["locale"] if "locale" in query else query["platform"].default_locale

        url = "http://ddragon.leagueoflegends.com/cdn/{version}/data/{locale}/profileicon.json".format(
            version=query["version"],
            locale=locale
        )
        try:
            body = json.loads(self._client.get(url)[0])
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        body["region"] = query["platform"].region.value
        body["locale"] = locale
        return ProfileIconDataDto(body)
