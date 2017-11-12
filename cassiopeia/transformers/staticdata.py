from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.staticdata.champion import ChampionData, ChampionListData, Champion, Champions
from ..core.staticdata.mastery import MasteryData, MasteryListData, Mastery, Masteries
from ..core.staticdata.rune import RuneData, RuneListData, Rune, Runes
from ..core.staticdata.item import ItemData, ItemListData, Item, Items
from ..core.staticdata.summonerspell import SummonerSpellData, SummonerSpellListData, SummonerSpell, SummonerSpells
from ..core.staticdata.version import VersionListData, Versions
from ..core.staticdata.map import MapData, MapListData, Map, Maps
from ..core.staticdata.realm import RealmData, Realms
from ..core.staticdata.language import LanguagesData, Locales
from ..core.staticdata.languagestrings import LanguageStringsData, LanguageStrings
from ..core.staticdata.profileicon import ProfileIconData, ProfileIconListData, ProfileIcon, ProfileIcons

from ..dto.staticdata import ChampionDto, ChampionListDto
from ..dto.staticdata import MasteryDto, MasteryListDto
from ..dto.staticdata import RuneDto, RuneListDto
from ..dto.staticdata import ItemDto, ItemListDto
from ..dto.staticdata import SummonerSpellDto, SummonerSpellListDto
from ..dto.staticdata import VersionListDto
from ..dto.staticdata import MapDto, MapListDto
from ..dto.staticdata.realm import RealmDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.profileicon import ProfileIconDetailsDto, ProfileIconDataDto

T = TypeVar("T")
F = TypeVar("F")


class StaticDataTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    ###############
    # Dto to Data #
    ###############

    # Champion

    @transform.register(ChampionDto, ChampionData)
    def champion_dto_to_data(self, value: ChampionDto, context: PipelineContext = None) -> ChampionData:
        data = deepcopy(value)
        return ChampionData.from_dto(data)

    @transform.register(ChampionListDto, ChampionListData)
    def champion_list_dto_to_data(self, value: ChampionListDto, context: PipelineContext = None) -> ChampionListData:
        data = deepcopy(value)

        data["data"] = [self.champion_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return ChampionListData(data, region=value["region"], version=value["version"], locale=value["locale"], included_data=value["includedData"])

    # Mastery

    @transform.register(MasteryDto, MasteryData)
    def mastery_dto_to_data(self, value: MasteryDto, context: PipelineContext = None) -> MasteryData:
        data = deepcopy(value)
        return MasteryData.from_dto(data)

    @transform.register(MasteryListDto, MasteryListData)
    def mastery_list_dto_to_data(self, value: MasteryListDto, context: PipelineContext = None) -> MasteryListData:
        data = deepcopy(value)

        data["data"] = [self.mastery_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return MasteryListData(data, region=value["region"], version=value["version"], locale=value["locale"], included_data=value["includedData"])

    # Rune

    @transform.register(RuneDto, RuneData)
    def rune_dto_to_data(self, value: RuneDto, context: PipelineContext = None) -> RuneData:
        data = deepcopy(value)
        return RuneData.from_dto(data)

    @transform.register(RuneListDto, RuneListData)
    def rune_list_dto_to_data(self, value: RuneListDto, context: PipelineContext = None) -> RuneListData:
        data = deepcopy(value)

        data["data"] = [self.rune_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return RuneListData(data, region=value["region"], version=value["version"], locale=value["locale"], included_data=value["includedData"])

    # Item

    @transform.register(ItemDto, ItemData)
    def item_dto_to_data(self, value: ItemDto, context: PipelineContext = None) -> ItemData:
        data = deepcopy(value)
        return ItemData.from_dto(data)

    @transform.register(ItemListDto, ItemListData)
    def item_list_dto_to_data(self, value: ItemListDto, context: PipelineContext = None) -> ItemListData:
        data = deepcopy(value)

        data["data"] = [self.item_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return ItemListData(data, region=value["region"], version=value["version"], locale=value["locale"], included_data=value["includedData"])

    # Summoner Spell

    @transform.register(SummonerSpellDto, SummonerSpellData)
    def summoner_spell_dto_to_data(self, value: SummonerSpellDto, context: PipelineContext = None) -> SummonerSpellData:
        data = deepcopy(value)
        return SummonerSpellData.from_dto(data)

    @transform.register(SummonerSpellListDto, SummonerSpellListData)
    def summoner_spell_list_dto_to_data(self, value: SummonerSpellListDto, context: PipelineContext = None) -> SummonerSpellListData:
        data = deepcopy(value)

        data["data"] = [self.summoner_spell_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return SummonerSpellListData(data, region=value["region"], version=value["version"], locale=value["locale"], included_data=value["includedData"])

    # Map

    @transform.register(MapDto, MapData)
    def map_dto_to_data(self, value: MapDto, context: PipelineContext = None) -> MapData:
        data = deepcopy(value)
        return MapData.from_dto(data)

    @transform.register(MapListDto, MapListData)
    def map_list_dto_to_data(self, value: MapListDto, context: PipelineContext = None) -> MapListData:
        data = deepcopy(value)

        data["data"] = [self.map_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"]})

        data = data["data"]
        return MapListData(data, region=value["region"], version=value["version"], locale=value["locale"])

    # Version

    @transform.register(VersionListDto, VersionListData)
    def version_list_dto_to_data(self, value: VersionListDto, context: PipelineContext = None) -> VersionListData:
        data = VersionListData(deepcopy(value["versions"]), region=value["region"])
        return data

    # Realm

    @transform.register(RealmDto, RealmData)
    def realm_dto_to_data(self, value: RealmDto, context: PipelineContext = None) -> RealmData:
        data = deepcopy(value)
        return RealmData(**data)

    # Languages

    @transform.register(LanguagesDto, LanguagesData)
    def languages_dto_to_data(self, value: LanguagesDto, context: PipelineContext = None) -> LanguagesData:
        data = deepcopy(value)
        return LanguagesData(data["languages"], region=value["region"])

    # Language Strings

    @transform.register(LanguageStringsDto, LanguageStringsData)
    def language_strings_dto_to_data(self, value: LanguageStringsDto, context: PipelineContext = None) -> LanguageStringsData:
        data = deepcopy(value)
        return LanguageStringsData.from_dto(data)

    # Profile Icons

    @transform.register(ProfileIconDetailsDto, ProfileIconData)
    def profile_icon_details_dto_to_data(self, value: ProfileIconDetailsDto, context: PipelineContext = None) -> ProfileIconData:
        data = deepcopy(value)
        return ProfileIconData.from_dto(data)

    @transform.register(ProfileIconDataDto, ProfileIconListData)
    def profile_icon_dto_to_data(self, value: ProfileIconDataDto, context: PipelineContext = None) -> ProfileIconListData:
        data = deepcopy(value)
        return ProfileIconListData([self.profile_icon_details_dto_to_data(p) for p in data["data"]], region=value["region"], version=value["version"], locale=value["locale"])

    ################
    # Data to Core #
    ################

    # Champion

    #@transform.register(ChampionData, Champion)
    def champion_data_to_core(self, value: ChampionData, context: PipelineContext = None) -> Champion:
        return Champion.from_data(value, loaded_groups={ChampionData})

    @transform.register(ChampionListData, Champions)
    def champion_list_data_to_core(self, value: ChampionListData, context: PipelineContext = None) -> Champions:
        return Champions.from_data(*[self.champion_data_to_core(c) for c in value], region=value.region, version=value.version, locale=value.locale, included_data=value.included_data)

    # Mastery

    #@transform.register(MasteryData, Mastery)
    def mastery_data_to_core(self, value: MasteryData, context: PipelineContext = None) -> Mastery:
        return Mastery.from_data(value)

    @transform.register(MasteryListData, Masteries)
    def mastery_list_data_to_core(self, value: MasteryListData, context: PipelineContext = None) -> Masteries:
        return Masteries.from_data(*[self.mastery_data_to_core(m) for m in value], region=value.region, version=value.version, locale=value.locale, included_data=value.included_data)

    # Rune

    #@transform.register(RuneData, Rune)
    def rune_data_to_core(self, value: RuneData, context: PipelineContext = None) -> Rune:
        return Rune.from_data(value)

    @transform.register(RuneListData, Runes)
    def rune_list_data_to_core(self, value: RuneListData, context: PipelineContext = None) -> Runes:
        return Runes.from_data(*[self.rune_data_to_core(r) for r in value], region=value.region, version=value.version, locale=value.locale, included_data=value.included_data)

    # Item

    #@transform.register(ItemData, Item)
    def item_data_to_core(self, value: ItemData, context: PipelineContext = None) -> Item:
        return Item.from_data(value)

    @transform.register(ItemListData, Items)
    def item_list_data_to_core(self, value: ItemListData, context: PipelineContext = None) -> Items:
        return Items.from_data(*(self.item_data_to_core(i) for i in value), region=value.region, version=value.version, locale=value.locale, included_data=value.included_data)

    # Summoner Spell

    #@transform.register(SummonerSpellData, SummonerSpell)
    def summoner_spell_data_to_core(self, value: SummonerSpellData, context: PipelineContext = None) -> SummonerSpell:
        return SummonerSpell.from_data(value)

    @transform.register(SummonerSpellListData, SummonerSpells)
    def summoner_spell_list_data_to_core(self, value: SummonerSpellListData, context: PipelineContext = None) -> SummonerSpells:
        return SummonerSpells.from_data(*[self.summoner_spell_data_to_core(s) for s in value], region=value.region, version=value.version, locale=value.locale, included_data=value.included_data)

    # Map

    #@transform.register(MapData, Map)
    def map_data_to_core(self, value: MapData, context: PipelineContext = None) -> Map:
        return Map.from_data(value)

    @transform.register(MapListData, Maps)
    def map_list_data_to_core(self, value: MapListData, context: PipelineContext = None) -> Maps:
        return Maps.from_data(*[self.map_data_to_core(m) for m in value], region=value.region, version=value.version, locale=value.locale)

    # Version

    @transform.register(VersionListData, Versions)
    def version_list_data_to_core(self, value: VersionListData, context: PipelineContext = None) -> Versions:
        version = Versions.from_data(*value, region=value.region)
        return version

    # Realm

    @transform.register(RealmData, Realms)
    def realm_data_to_core(self, value: RealmData, context: PipelineContext = None) -> Realms:
        realms = Realms.from_data(value)
        realms(region=value.region)
        return realms

    # Languages

    @transform.register(LanguagesData, Locales)
    def languages_data_to_core(self, value: LanguagesData, context: PipelineContext = None) -> Locales:
        return Locales.from_data(*value, region=value.region)

    # Language Strings

    @transform.register(LanguageStringsData, LanguageStrings)
    def language_strings_data_to_core(self, value: LanguageStringsData, context: PipelineContext = None) -> LanguageStrings:
        return LanguageStrings.from_data(value)

    # Profile Icon

    #@transform.register(ProfileIconData, ProfileIcon)
    def profile_icon_data_to_core(self, value: ProfileIconData, context: PipelineContext = None) -> ProfileIcon:
        return ProfileIcon.from_data(value)

    @transform.register(ProfileIconListData, ProfileIcons)
    def profile_icon_list_data_to_core(self, value: ProfileIconListData, context: PipelineContext = None) -> ProfileIcons:
        return ProfileIcons.from_data(*value, region=value.region, version=value.version, locale=value.locale)
