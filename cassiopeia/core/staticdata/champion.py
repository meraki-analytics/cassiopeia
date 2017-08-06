from typing import Dict, List, Set, Union

from PIL.Image import Image as PILImage
from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ...configuration import settings
from ...data import Resource, Region, Platform, Map, GameMode
from ..champion import ChampionData as ChampionStatusData
from ..champion import ChampionListData as ChampionStatusListData
from ..common import CoreData, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList, DataObjectList, get_latest_version
from .common import ImageData, Image, Sprite
from ...dto.staticdata import champion as dto
from .item import Item


##############
# Data Types #
##############


class ChampionListData(DataObjectList):
    _dto_type = dto.ChampionListDto
    _renamed = {"included_data": "includedData"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._dto["includedData"]


class SpellVarsData(CoreData):
    _renamed = {"ranks_with": "ranksWith", "dynamic": "dyn", "coefficients": "coeff"}

    @property  # This doesn't get returned by the API
    def ranks_with(self) -> str:
        return self._dto["ranksWith"]

    @property  # This doesn't get returned by the API
    def dynamic(self) -> str:
        return self._dto["dyn"]

    @property
    def link(self) -> str:
        return self._dto["link"]

    @property
    def coefficients(self) -> List[float]:
        return self._dto["coeff"]

    @property
    def key(self) -> str:
        return self._dto["key"]


class LevelTipData(CoreData):
    _renamed = {"effects": "effect", "keywords": "label"}

    @property
    def effects(self) -> List[str]:
        return self._dto["effect"]

    @property
    def keywords(self) -> List[str]:
        return self._dto["label"]


class ChampionSpellData(CoreData):
    _renamed = {"level_up_tips": "leveltip", "variables": "vars", "sanitized_description": "sanitizedDescription", "sanitized_tooltip": "sanitizedTooltip",
                "max_rank": "maxrank", "cooldowns": "cooldown", "costs": "cost", "alternative_images": "altimages", "effects": "effect", "resource": "costType"}

    @property
    def level_up_tips(self) -> LevelTipData:
        return LevelTipData.from_dto(self._dto["leveltip"])

    @property
    def variables(self) -> List[SpellVarsData]:
        return [SpellVarsData.from_dto(v) for v in self._dto["vars"]]

    @property
    def resource(self) -> str:
        return self._dto["costType"]

    @property
    def image(self) -> ImageData:
        return ImageData.from_dto(self._dto["image"])

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def sanitized_tooltip(self) -> str:
        return self._dto["sanitizedTooltip"]

    @property
    def effects(self) -> List[List[float]]:
        return self._dto["effect"]

    @property
    def tooltip(self) -> str:
        return self._dto["tooltip"]

    @property
    def max_rank(self) -> int:
        return self._dto["maxrank"]

    @property
    def range(self) -> List[Union[int, str]]:
        return self._dto["range"]

    @property
    def cooldowns(self) -> List[float]:
        return self._dto["cooldown"]

    @property
    def costs(self) -> List[int]:
        return self._dto["cost"]

    @property
    def key(self) -> str:
        return self._dto["key"]

    @property
    def description(self) -> str:
        return self._dto["description"]

    @property
    def alternative_images(self) -> List[ImageData]:
        return [ImageData.from_dto(alt) for alt in self._dto["altimages"]]

    @property
    def name(self) -> str:
        return self._dto["name"]


class BlockItemData(CoreData):
    _renamed = {}

    @property
    def count(self) -> int:
        return self._dto["count"]

    @property
    def id(self) -> int:
        return self._dto["id"]


class BlockData(CoreData):
    _renamed = {"rec_math": "recMath"}

    @property
    def items(self) -> list:
        return [BlockItemData.from_dto(item) for item in self._dto["items"]]

    @property
    def rec_math(self) -> bool:
        return self._dto["recMath"]

    @property
    def type(self) -> str:
        return self._dto["type"]


class RecommendedData(CoreData):
    _renamed = {"item_sets": "blocks"}

    @property
    def map(self) -> str:
        return self._dto["map"]

    @property
    def item_sets(self) -> List[BlockData]:
        return [BlockData.from_dto(item_set) for item_set in self._dto["blocks"]]

    @property
    def champion(self) -> str:
        return self._dto["champion"]

    @property
    def title(self) -> str:
        return self._dto["title"]

    @property
    def priority(self) -> bool:
        return self._dto["priority"]

    @property
    def mode(self) -> str:
        return self._dto["mode"]

    @property
    def type(self) -> str:
        return self._dto["type"]


class PassiveData(CoreData):
    _renamed = {"sanitized_description": "sanitizedDescription"}

    @property
    def image(self) -> ImageData:
        return ImageData.from_dto(self._dto["image"])

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def description(self) -> str:
        return self._dto["description"]


class SkinData(CoreData):
    _renamed = {"number": "num"}

    @property
    def number(self) -> int:
        return self._dto["num"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def id(self) -> int:
        return self._dto["id"]


class StatsData(CoreData):
    _renamed = {"armor_per_level": "armorperlevel",
                "health_per_level": "hpperlevel",
                "attack_damage": "attackdamage",
                "mana_per_level": "mpperlevel",
                "attack_speed_offset": "attackspeedoffset",
                "health": "hp",
                "health_regen_per_level": "hpregenperlevel",
                "percent_attack_speed_per_level": "attackspeedperlevel",
                "attack_range": "attackrange",
                "attack_damage_per_level": "attackdamageperlevel",
                "mana_regen_per_level": "mpregenperlevel",
                "mana": "mp",
                "magic_resist_per_level": "spellblockperlevel",
                "critical_strike_chance": "crit",
                "mana_regen": "mpregen",
                "magic_resist": "spellblock",
                "health_regen": "hpregen",
                "critical_strike_chance_per_level": "critperlevel"}

    @property
    def armor_per_level(self) -> float:
        return self._dto["armorperlevel"]

    @property
    def health_per_level(self) -> float:
        return self._dto["hpperlevel"]

    @property
    def attack_damage(self) -> float:
        return self._dto["attackdamage"]

    @property
    def mana_per_level(self) -> float:
        return self._dto["mpperlevel"]

    @property
    def attack_speed_offset(self) -> float:
        return self._dto["attackspeedoffset"]

    @property
    def armor(self) -> float:
        return self._dto["armor"]

    @property
    def health(self) -> float:
        return self._dto["hp"]

    @property
    def health_regen_per_level(self) -> float:
        return self._dto["hpregenperlevel"]

    @property
    def magic_resist(self) -> float:
        return self._dto["spellblock"]

    @property
    def attack_range(self) -> float:
        return self._dto["attackrange"]

    @property
    def movespeed(self) -> float:
        return self._dto["movespeed"]

    @property
    def attack_damage_per_level(self) -> float:
        return self._dto["attackdamageperlevel"]

    @property
    def mana_regen_per_level(self) -> float:
        return self._dto["mpregenperlevel"]

    @property
    def mana(self) -> float:
        return self._dto["mp"]

    @property
    def magic_resist_per_level(self) -> float:
        return self._dto["spellblockperlevel"]

    @property
    def critical_strike_chance(self) -> float:
        return self._dto["crit"]

    @property
    def mana_regen(self) -> float:
        return self._dto["mpregen"]

    @property
    def percent_attack_speed_per_level(self) -> float:
        return self._dto["attackspeedperlevel"]

    @property
    def health_regen(self) -> float:
        return self._dto["hpregen"]

    @property
    def critical_strike_chance_per_level(self) -> float:
        return self._dto["critperlevel"]


class InfoData(CoreData):
    _renamed = {}

    @property
    def difficulty(self) -> int:
        return self._dto["difficulty"]

    @property
    def attack(self) -> int:
        return self._dto["attack"]

    @property
    def defense(self) -> int:
        return self._dto["defense"]

    @property
    def magic(self) -> int:
        return self._dto["magic"]


class ChampionData(CoreData):
    _dto_type = dto.ChampionDto
    _renamed = {"ally_tips": "allytips", "enemy_tips": "enemytips", "recommended_itemsets": "recommended", "resource": "partype", "included_data": "includedData"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]

    @property
    def included_data(self) -> Set[str]:
        return self._dto["includedData"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def ally_tips(self) -> List[str]:
        return self._dto["allytips"]

    @property
    def enemy_tips(self) -> List[str]:
        return self._dto["enemytips"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def title(self) -> str:
        return self._dto["title"]

    @property
    def blurb(self) -> str:
        return self._dto["blurb"]

    @property
    def key(self) -> str:
        return self._dto["key"]

    @property
    def lore(self) -> str:
        return self._dto["lore"]

    @property
    def resource(self) -> str:
        return self._dto["partype"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]

    @property
    def recommended_itemsets(self) -> List[RecommendedData]:
        return [RecommendedData.from_dto(item) for item in self._dto["recommended"]]

    @property
    def info(self) -> InfoData:
        return InfoData.from_dto(self._dto["info"])

    @property
    def stats(self) -> StatsData:
        return StatsData.from_dto(self._dto["stats"])

    @property
    def image(self) -> ImageData:
        return ImageData.from_dto(self._dto["image"])

    @property
    def skins(self) -> List[SkinData]:
        return [SkinData.from_dto(skin) for skin in self._dto["skins"]]

    @property
    def passive(self) -> PassiveData:
        return PassiveData.from_dto(self._dto["passive"])

    @property
    def spells(self) -> List[ChampionSpellData]:
        return [ChampionSpellData.from_dto(spell) for spell in self._dto["spells"]]


##############
# Core Types #
##############


class Champions(CassiopeiaGhostList):
    _data_types = {ChampionListData}

    def __init__(self, *args, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        if included_data is None:
            included_data = {"all"}
        if locale is None:
            locale = region.default_locale
        kwargs = {"region": region, "included_data": included_data, "locale": locale}
        if version:
            kwargs["version"] = version
        super().__init__(*args, **kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale, "includedData": self.included_data}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        self.clear()
        from ...transformers.staticdata import StaticDataTransformer
        SearchableList.__init__(self, [StaticDataTransformer.champion_data_to_core(None, c) for c in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ChampionListData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this champion."""
        try:
            return self._data[ChampionListData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="champion")
            self(version=version)
            return self._data[ChampionListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ChampionListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[ChampionListData].included_data


@searchable({str: ["key"]})
class SpellVars(CassiopeiaObject):
    _data_types = {SpellVarsData}

    @property
    def ranks_with(self) -> str:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[SpellVarsData].ranks_with

    @property
    def dynamic(self) -> str:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[SpellVarsData].dynamic

    @property
    def link(self) -> str:
        """Stat this spell scales from."""
        return self._data[SpellVarsData].link

    @lazy_property
    def coefficients(self) -> List[float]:
        """The scaling coefficients for this spell."""
        return SearchableList(self._data[SpellVarsData].coefficients)

    @property
    def key(self) -> str:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[SpellVarsData].key


@searchable({str: ["name", "key", "keywords", "resource"], Resource: ["resource"]})
class ChampionSpell(CassiopeiaObject):
    _data_types = {ChampionSpellData}

    @lazy_property
    def keywords(self) -> List[str]:
        """The keywords for this spell."""
        return SearchableList(self._data[ChampionSpellData].level_up_tips.keywords)

    @property
    def effects_by_level(self) -> List[str]:
        """The level-up changes, level-by-level."""
        return SearchableList(self._data[ChampionSpellData].level_up_tips.effects)

    @lazy_property
    def variables(self) -> List[SpellVars]:
        """Contains spell data."""
        return SearchableList(SpellVars.from_data(v) for v in self._data[ChampionSpellData].variables)

    @property
    def resource(self) -> Resource:
        """The resource consumed when using this spell."""
        return Resource(self._data[ChampionSpellData].resource)

    @lazy_property
    def image_info(self) -> Image:
        """The info about the spell's image, which can be pulled from datadragon."""
        return Image(self._data[ChampionSpellData].image)

    @property
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[ChampionSpellData].sanitized_description

    @property
    def sanitized_tooltip(self) -> str:
        """The spell's sanitized tooltip."""
        return self._data[ChampionSpellData].sanitized_tooltip

    @property
    def effects(self) -> List[List[float]]:
        """The level-by-level replacements for {{ e# }} tags in other values."""
        return SearchableList(self._data[ChampionSpellData].effects)

    @property
    def tooltip(self) -> str:
        """The spell's tooltip."""
        return self._data[ChampionSpellData].tooltip

    @property
    def max_rank(self) -> int:
        """The maximum rank this spell can attain."""
        return self._data[ChampionSpellData].max_rank

    @property
    def range(self) -> List[Union[int, str]]:
        """The maximum range of this spell. `self` if it has no range."""
        return SearchableList(self._data[ChampionSpellData].range)

    @property
    def cooldowns(self) -> List[float]:
        """The cooldowns of this spell (per level)."""
        return SearchableList(self._data[ChampionSpellData].cooldowns)

    @property
    def costs(self) -> List[int]:
        """The resource costs of this spell (per level)."""
        return SearchableList(self._data[ChampionSpellData].costs)

    @property
    def key(self) -> str:
        """The spell's key."""
        return self._data[ChampionSpellData].key

    @property
    def description(self) -> str:
        """The spell's description."""
        return self._data[ChampionSpellData].description

    @lazy_property
    def alternative_images(self) -> List[Image]:
        """The alternative images for this spell. These won't exist after patch NN, when Riot standardized all images."""
        return SearchableList(Image(alt) for alt in self._data[ChampionSpellData].alternative_images)

    @property
    def name(self) -> str:
        """The spell's name."""
        return self._data[ChampionSpellData].name


@searchable({str: ["type", "items"], Item: ["items"]})
class ItemSet(CassiopeiaObject):
    _data_types = {BlockData}

    @property
    def items(self) -> Dict[Item, int]:
        """A dictionary of items mapped to how many of them are recommended."""
        return SearchableDictionary({Item(id=item.id): item.count for item in self._data[BlockData].items})

    @property
    def rec_math(self) -> bool:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[BlockData].rec_math

    @property
    def type(self) -> str:
        """The item set's type (e.g. starting items)."""
        return self._data[BlockData].type


@searchable({str: ["item_sets", "map", "title", "mode", "type"], Item: ["item_sets"], GameMode: ["mode"]})
class RecommendedItems(CassiopeiaObject):
    _data_types = {RecommendedData}

    @property
    def map(self) -> Map:
        """The name of the map these recommendations are for."""
        return Map(self._data[RecommendedData].map)

    @lazy_property
    def item_sets(self) -> List[ItemSet]:
        """The recommended item sets."""
        return SearchableList(ItemSet.from_data(itemset) for itemset in self._data[RecommendedData].item_sets)

    @property
    def champion(self) -> "Champion":
        """The name of the champion to whom this set of recommendations belongs."""
        return Champion(name=self._data[RecommendedData].champion)

    @property
    def title(self) -> str:
        """The title of these recommendations."""
        return self._data[RecommendedData].title

    @property
    def priority(self) -> bool:
        """Whether this is a priority recommendation."""
        return self._data[RecommendedData].priority

    @property
    def mode(self) -> GameMode:
        """The game mode these recommendations are for."""
        return GameMode(self._data[RecommendedData].mode)

    @property
    def type(self) -> str:
        """The type of recommendation."""
        return self._data[RecommendedData].type


@searchable({str: ["name"]})
class Passive(CassiopeiaObject):
    _data_types = {PassiveData}

    @lazy_property
    def image_info(self) -> Image:
        """The info about the spell's image, which can be pulled from datadragon."""
        return Image(self._data[PassiveData].image)

    @property
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[PassiveData].sanitized_description

    @property
    def name(self) -> str:
        """The spell's name."""
        return self._data[PassiveData].name

    @property
    def description(self) -> str:
        """The spells' description."""
        return self._data[PassiveData].description


@searchable({str: ["name", "splash_url", "loading_image_url"], int: ["id"]})
class Skin(CassiopeiaObject):
    _data_types = {SkinData}

    def __init__(self, **kwargs):
        self.__champion_key = kwargs.pop("champion_key")
        super().__init__(**kwargs)

    @property
    def champion_key(self) -> str:
        """The key for the champion this belongs to."""
        return self.__champion_key

    @property
    def number(self) -> int:
        """The skin number."""
        return self._data[SkinData].number

    @property
    def name(self) -> str:
        """The skin's name."""
        return self._data[SkinData].name

    @property
    def id(self) -> int:
        """The skin's ID."""
        return self._data[SkinData].id

    @property
    def splash_url(self) -> str:
        """The skin's splash art url."""
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_{}.jpg".format(self.champion_key, self.number)

    @property
    def loading_image_url(self) -> str:
        """The skin's loading screen image url."""
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg".format(self.champion_key, self.number)

    @lazy_property
    def splash(self) -> PILImage:
        """The skin's splash art."""
        return settings.pipeline.get(PILImage, query={"url": self.splash_url})

    @lazy_property
    def loading_image(self) -> PILImage:
        """The skin's loading screen image."""
        return settings.pipeline.get(PILImage, query={"url": self._loading_image_url})


class Stats(CassiopeiaObject):
    _data_types = {StatsData}

    @property
    def armor_per_level(self) -> float:
        return self._data[StatsData].armor_per_level

    @property
    def health_per_level(self) -> float:
        return self._data[StatsData].health_per_level

    @property
    def attack_damage(self) -> float:
        return self._data[StatsData].attack_damage

    @property
    def mana_per_level(self) -> float:
        return self._data[StatsData].mana_per_level

    @property
    def attack_speed(self) -> float:
        return 0.625 / (1.0 + self._data[StatsData].attack_speed_offset)

    @property
    def armor(self) -> float:
        return self._data[StatsData].armor

    @property
    def health(self) -> float:
        return self._data[StatsData].health

    @property
    def health_regen_per_level(self) -> float:
        return self._data[StatsData].health_regen_per_level

    @property
    def magic_resist(self) -> float:
        return self._data[StatsData].magic_resist

    @property
    def attack_range(self) -> float:
        return self._data[StatsData].attack_range

    @property
    def movespeed(self) -> float:
        return self._data[StatsData].movespeed

    @property
    def attack_damage_per_level(self) -> float:
        return self._data[StatsData].attack_damage_per_level

    @property
    def mana_regen_per_level(self) -> float:
        return self._data[StatsData].mana_regen_per_level

    @property
    def mana(self) -> float:
        return self._data[StatsData].mana

    @property
    def magic_resist_per_level(self) -> float:
        return self._data[StatsData].magic_resist_per_level

    @property
    def critical_strike_chance(self) -> float:
        return self._data[StatsData].critical_strike_chance

    @property
    def mana_regen(self) -> float:
        return self._data[StatsData].mana_regen

    @property
    def percent_attack_speed_per_level(self) -> float:
        return self._data[StatsData].percent_attack_speed_per_level / 100.0

    @property
    def health_regen(self) -> float:
        return self._data[StatsData].health_regen

    @property
    def critical_strike_chance_per_level(self) -> float:
        return self._data[StatsData].critperlevel


class Info(CassiopeiaObject):
    _data_types = {InfoData}

    @property
    def difficulty(self) -> int:
        """How Riot rates the difficulty of this champion."""
        return self._data[InfoData].difficulty

    @property
    def attack(self) -> int:
        """How attack-oriented Riot rates this champion."""
        return self._data[InfoData].attack

    @property
    def defense(self) -> int:
        """How defense-oriented Riot rates this champion."""
        return self._data[InfoData].defense

    @property
    def magic(self) -> int:
        """How magic-oriented Riot rates this champion."""
        return self._data[InfoData].magic


@searchable({str: ["name", "key", "title", "region", "platform", "locale", "resource", "tags"], int: ["id"], Region: ["region"], Platform: ["platform"], bool: ["free_to_play"], Resource: ["resource"]})
class Champion(CassiopeiaGhost):
    _data_types = {ChampionData, ChampionStatusData}
    _load_types = {ChampionData: ChampionListData, ChampionStatusData: ChampionStatusListData}

    def __init__(self, *, id: int = None, name: str = None, key: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        if included_data is None:
            included_data = {"all"}
        if locale is None:
            locale = region.default_locale
        kwargs = {"region": region, "included_data": included_data, "locale": locale}
        if id is not None:
            kwargs["id"] = id
        if key is not None:
            kwargs["key"] = key
        if name is not None:
            kwargs["name"] = name
        if version is not None:
            kwargs["version"] = version
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale, "includedData": self.included_data}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item

        # The `data` is a list of champion data instances
        if "id" in self._data[ChampionData]._dto or "id" in self._data[ChampionStatusData]._dto:
            find = "id", self.id
        elif "name" in self._data[ChampionData]._dto or "name" in self._data[ChampionStatusData]._dto:
            find = "name", self.name
        else:
            raise RuntimeError("Impossible!")
        if load_group is ChampionData:
            data = find_matching_attribute(data, *find)
        else:
            data = find_matching_attribute(data, *find)
        super().__load_hook__(load_group, data)

    # What do we do about params like this that can exist in both data objects?
    # They will be set on both data objects always, so we can choose either one to return.
    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ChampionData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this champion."""
        try:
            return self._data[ChampionData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="champion")
            self(version=version)
            return self._data[ChampionData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ChampionData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[ChampionData].included_data

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The champion's ID."""
        return self._data[ChampionData].id

    @CassiopeiaGhost.property(ChampionStatusData)
    @ghost_load_on(KeyError)
    def enabled(self) -> bool:
        """Whether or not the champion is currently enabled."""
        return self._data[ChampionStatusData].enabled

    @CassiopeiaGhost.property(ChampionStatusData)
    @ghost_load_on(KeyError)
    def custom_enabled(self) -> bool:
        """Whether or not the champion is currently enabled in custom games."""
        return self._data[ChampionStatusData].custom_enabled

    @CassiopeiaGhost.property(ChampionStatusData)
    @ghost_load_on(KeyError)
    def coop_ai_enabled(self) -> bool:
        """Whether or not the champion is currently enabled in coop and AI games."""
        return self._data[ChampionStatusData].coop_ai_enabled

    @CassiopeiaGhost.property(ChampionStatusData)
    @ghost_load_on(KeyError)
    def ranked_enabled(self) -> bool:
        """Whether or not the champion is currently enabled in ranked games."""
        return self._data[ChampionStatusData].ranked_enabled

    @CassiopeiaGhost.property(ChampionStatusData)
    @ghost_load_on(KeyError)
    def free_to_play(self) -> bool:
        """Whether or not the champion is currently free to play."""
        return self._data[ChampionStatusData].free_to_play

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def ally_tips(self) -> List[str]:
        """The tips for playing with this champion."""
        return self._data[ChampionData].ally_tips

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def enemy_tips(self) -> List[str]:
        """The tips for playing against this champion."""
        return self._data[ChampionData].enemy_tips

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def blurb(self) -> str:
        """A short blurb about this champion."""
        return self._data[ChampionData].blurb

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def key(self) -> str:
        """The champion's key."""
        return self._data[ChampionData].key

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def lore(self) -> str:
        """The champion's lore."""
        return self._data[ChampionData].lore

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        """The champion's name."""
        return self._data[ChampionData].name

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def resource(self) -> Resource:
        """The type of resource this champion uses."""
        return Resource(self._data[ChampionData].resource)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def tags(self) -> List[str]:
        """The tags associated with this champion."""
        return self._data[ChampionData].tags

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    def title(self) -> str:
        """The champion's title."""
        return self._data[ChampionData].title

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def info(self) -> Info:
        """Info about this champion."""
        return Info.from_data(self._data[ChampionData].info)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def recommended_itemsets(self) -> List[RecommendedItems]:
        """The champion's recommended itemsets."""
        return SearchableList(RecommendedItems.from_data(item) for item in self._data[ChampionData].recommended_itemsets)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def stats(self) -> Stats:
        """The champion's stats."""
        return Stats.from_data(self._data[ChampionData].stats)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def skins(self) -> List[Skin]:
        """This champion's skins."""
        skins = []
        for skin in self._data[ChampionData].skins:
            skins.append(Skin.from_data((skin)))
            skins[-1]._Skin__champion_key = self.key
        return SearchableList(skins)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def passive(self) -> Passive:
        """This champion's passive."""
        return Passive.from_data(self._data[ChampionData].passive)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def spells(self) -> List[ChampionSpell]:
        """This champion's spells."""
        return SearchableList(ChampionSpell.from_data(spell) for spell in self._data[ChampionData].spells)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on(KeyError)
    @lazy
    def image(self) -> Image:
        """The image information for this champion."""
        image = Image(self._data[ChampionData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
