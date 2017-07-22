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
from ..core.staticdata.language import LanguagesData, Languages
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
from ..dto.staticdata.profileicon import ProfileIconDataDto, ProfileIconListDto

T = TypeVar("T")
F = TypeVar("F")


class StaticDataTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # Data

    @transform.register(ChampionDto, ChampionData)
    def champion_dto_to_data(self, value: ChampionDto, context: PipelineContext = None) -> ChampionData:
        data = deepcopy(value)
        return ChampionData(data)

    @transform.register(ChampionListDto, ChampionListData)
    def champion_list_dto_to_data(self, value: ChampionListDto, context: PipelineContext = None) -> ChampionListData:
        data = deepcopy(value)

        data["data"] = [self.champion_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return ChampionListData(data)

    @transform.register(MasteryDto, MasteryData)
    def mastery_dto_to_data(self, value: MasteryDto, context: PipelineContext = None) -> MasteryData:
        data = deepcopy(value)
        return MasteryData(data)

    @transform.register(MasteryListDto, MasteryListData)
    def mastery_list_dto_to_data(self, value: MasteryListDto, context: PipelineContext = None) -> MasteryListData:
        data = deepcopy(value)

        data["data"] = [self.mastery_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return MasteryListData(data)

    @transform.register(RuneDto, RuneData)
    def rune_dto_to_data(self, value: RuneDto, context: PipelineContext = None) -> RuneData:
        data = deepcopy(value)
        return RuneData(data)

    @transform.register(RuneListDto, RuneListData)
    def rune_list_dto_to_data(self, value: RuneListDto, context: PipelineContext = None) -> RuneListData:
        data = deepcopy(value)

        data["data"] = [self.rune_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return RuneListData(data)

    @transform.register(ItemDto, ItemData)
    def item_dto_to_data(self, value: ItemDto, context: PipelineContext = None) -> ItemData:
        data = deepcopy(value)
        return ItemData(data)

    @transform.register(ItemListDto, ItemListData)
    def item_list_dto_to_data(self, value: ItemListDto, context: PipelineContext = None) -> ItemListData:
        data = deepcopy(value)

        data["data"] = [self.item_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return ItemListData(data)

    @transform.register(SummonerSpellDto, SummonerSpellData)
    def summoner_spell_dto_to_data(self, value: SummonerSpellDto, context: PipelineContext = None) -> SummonerSpellData:
        data = deepcopy(value)
        return SummonerSpellData(data)

    @transform.register(SummonerSpellListDto, SummonerSpellListData)
    def summoner_spell_list_dto_to_data(self, value: SummonerSpellListDto, context: PipelineContext = None) -> SummonerSpellListData:
        data = deepcopy(value)

        data["data"] = [self.summoner_spell_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"], "includedData": data["includedData"]})

        data = data["data"]
        return SummonerSpellListData(data)

    @transform.register(MapDto, MapData)
    def map_dto_to_data(self, value: MapDto, context: PipelineContext = None) -> MapData:
        data = deepcopy(value)
        return MapData(data)

    @transform.register(MapListDto, MapListData)
    def map_list_dto_to_data(self, value: MapListDto, context: PipelineContext = None) -> MapListData:
        data = deepcopy(value)

        data["data"] = [self.map_dto_to_data(c) for c in data["data"].values()]
        for c in data["data"]:
            c._update({"region": data["region"], "locale": data["locale"], "version": data["version"]})

        data = data["data"]
        return MapListData(data)

    @transform.register(VersionListDto, VersionListData)
    def version_list_dto_to_data(self, value: VersionListDto, context: PipelineContext = None) -> VersionListData:
        data = VersionListData(deepcopy(value["versions"]))
        data._region = value["region"]
        return data

    @transform.register(RealmDto, RealmData)
    def realm_dto_to_data(self, value: RealmDto, context: PipelineContext = None) -> RealmData:
        data = deepcopy(value)
        return RealmData(data)

    @transform.register(LanguagesDto, LanguagesData)
    def languages_dto_to_data(self, value: LanguagesDto, context: PipelineContext = None) -> LanguagesData:
        data = deepcopy(value)
        return LanguagesData(data["languages"])

    @transform.register(LanguageStringsDto, LanguageStringsData)
    def language_strings_dto_to_data(self, value: LanguageStringsDto, context: PipelineContext = None) -> LanguageStringsData:
        data = deepcopy(value)
        return LanguageStringsData(data)

    @transform.register(ProfileIconDataDto, ProfileIconData)
    def profile_icon_dto_to_data(self, value: ProfileIconDataDto, context: PipelineContext = None) -> ProfileIconData:
        data = deepcopy(value)
        return ProfileIconData(data)

    @transform.register(ProfileIconListDto, ProfileIconListData)
    def profile_icon_dto_to_data(self, value: ProfileIconListDto, context: PipelineContext = None) -> ProfileIconListData:
        data = deepcopy(value)
        return ProfileIconListData([self.profile_icon_dto_to_data(p) for p in data["data"]])

    # Core

    @transform.register(ChampionData, Champion)
    def champion_data_to_core(self, value: ChampionData, context: PipelineContext = None) -> Champion:
        return Champion(value)

    @transform.register(ChampionListData, ChampionListData)
    def champion_list_data_to_core(self, value: ChampionListData, context: PipelineContext = None) -> Champions:
        return Champions([self.champion_data_to_core(c) for c in value])

    @transform.register(MasteryData, Mastery)
    def mastery_data_to_core(self, value: MasteryData, context: PipelineContext = None) -> Mastery:
        return Mastery(value)

    @transform.register(MasteryListData, Masteries)
    def mastery_list_data_to_core(self, value: MasteryListData, context: PipelineContext = None) -> Masteries:
        return Masteries([self.mastery_data_to_core(m) for m in value])

    @transform.register(RuneData, Rune)
    def rune_data_to_core(self, value: RuneData, context: PipelineContext = None) -> Rune:
        return Rune(value)

    @transform.register(RuneListData, Runes)
    def rune_list_data_to_core(self, value: RuneListData, context: PipelineContext = None) -> Runes:
        return Runes([self.rune_data_to_core(r) for r in value])

    @transform.register(ItemData, Item)
    def item_data_to_core(self, value: ItemData, context: PipelineContext = None) -> Item:
        return Item(value)

    @transform.register(ItemListData, Items)
    def item_list_data_to_core(self, value: ItemListData, context: PipelineContext = None) -> Items:
        return Items([self.item_data_to_core(i) for i in value])

    @transform.register(SummonerSpellData, SummonerSpell)
    def summoner_spell_data_to_core(self, value: SummonerSpellData, context: PipelineContext = None) -> SummonerSpell:
        return SummonerSpell(value)

    @transform.register(SummonerSpellListData, SummonerSpells)
    def summoner_spell_list_data_to_core(self, value: SummonerSpellListData, context: PipelineContext = None) -> SummonerSpells:
        return SummonerSpells([self.summoner_spell_data_to_core(s) for s in value])

    @transform.register(MapData, Map)
    def map_data_to_core(self, value: MapData, context: PipelineContext = None) -> Map:
        return Map(value)

    @transform.register(MapListData, Maps)
    def map_list_data_to_core(self, value: MapListData, context: PipelineContext = None) -> Maps:
        return Maps([self.map_data_to_core(m) for m in value])

    @transform.register(VersionListData, Versions)
    def version_list_data_to_core(self, value: VersionListData, context: PipelineContext = None) -> Versions:
        version = Versions([value])
        version._region = value._region
        return version

    @transform.register(RealmData, Realms)
    def realm_data_to_core(self, value: RealmData, context: PipelineContext = None) -> Realms:
        return Realms(value)

    @transform.register(LanguagesData, Languages)
    def languages_data_to_core(self, value: LanguagesData, context: PipelineContext = None) -> Languages:
        return Languages(value)

    @transform.register(LanguageStringsData, LanguageStrings)
    def language_strings_data_to_core(self, value: LanguageStringsData, context: PipelineContext = None) -> LanguageStrings:
        return LanguageStrings(value)

    @transform.register(ProfileIconData, ProfileIcons)
    def profile_icon_data_to_core(self, value: ProfileIconData, context: PipelineContext = None) -> ProfileIcons:
        return ProfileIcons(value)

    @transform.register(ProfileIconData, ProfileIcons)
    def profile_icon_data_to_core(self, value: ProfileIconData, context: PipelineContext = None) -> ProfileIcons:
        return ProfileIcons(value)
