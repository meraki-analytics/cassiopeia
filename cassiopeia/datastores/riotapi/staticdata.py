import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.staticdata.champion import ChampionDto, ChampionListDto
from ...dto.staticdata.rune import RuneDto, RuneListDto
from ...dto.staticdata.item import ItemDto, ItemListDto
from ...dto.staticdata.summonerspell import SummonerSpellDto, SummonerSpellListDto
from ...dto.staticdata.version import VersionListDto
from ...dto.staticdata.map import MapDto, MapListDto
from ...dto.staticdata.realm import RealmDto
from ...dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ...dto.staticdata.profileicon import ProfileIconDataDto
from ..uniquekeys import _hash_included_data, convert_region_to_platform

T = TypeVar("T")


def _get_latest_version(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    realms = pipeline.get(RealmDto, {"platform": query["platform"]})
    return realms["v"]


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class StaticDataAPI(RiotAPIService):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ChampionDto)
    @validate_query(_validate_get_champion_query, convert_region_to_platform)
    def get_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        if self._request_by_id or "id" not in query:  # Get by champion list
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

            if "id" in query:
                champion = find_matching_attribute(champions["data"].values(), "id", query["id"])
            elif "name" in query:
                champion = find_matching_attribute(champions["data"].values(), "name", query["name"])
            else:
                raise ValueError("Impossible!")
            if champion is None:
                raise NotFoundError
            champion["region"] = query["platform"].region.value
            champion["version"] = query["version"]
            champion["locale"] = query["locale"]
            champion["includedData"] = query["includedData"]
            return ChampionDto(champion)
        else:
            params = {
                "version": query["version"],
                "locale": query["locale"],
                "tags": ",".join(list(query["includedData"]))
            }

            url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
            try:
                data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/champion"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["region"] = query["platform"].region.value
            data["version"] = query["version"]
            data["locale"] = query["locale"]
            data["includedData"] = query["includedData"]
            return ChampionDto(data)

    _validate_get_many_champion_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(ChampionDto)
    @validate_query(_validate_get_many_champion_query, convert_region_to_platform)
    def get_many_champion(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionDto, None, None]:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"])),
            "dataById": True
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/champion"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        def generator():
            for id in query["ids"]:
                try:
                    champion = data["data"][str(id)]
                except KeyError as error:
                    raise NotFoundError("No champion exists with id \"{id}\"".format(id=id)) from error

                champion["region"] = query["platform"].region.value
                champion["version"] = data["version"]
                champion["locale"] = query["locale"]
                champion["includedData"] = query["includedData"]
                yield ChampionDto(champion)

        return generator()

    _validate_get_champion_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"}).also. \
        can_have("dataById").with_default(True)

    @get.register(ChampionListDto)
    @validate_query(_validate_get_champion_list_query, convert_region_to_platform)
    def get_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"])),
            "dataById": query["dataById"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/champions"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["version"] = query["version"]
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        data["dataById"] = query["dataById"]
        for key, champion in data["data"].items():
            champion = ChampionDto(champion)
            data["data"][key] = champion
            champion["region"] = query["platform"].region.value
            champion["version"] = query["version"]
            champion["locale"] = query["locale"]
            champion["includedData"] = query["includedData"]
        result = ChampionListDto(data)
        return result

    _validate_get_many_champion_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"}).also. \
        can_have("dataById").with_default(True)

    @get_many.register(ChampionListDto)
    @validate_query(_validate_get_many_champion_list_query, convert_region_to_platform)
    def get_many_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionListDto, None, None]:
        params = {
            "tags": ",".join(list(query["includedData"])),
            "dataById": query["dataById"]
        }

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/champions"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["version"] = query["version"]
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                data["dataById"] = query["dataById"]
                for key, champion in data["data"].items():
                    champion = ChampionDto(champion)
                    data["data"][key] = champion
                    champion["region"] = query["platform"].region.value
                    champion["version"] = query["version"]
                    champion["locale"] = query["locale"]
                    champion["includedData"] = query["includedData"]
                yield ChampionListDto(data)

        return generator()

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    @get.register(VersionListDto)
    @validate_query(_validate_get_versions_query, convert_region_to_platform)
    def get_versions(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/versions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "staticdata/versions"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return VersionListDto({
            "region": query["platform"].region.value,
            "versions": data
        })

    #########
    # Runes #
    #########

    _validate_get_rune_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(RuneDto)
    @validate_query(_validate_get_rune_query, convert_region_to_platform)
    def get_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneDto:
        if self._request_by_id or "id" not in query:  # Get by rune list
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

            if "id" in query:
                rune = find_matching_attribute(runes["data"].values(), "id", query["id"])
            elif "name" in query:
                rune = find_matching_attribute(runes["data"].values(), "name", query["name"])
            else:
                raise ValueError("Impossible!")
            if rune is None:
                raise NotFoundError
            rune["region"] = query["platform"].region.value
            rune["version"] = query["version"]
            rune["locale"] = query["locale"]
            rune["includedData"] = query["includedData"]
            return RuneDto(rune)
        else:
            params = {
                "version": query["version"],
                "locale": query["locale"],
                "tags": ",".join(list(query["includedData"]))
            }

            url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
            try:
                data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/rune"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["region"] = query["platform"].region.value
            data["version"] = query["version"]
            data["locale"] = query["locale"]
            data["includedData"] = query["includedData"]
            return RuneDto(data)

    _validate_get_many_rune_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(RuneDto)
    @validate_query(_validate_get_many_rune_query, convert_region_to_platform)
    def get_many_rune(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[RuneDto, None, None]:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/rune"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        def generator():
            for id in query["ids"]:
                try:
                    rune = data["data"][str(id)]
                except KeyError as error:
                    raise NotFoundError("No rune exists with id \"{id}\"".format(id=id)) from error

                rune["region"] = query["platform"].region.value
                rune["version"] = data["version"]
                rune["locale"] = query["locale"]
                rune["includedData"] = query["includedData"]
                yield RuneDto(rune)

        return generator()

    _validate_get_rune_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(RuneListDto)
    @validate_query(_validate_get_rune_list_query, convert_region_to_platform)
    def get_rune_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RuneListDto:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/runes"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        for key, rune in data["data"].items():
            rune = RuneDto(rune)
            data["data"][key] = rune
            rune["region"] = query["platform"].region.value
            rune["version"] = query["version"]
            rune["locale"] = query["locale"]
            rune["includedData"] = query["includedData"]
        result = RuneListDto(data)
        return result

    _validate_get_many_rune_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(RuneListDto)
    @validate_query(_validate_get_many_rune_list_query, convert_region_to_platform)
    def get_many_rune_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[RuneListDto, None, None]:
        params = {
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/runes"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                for key, rune in data["data"].items():
                    rune = RuneDto(rune)
                    data["data"][key] = rune
                    rune["region"] = query["platform"].region.value
                    rune["version"] = query["version"]
                    rune["locale"] = query["locale"]
                    rune["includedData"] = query["includedData"]
                yield RuneListDto(data)

        return generator()

    #########
    # Items #
    #########

    _validate_get_item_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemDto)
    @validate_query(_validate_get_item_query, convert_region_to_platform)
    def get_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemDto:
        if self._request_by_id or "id" not in query:  # Get by item list
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

            if "id" in query:
                item = find_matching_attribute(items["data"].values(), "id", query["id"])
            elif "name" in query:
                item = find_matching_attribute(items["data"].values(), "name", query["name"])
            else:
                raise ValueError("Impossible!")
            if item is None:
                raise NotFoundError
            item["region"] = query["platform"].region.value
            item["version"] = query["version"]
            item["locale"] = query["locale"]
            item["includedData"] = query["includedData"]
            return ItemDto(item)
        else:
            params = {
                "version": query["version"],
                "locale": query["locale"],
                "tags": ",".join(list(query["includedData"]))
            }

            url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
            try:
                data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/item"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["region"] = query["platform"].region.value
            data["version"] = query["version"]
            data["locale"] = query["locale"]
            data["includedData"] = query["includedData"]
            if data["id"] == 3632:  # This item doesn't have a name.
                data["name"] = ""
            if "tags" not in data:
                data["tags"] = []
            if "depth" not in data:
                data["depth"] = 1
            if "colloq" not in data:
                data["colloq"] = ""
            if "plaintext" not in data:
                data["plaintext"] = ""
            return ItemDto(data)

    _validate_get_many_item_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(ItemDto)
    @validate_query(_validate_get_many_item_query, convert_region_to_platform)
    def get_many_item(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ItemDto, None, None]:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/item"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        def generator():
            for id in query["ids"]:
                try:
                    item = data["data"][str(id)]
                except KeyError as error:
                    raise NotFoundError("No item exists with id \"{id}\"".format(id=id)) from error

                item["region"] = query["platform"].region.value
                item["version"] = data["version"]
                item["locale"] = query["locale"]
                item["includedData"] = query["includedData"]
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
                yield ItemDto(item)

        return generator()

    _validate_get_item_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemListDto)
    @validate_query(_validate_get_item_list_query, convert_region_to_platform)
    def get_item_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ItemListDto:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/items"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        for key, item in data["data"].items():
            item = ItemDto(item)
            data["data"][key] = item
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
            item["region"] = query["platform"].region.value
            item["version"] = query["version"]
            item["locale"] = query["locale"]
            item["includedData"] = query["includedData"]
        result = ItemListDto(data)
        return result

    _validate_get_many_item_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(ItemListDto)
    @validate_query(_validate_get_many_item_list_query, convert_region_to_platform)
    def get_many_item_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ItemListDto, None, None]:
        params = {
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/items"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                for key, item in data["data"].items():
                    item = ItemDto(item)
                    data["data"][key] = item
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
                yield ItemListDto(data)

        return generator()

    ########
    # Maps #
    ########

    _validate_get_map_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(MapDto)
    @validate_query(_validate_get_map_query, convert_region_to_platform)
    def get_map(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapDto:
        if self._request_by_id or "id" not in query:  # Get by map list
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

            if "id" in query:
                map = find_matching_attribute(maps["data"].values(), "mapId", query["id"])
            elif "name" in query:
                map = find_matching_attribute(maps["data"].values(), "mapName", query["name"])
            else:
                raise ValueError("Impossible!")
            if map is None:
                raise NotFoundError
            map["region"] = query["platform"].region.value
            map["version"] = query["version"]
            map["locale"] = query["locale"]
            return MapDto(map)

    _validate_get_map_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(MapListDto)
    @validate_query(_validate_get_map_list_query, convert_region_to_platform)
    def get_map_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MapListDto:
        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/maps".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/maps"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        for key, map in data["data"].items():
            map = MapDto(map)
            data["data"][key] = map
        result = MapListDto(data)
        return result

    ###################
    # Summoner Spells #
    ###################

    _validate_get_summoner_spell_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_latest_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(SummonerSpellDto)
    @validate_query(_validate_get_summoner_spell_query, convert_region_to_platform)
    def get_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellDto:
        if self._request_by_id or "id" not in query:  # Get by summoner spell list
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

            if "id" in query:
                summoner_spell = find_matching_attribute(summoner_spells["data"].values(), "id", query["id"])
            elif "name" in query:
                summoner_spell = find_matching_attribute(summoner_spells["data"].values(), "name", query["name"])
            else:
                raise ValueError("Impossible!")
            if summoner_spell is None:
                raise NotFoundError
            summoner_spell["region"] = query["platform"].region.value
            summoner_spell["version"] = query["version"]
            summoner_spell["locale"] = query["locale"]
            summoner_spell["includedData"] = query["includedData"]
            return SummonerSpellDto(summoner_spell)
        else:
            params = {
                "version": query["version"],
                "locale": query["locale"],
                "tags": ",".join(list(query["includedData"]))
            }

            url = "https://{platform}.api.riotgames.com/lol/static-data/v3/summoner-spells/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
            try:
                data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/summoner-spell"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["region"] = query["platform"].region.value
            data["version"] = query["version"]
            data["locale"] = query["locale"]
            data["includedData"] = query["includedData"]
            return SummonerSpellDto(data)

    _validate_get_many_summoner_spell_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(SummonerSpellDto)
    @validate_query(_validate_get_many_summoner_spell_query, convert_region_to_platform)
    def get_many_summoner_spell(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpellDto, None, None]:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/summoner-spells".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/summoner-spell"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        def generator():
            for id in query["ids"]:
                try:
                    summoner_spell = data["data"][id]
                except KeyError as error:
                    raise NotFoundError("No summoner spell exists with id \"{id}\"".format(id=id)) from error

                summoner_spell["region"] = query["platform"].region.value
                summoner_spell["version"] = data["version"]
                summoner_spell["locale"] = query["locale"]
                summoner_spell["includedData"] = query["includedData"]
                yield SummonerSpellDto(summoner_spell)

        return generator()

    _validate_get_summoner_spell_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(SummonerSpellListDto)
    @validate_query(_validate_get_summoner_spell_list_query, convert_region_to_platform)
    def get_summoner_spell_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerSpellListDto:
        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/summoner-spells".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/summoner-spells"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        for key, summoner_spell in data["data"].items():
            summoner_spell = SummonerSpellDto(summoner_spell)
            data["data"][key] = summoner_spell
            summoner_spell["region"] = query["platform"].region.value
            summoner_spell["version"] = query["version"]
            summoner_spell["locale"] = query["locale"]
            summoner_spell["includedData"] = query["includedData"]
        result = SummonerSpellListDto(data)
        return result

    _validate_get_many_summoner_spell_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(SummonerSpellListDto)
    @validate_query(_validate_get_many_summoner_spell_list_query, convert_region_to_platform)
    def get_many_summoner_spell_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpellListDto, None, None]:
        params = {
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/summoner-spells".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/summoner-spells"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                for key, summoner_spell in data["data"].items():
                    summoner_spell = SummonerSpellDto(summoner_spell)
                    data["data"][key] = summoner_spell
                    summoner_spell["region"] = query["platform"].region.value
                    summoner_spell["version"] = query["version"]
                    summoner_spell["locale"] = query["locale"]
                    summoner_spell["includedData"] = query["includedData"]
                yield SummonerSpellListDto(data)

        return generator()

    ##########
    # Realms #
    ##########

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    @get.register(RealmDto)
    @validate_query(_validate_get_realms_query, convert_region_to_platform)
    def get_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RealmDto:
        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/realms".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "staticdata/realms"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return RealmDto(data)

    _validate_get_many_realms_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(RealmDto)
    @validate_query(_validate_get_many_realms_query, convert_region_to_platform)
    def get_many_realms(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[RealmDto, None, None]:
        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/realms".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {}, self._get_rate_limiter(platform, "staticdata/realms"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                yield RealmDto(data)

        return generator()

    ############
    # Language #
    ############

    _validate_get_languages_query = Query. \
        has("platform").as_(Platform)

    @get.register(LanguagesDto)
    @validate_query(_validate_get_languages_query, convert_region_to_platform)
    def get_language(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/languages".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "staticdata/language"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data = {"region": query["platform"].region.value, "languages": data}
        return LanguagesDto(data)

    _validate_get_many_languages_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(LanguagesDto)
    @validate_query(_validate_get_many_languages_query, convert_region_to_platform)
    def get_many_language(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[LanguagesDto, None, None]:
        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/languages".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {}, self._get_rate_limiter(platform, "staticdata/language"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                yield LanguagesDto(data)

        return generator()

    ####################
    # Language Strings #
    ####################

    _validate_get_language_strings_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(LanguageStringsDto)
    @validate_query(_validate_get_language_strings_query, convert_region_to_platform)
    def get_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LanguageStringsDto:
        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/language-strings".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/language-strings"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        return LanguageStringsDto(data)

    _validate_get_many_language_strings_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str)

    @get_many.register(LanguageStringsDto)
    @validate_query(_validate_get_many_language_strings_query, convert_region_to_platform)
    def get_many_language_strings(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[LanguageStringsDto, None, None]:
        params = {}

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/language-strings".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/language-strings"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                yield LanguageStringsDto(data)

        return generator()

    #################
    # Profile Icons #
    #################

    _validate_get_profile_icons_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(ProfileIconDataDto)
    @validate_query(_validate_get_profile_icons_query, convert_region_to_platform)
    def get_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/profile-icons".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "staticdata/profile-icons"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        for pi in data["data"].values():
            pi["region"] = data["region"]
            pi["version"] = data["version"]
            pi["locale"] = data["locale"]
        return ProfileIconDataDto(data)

    _validate_get_many_profile_icons_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str)

    @get_many.register(ProfileIconDataDto)
    @validate_query(_validate_get_many_profile_icons_query, convert_region_to_platform)
    def get_many_profile_icons(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIconDataDto, None, None]:
        params = {}

        if "version" in query:
            params["version"] = query["version"]

        if "locale" in query:
            params["locale"] = query["locale"]

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/profile-icons".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "staticdata/profile-icons"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                for pi in data["data"].values():
                    pi["region"] = data["region"]
                    pi["version"] = data["version"]
                    pi["locale"] = data["locale"]
                yield ProfileIconDataDto(data)

        return generator()
