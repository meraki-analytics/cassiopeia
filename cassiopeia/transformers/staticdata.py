from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.staticdata.champion import ChampionData, ChampionListData
from ..core.staticdata.mastery import MasteryData, MasteryListData
from ..core.staticdata.rune import RuneData, RuneListData
from ..core.staticdata.item import ItemData, ItemListData
from ..core.staticdata.summonerspell import SummonerSpellData, SummonerSpellListData
from ..core.staticdata.version import VersionListData
from ..core.staticdata.map import MapData, MapListData
from ..core.staticdata.realm import RealmData
from ..core.staticdata.language import LanguagesData
from ..core.staticdata.languagestrings import LanguageStringsData
from ..core.staticdata.profileicon import ProfileIconData

from ..dto.staticdata import ChampionDto, ChampionListDto
from ..dto.staticdata import MasteryDto, MasteryListDto
from ..dto.staticdata import RuneDto, RuneListDto
from ..dto.staticdata import ItemDto, ItemListDto
from ..dto.staticdata import SummonerSpellDto, SummonerSpellListDto
from ..dto.staticdata import VersionListDto
from ..dto.staticdata import MapDto, MapListDto
from ..dto.staticdata.realm import RealmDto
from ..dto.staticdata.language import LanguagesDto, LanguageStringsDto
from ..dto.staticdata.profileicon import ProfileIconDataDto

T = TypeVar("T")
F = TypeVar("F")


class StaticDataTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

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
        return data

    @transform.register(RealmDto, RealmData)
    def realm_dto_to_data(self, value: RealmDto, context: PipelineContext = None) -> RealmData:
        data = deepcopy(value)
        return RealmData(data)

    @transform.register(LanguagesDto, LanguagesData)
    def languages_dto_to_data(self, value: LanguagesDto, context: PipelineContext = None) -> LanguagesData:
        data = deepcopy(value)
        return LanguagesData(data)

    @transform.register(LanguageStringsDto, LanguageStringsData)
    def language_strings_dto_to_data(self, value: LanguageStringsDto, context: PipelineContext = None) -> LanguageStringsData:
        data = deepcopy(value)
        return LanguageStringsData(data)

    @transform.register(ProfileIconDataDto, ProfileIconData)
    def profile_icon_dto_to_data(self, value: ProfileIconDataDto, context: PipelineContext = None) -> ProfileIconData:
        data = deepcopy(value)
        return ProfileIconData(data)
