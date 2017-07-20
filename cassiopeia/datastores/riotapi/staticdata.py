from typing import Type, TypeVar, Mapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.staticdata.champion import ChampionDto, ChampionListDto
from ...dto.staticdata.mastery import MasteryDto, MasteryListDto
from ...dto.staticdata.rune import RuneDto, RuneListDto
from ...dto.staticdata.item import ItemDto, ItemListDto
from ...dto.staticdata.summonerspell import SummonerSpellDto, SummonerSpellListDto
from ...dto.staticdata.version import VersionListDto
from ...dto.staticdata.map import MapDto, MapListDto
from ...dto.staticdata.realm import RealmDto
from ...dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ...dto.staticdata.profileicon import ProfileIconDataDto

T = TypeVar("T")


def _get_default_version(query: Mapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: Mapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class StaticDataAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    #############
    # Champions #
    #############

    _validate_get_champion_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ChampionDto)
    def get_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_champion_query(query, context)

        params = {
            "version": query["version"],
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, params)
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
    def get_many_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_champion_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"])),
            "dataById": True
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
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
        can_have("dataById").with_default(False)

    @get.register(ChampionListDto)
    def get_champion_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_champion_list_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"])),
            "dataById": query["dataById"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return ChampionListDto(data)

    _validate_get_many_champion_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"}).also. \
        can_have("dataById").with_default(False)

    @get_many.register(ChampionListDto)
    def get_many_champion_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_champion_list_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield ChampionListDto(data)

        return generator()

    ############
    # Versions #
    ############

    _validate_get_versions_query = Query. \
        has("platform").as_(Platform)

    @get.register(VersionListDto)
    def get_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> VersionListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_versions_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/versions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return VersionListDto({
            "region": query["platform"].region.value,
            "versions": data
        })

    _validate_get_many_versions_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(VersionListDto)
    def get_many_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[VersionListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_versions_query(query, context)

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/versions".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {})
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield VersionListDto({
                    "region": platform.region.value,
                    "versions": data
                })

        return generator()

    #############
    # Masteries #
    #############

    _validate_get_mastery_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(MasteryDto)
    def get_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasteryDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_mastery_query(query, context)

        params = {
            "version": query["version"],
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/masteries/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["version"] = query["version"]
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return MasteryDto(data)

    _validate_get_many_mastery_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(MasteryDto)
    def get_many_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasteryDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_mastery_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/masteries".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        def generator():
            for id in query["ids"]:
                try:
                    mastery = data["data"][str(id)]
                except KeyError as error:
                    raise NotFoundError("No mastery exists with id \"{id}\"".format(id=id)) from error

                mastery["region"] = query["platform"].region.value
                mastery["version"] = data["version"]
                mastery["locale"] = query["locale"]
                mastery["includedData"] = query["includedData"]
                yield MasteryDto(mastery)

        return generator()

    _validate_get_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(MasteryListDto)
    def get_mastery_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasteryListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_mastery_list_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/masteries".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return MasteryListDto(data)

    _validate_get_many_mastery_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(MasteryListDto)
    def get_many_mastery_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasteryListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_mastery_list_query(query, context)

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
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/masteries".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield MasteryListDto(data)

        return generator()

    #########
    # Runes #
    #########

    _validate_get_rune_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(RuneDto)
    def get_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> RuneDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_rune_query(query, context)

        params = {
            "version": query["version"],
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, params)
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
    def get_many_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[RuneDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_rune_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
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
    def get_rune_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> RuneListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_rune_list_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/runes".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return RuneListDto(data)

    _validate_get_many_rune_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(RuneListDto)
    def get_many_rune_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[RuneListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_rune_list_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield RuneListDto(data)

        return generator()

    #########
    # Items #
    #########

    _validate_get_item_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemDto)
    def get_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> ItemDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_item_query(query, context)

        params = {
            "version": query["version"],
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["version"] = query["version"]
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return ItemDto(data)

    _validate_get_many_item_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(ItemDto)
    def get_many_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ItemDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_item_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
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
                yield ItemDto(item)

        return generator()

    _validate_get_item_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(ItemListDto)
    def get_item_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> ItemListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_item_list_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/items".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return ItemListDto(data)

    _validate_get_many_item_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(ItemListDto)
    def get_many_item_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ItemListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_item_list_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield ItemListDto(data)

        return generator()

    ########
    # Maps #
    ########

    _validate_get_map_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(MapListDto)
    def get_map_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> MapListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_map_list_query(query, context)

        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/maps".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        return MapListDto(data)

    ###################
    # Summoner Spells #
    ###################

    _validate_get_summoner_spell_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str).also. \
        can_have("includedData").with_default({"all"})

    @get.register(SummonerSpellListDto)
    def get_summoner_spell_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpellListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_summoner_spell_list_query(query, context)

        params = {
            "locale": query["locale"],
            "tags": ",".join(list(query["includedData"]))
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/summoner-spells".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        data["includedData"] = query["includedData"]
        return SummonerSpellListDto(data)

    _validate_get_many_summoner_spell_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str).also. \
        can_have("includedData").with_default({"all"})

    @get_many.register(SummonerSpellListDto)
    def get_many_summoner_spell_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpellListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_summoner_spell_list_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield SummonerSpellListDto(data)

        return generator()

    ##########
    # Realms #
    ##########

    _validate_get_realms_query = Query. \
        has("platform").as_(Platform)

    @get.register(RealmDto)
    def get_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> RealmDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_realms_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/realms".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return RealmDto(data)

    _validate_get_many_realms_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(RealmDto)
    def get_many_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[RealmDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_realms_query(query, context)

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/realms".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {})
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                yield RealmDto(data)

        return generator()

    ############
    # Language #
    ############

    _validate_get_language_query = Query. \
        has("platform").as_(Platform)

    @get.register(LanguagesDto)
    def get_language(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguagesDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_language_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/languages".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {})
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data = {"region": query["platform"].region.value, "languages": data}
        return LanguagesDto(data)

    _validate_get_many_language_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(LanguagesDto)
    def get_many_language(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LanguagesDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_language_query(query, context)

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/static-data/v3/languages".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {})
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
    def get_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStringsDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_language_strings_query(query, context)

        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/language-strings".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
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
    def get_many_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LanguageStringsDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_language_strings_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                yield LanguageStringsDto(data)

        return generator()













    #################
    # Profile Icons #
    #################

    _validate_get_profile_icon_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("version").as_(str).also. \
        can_have("locale").with_default(_get_default_locale, supplies_type=str)

    @get.register(ProfileIconDataDto)
    def get_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIconDataDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_profile_icon_query(query, context)

        params = {
            "locale": query["locale"]
        }

        if "version" in query:
            params["version"] = query["version"]

        url = "https://{platform}.api.riotgames.com/lol/static-data/v3/profile-icons".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["locale"] = query["locale"]
        return ProfileIconDataDto(data)

    _validate_get_many_profile_icons_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("version").as_(str).also. \
        can_have("locale").as_(str)

    @get_many.register(ProfileIconDataDto)
    def get_many_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIconDataDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StaticDataAPI._validate_get_many_profile_icons_query(query, context)

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
                    data = self._get(url, params)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                yield ProfileIconDataDto(data)

        return generator()
