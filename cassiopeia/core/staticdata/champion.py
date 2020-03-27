from typing import Dict, List, Set, Union
from PIL.Image import Image as PILImage
import arrow

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ... import configuration
from ...data import Resource, Region, Platform, GameMode, Key
from ..common import CoreData, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, CoreDataList, get_latest_version, provide_default_region, ghost_load_on
from .common import ImageData, Image, Sprite
from .map import Map
from ...dto.staticdata import champion as dto
from .item import Item


##############
# Data Types #
##############


class ChampionReleaseData(CoreData):
    _renamed = {}


class ChampionRatesData(CoreData):
    _dto_type = dto.ChampionRatesDto
    _renamed = {}


class ChampionListData(CoreDataList):
    _dto_type = dto.ChampionListDto
    _renamed = {"included_data": "includedData"}


class SpellVarsData(CoreData):
    _renamed = {"dyn": "dynamic", "coeff": "coefficients"}


class LevelTipData(CoreData):
    _renamed = {"effect": "effects", "label": "keywords"}


class ChampionSpellData(CoreData):
    _renamed = {"vars": "variables", "maxrank": "maxRank", "cooldown": "cooldowns", "cost": "costs", "effect": "effects", "costType": "cost_type", "keyboardKey": "keyboard_key"}

    def __call__(self, *args, **kwargs):
        if "leveltip" in kwargs:
            self.levelUpTips = LevelTipData(**kwargs.pop("leveltip"))
        if "vars" in kwargs:
            self.variables =  [SpellVarsData(**v) for v in kwargs.pop("vars")]
        if "image" in kwargs:
            self.image =  ImageData(version=kwargs["version"], **kwargs.pop("image"))
        if "altimages" in kwargs:
            self.alternative_images = [ImageData(version=kwargs["version"], **alt) for alt in kwargs.pop("altimages")]
        super().__call__(**kwargs)
        return self


class BlockItemData(CoreData):
    _renamed = {}


class BlockData(CoreData):
    _renamed = {}

    def __call__(self, *args, **kwargs):
        if "items" in kwargs:
            self.items = [BlockItemData(**item) for item in kwargs.pop("items")]
        super().__call__(**kwargs)
        return self


class RecommendedData(CoreData):
    _renamed = {}

    def __call__(self, *args, **kwargs):
        if "blocks" in kwargs:
            self.itemSets = [BlockData(**item) for item in kwargs.pop("blocks")]
        super().__call__(**kwargs)
        return self


class PassiveData(CoreData):
    _renamed = {}

    def __call__(self, **kwargs):
        if "image" in kwargs:
            self.image = ImageData(version=kwargs["version"], **kwargs.pop("image"))
        super().__call__(**kwargs)
        return self


class SkinData(CoreData):
    _renamed = {"num": "number"}


class StatsData(CoreData):
    _renamed = {"armorperlevel": "armorPerLevel", "hpperlevel": "healthPerLevel", "attackdamage": "attackDamage", "mpperlevel": "manaPerLevel", "attackspeedoffset": "attackSpeedOffset", "hp": "health", "hpregenperlevel": "healthHegenPerLevel", "attackspeedperlevel": "percentAttackSpeedPerLevel", "attackrange": "attackRange", "attackdamageperlevel": "attackDamagePerLevel", "mpregenperlevel": "manaRegenPerLevel", "mp": "mana", "spellblockperlevel": "magicResistPerLevel", "crit": "criticalStrikeChance", "mpregen": "manaRegen", "spellblock": "magicResist", "hpregen": "healthRegen", "critperlevel": "criticalStrikeChancePerLevel"}


class InfoData(CoreData):
    _renamed = {}


class ChampionData(CoreData):
    _dto_type = dto.ChampionDto
    _renamed = {"allytips": "allyTips", "enemytips": "enemyTips", "recommended": "recommendedItemsets", "partype": "resource", "included_data": "includedData"}

    def __call__(self, **kwargs):
        if "recommended" in kwargs:
            self.recommendedItemsets = [RecommendedData(**item) for item in kwargs.pop("recommended")]
        if "info" in kwargs:
            self.info = InfoData(**kwargs.pop("info"))
        if "stats" in kwargs:
            self.stats = StatsData(**kwargs.pop("stats"))
        if "image" in kwargs:
            self.image = ImageData(**kwargs.pop("image"))
        if "skins" in kwargs:
            self.skins = [SkinData(**skin) for skin in kwargs.pop("skins")]
        if "passive" in kwargs:
            version = kwargs.get("version", get_latest_version(kwargs["region"], endpoint="champion"))
            self.passive = PassiveData(version=version, **kwargs.pop("passive"))
        if "spells" in kwargs:
            try:
                version
            except NameError:
                version = kwargs.get("version", get_latest_version(kwargs["region"], endpoint="champion"))
            self.spells = [ChampionSpellData(version=version, **spell) for spell in kwargs.pop("spells")]
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class Champions(CassiopeiaLazyList):
    _data_types = {ChampionListData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if included_data is None:
            included_data = {"all"}
        if locale is None and region is not None:
            locale = Region(region).default_locale
        kwargs = {"region": region, "included_data": included_data, "locale": locale}
        if version:
            kwargs["version"] = version
        CassiopeiaObject.__init__(self, **kwargs)

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
        except AttributeError:
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
        return self._data[ChampionListData].includedData


@searchable({str: ["key"]})
class SpellVars(CassiopeiaObject):
    _data_types = {SpellVarsData}

    @property
    def ranks_with(self) -> str:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[SpellVarsData].ranksWith

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


@searchable({str: ["name", "key", "keywords"], Key: ["keyboard_key"]})
class ChampionSpell(CassiopeiaObject):
    _data_types = {ChampionSpellData}

    @lazy_property
    def keywords(self) -> List[str]:
        """The keywords for this spell."""
        return SearchableList(self._data[ChampionSpellData].levelUpTips.keywords)

    @property
    def effects_by_level(self) -> List[str]:
        """The level-up changes, level-by-level."""
        return SearchableList(self._data[ChampionSpellData].levelUpTips.effects)

    @lazy_property
    def variables(self) -> List[SpellVars]:
        """Contains spell data."""
        return SearchableList(SpellVars.from_data(v) for v in self._data[ChampionSpellData].variables)

    @property
    def resource(self) -> Resource:
        """The resource consumed when using this spell."""
        return Resource(self._data[ChampionSpellData].cost_type)

    @lazy_property
    def image_info(self) -> Image:
        """The info about the spell's image, which can be pulled from datadragon."""
        return Image.from_data(self._data[ChampionSpellData].image)

    @property
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[ChampionSpellData].sanitizedDescription

    @property
    def sanitized_tooltip(self) -> str:
        """The spell's sanitized tooltip."""
        return self._data[ChampionSpellData].sanitizedTooltip

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
        return SearchableList(Image.from_data(alt) for alt in self._data[ChampionSpellData].alternativeImages)

    @property
    def name(self) -> str:
        """The spell's name."""
        return self._data[ChampionSpellData].name

    @property
    def keyboard_key(self) -> Key:
        """Q, W, E, or R"""
        return Key(self._data[ChampionSpellData].keyboard_key)


@searchable({str: ["type", "items"], Item: ["items"]})
class ItemSet(CassiopeiaObject):
    _data_types = {BlockData}

    def __init__(self, **kwargs):
        if "region" in kwargs:
            self.__region = kwargs["region"]
        super().__init__(**kwargs)

    @classmethod
    def from_data(cls, data: CoreData, region: Region):
        self = super().from_data(data)
        self.__region = region
        return self

    @property
    def items(self) -> Dict[Item, int]:
        """A dictionary of items mapped to how many of them are recommended."""
        return SearchableDictionary({Item(id=item.id, region=self.__region): item.count for item in self._data[BlockData].items})  # TODO Add version; low priority and hopefully it's just never an issue

    @property
    def rec_math(self) -> bool:
        """Well, we don't know what this one is. let us know if you figure it out."""
        return self._data[BlockData].recMath

    @property
    def type(self) -> str:
        """The item set's type (e.g. starting items)."""
        return self._data[BlockData].type


@searchable({str: ["item_sets", "map", "title", "mode", "type"], Item: ["item_sets"], GameMode: ["mode"]})
class RecommendedItems(CassiopeiaObject):
    _data_types = {RecommendedData}

    def __init__(self, **kwargs):
        if "region" in kwargs:
            self.__region = kwargs["region"]
        super().__init__(**kwargs)

    @classmethod
    def from_data(cls, data: CoreData, region: Region):
        self = super().from_data(data)
        self.__region = region
        return self

    @lazy_property
    def map(self) -> Map:
        """The name of the map these recommendations are for."""
        convert_shitty_map_name_to_id = {
            "HA": 12,
            "CS": 8,
            "SR": 11,
            "TT": 10
        }
        id_ = convert_shitty_map_name_to_id[self._data[RecommendedData].map]
        return Map(id=id_, region=self.__region)  # TODO Add version; low priority and hopefully it's just never an issue

    @lazy_property
    def item_sets(self) -> List[ItemSet]:
        """The recommended item sets."""
        return SearchableList(ItemSet.from_data(itemset, region=self.__region) for itemset in self._data[RecommendedData].itemSets)

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
        return Image.from_data(self._data[PassiveData].image)

    @property
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[PassiveData].sanitizedDescription

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
        if "champion_key" in kwargs:
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
        return "https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{}_{}.jpg".format(self.champion_key, self.number)

    @property
    def loading_image_url(self) -> str:
        """The skin's loading screen image url."""
        return "https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{}_{}.jpg".format(self.champion_key, self.number)

    @lazy_property
    def splash(self) -> PILImage:
        """The skin's splash art."""
        return configuration.settings.pipeline.get(PILImage, query={"url": self.splash_url})

    @lazy_property
    def loading_image(self) -> PILImage:
        """The skin's loading screen image."""
        return configuration.settings.pipeline.get(PILImage, query={"url": self.loading_image_url})


class Stats(CassiopeiaObject):
    _data_types = {StatsData}

    @property
    def armor_per_level(self) -> float:
        return self._data[StatsData].armorPerLevel

    @property
    def health_per_level(self) -> float:
        return self._data[StatsData].healthPerLevel

    @property
    def attack_damage(self) -> float:
        return self._data[StatsData].attackDamage

    @property
    def mana_per_level(self) -> float:
        return self._data[StatsData].manaPerLevel

    @property
    def attack_speed(self) -> float:
        return 0.625 / (1.0 + self._data[StatsData].attackSpeedOffset)

    @property
    def armor(self) -> float:
        return self._data[StatsData].armor

    @property
    def health(self) -> float:
        return self._data[StatsData].health

    @property
    def health_regen_per_level(self) -> float:
        return self._data[StatsData].healthRegenPerLevel

    @property
    def magic_resist(self) -> float:
        return self._data[StatsData].magicResist

    @property
    def attack_range(self) -> float:
        return self._data[StatsData].attackRange

    @property
    def movespeed(self) -> float:
        return self._data[StatsData].movespeed

    @property
    def attack_damage_per_level(self) -> float:
        return self._data[StatsData].attackDamagePerLevel

    @property
    def mana_regen_per_level(self) -> float:
        return self._data[StatsData].manaRegenPerLevel

    @property
    def mana(self) -> float:
        return self._data[StatsData].mana

    @property
    def magic_resist_per_level(self) -> float:
        return self._data[StatsData].magicResistPerLevel

    @property
    def critical_strike_chance(self) -> float:
        return self._data[StatsData].criticalStrikeChance

    @property
    def mana_regen(self) -> float:
        return self._data[StatsData].manaRegen

    @property
    def percent_attack_speed_per_level(self) -> float:
        return self._data[StatsData].percentAttackSpeedPerLevel / 100.0

    @property
    def health_regen(self) -> float:
        return self._data[StatsData].healthRegen

    @property
    def critical_strike_chance_per_level(self) -> float:
        return self._data[StatsData].criticalStrikeChancePerLevel


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


@searchable({str: ["name", "key", "region", "platform", "locale", "tags"], int: ["id"], Region: ["region"], Platform: ["platform"], bool: ["free_to_play"]})
class Champion(CassiopeiaGhost):
    _data_types = (ChampionData, ChampionReleaseData, ChampionRatesData)

    @provide_default_region
    def __init__(self, *, id: int = None, name: str = None, key: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if included_data is None:
            included_data = {"all"}
        if locale is None and region is not None:
            locale = Region(region).default_locale
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
        query = {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale, "includedData": self.included_data}
        if hasattr(self._data[ChampionData], "id"):
            query["id"] = self._data[ChampionData].id
        if hasattr(self._data[ChampionData], "name"):
            query["name"] = self._data[ChampionData].name
        return query

    def __eq__(self, other: "Champion"):
        if not isinstance(other, Champion) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[ChampionData], "id"): s["id"] = self.id
        if hasattr(other._data[ChampionData], "id"): o["id"] = other.id
        if hasattr(self._data[ChampionData], "name"): s["name"] = self.name
        if hasattr(other._data[ChampionData], "name"): o["name"] = other.name
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = "?"
        name = "?"
        if hasattr(self._data[ChampionData], "id"):
            id_ = self.id
        if hasattr(self._data[ChampionData], "name"):
            name = self.name
        return "Champion(name='{name}', id={id_}, region='{region}')".format(name=name, id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

    def load(self, load_groups: Set = None) -> "Champion":
        return super().load(load_groups=self._data_types)

    def __load__(self, load_group: CoreData = None, load_groups: Set = None) -> None:
        return super().__load__(load_group=load_group, load_groups=self._data_types)

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
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="champion")
            self(version=version)
            return self._data[ChampionData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ChampionData].locale or self.region.default_locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[ChampionData].includedData

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def id(self) -> int:
        """The champion's ID."""
        return self._data[ChampionData].id

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def ally_tips(self) -> List[str]:
        """The tips for playing with this champion."""
        return self._data[ChampionData].allyTips

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def enemy_tips(self) -> List[str]:
        """The tips for playing against this champion."""
        return self._data[ChampionData].enemyTips

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def blurb(self) -> str:
        """A short blurb about this champion."""
        return self._data[ChampionData].blurb

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def key(self) -> str:
        """The champion's key."""
        return self._data[ChampionData].key

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def lore(self) -> str:
        """The champion's lore."""
        return self._data[ChampionData].lore

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def name(self) -> str:
        """The champion's name."""
        return self._data[ChampionData].name

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def resource(self) -> Resource:
        """The type of resource this champion uses."""
        return Resource(self._data[ChampionData].resource)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def tags(self) -> List[str]:
        """The tags associated with this champion."""
        return self._data[ChampionData].tags

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    def title(self) -> str:
        """The champion's title."""
        return self._data[ChampionData].title

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def info(self) -> Info:
        """Info about this champion."""
        return Info.from_data(self._data[ChampionData].info)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def recommended_itemsets(self) -> List[RecommendedItems]:
        """The champion's recommended itemsets."""
        return SearchableList(RecommendedItems.from_data(item, region=self.region) for item in self._data[ChampionData].recommendedItemsets)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def stats(self) -> Stats:
        """The champion's stats."""
        return Stats.from_data(self._data[ChampionData].stats)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def skins(self) -> List[Skin]:
        """This champion's skins."""
        skins = []
        for skin in self._data[ChampionData].skins:
            skins.append(Skin.from_data((skin)))
            skins[-1]._Skin__champion_key = self.key
        return SearchableList(skins)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def passive(self) -> Passive:
        """This champion's passive."""
        return Passive.from_data(self._data[ChampionData].passive)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def spells(self) -> List[ChampionSpell]:
        """This champion's spells."""
        keys = {0: "Q", 1: "W", 2: "E", 3: "R"}
        spells = []
        for i, spell in enumerate(self._data[ChampionData].spells):
            spell.keyboard_key = keys[i]
            spells.append(ChampionSpell.from_data(spell))
        return SearchableList(spells)

    @CassiopeiaGhost.property(ChampionData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        """The image information for this champion."""
        image = Image.from_data(self._data[ChampionData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.spriteInfo

    @lazy_property
    def free_to_play(self) -> bool:
        """Whether or not the champion is currently free to play."""
        from ..champion import ChampionRotation
        rotation = ChampionRotation(region=self.region)
        for champ in rotation.free_champions:
            if self.id == champ.id:
                return True
        else:
            return False

    @lazy_property
    def free_to_play_new_players(self) -> bool:
        """Whether or not the champion is currently free to play for new players."""
        from ..champion import ChampionRotation
        rotation = ChampionRotation(region=self.region)
        for champ in rotation.free_champions_for_new_players:
            if self.id == champ.id:
                return True
        for champ in rotation.free_champions:
            if self.id == champ.id:
                return True
        else:
            return False

    @CassiopeiaGhost.property(ChampionReleaseData)
    @ghost_load_on
    @lazy
    def release_date(self) -> arrow.Arrow:
        return arrow.get(self._data[ChampionReleaseData].releaseDate)

    @CassiopeiaGhost.property(ChampionRatesData)
    @ghost_load_on
    @lazy
    def play_rates(self) -> SearchableDictionary:
       return self._data[ChampionRatesData].playRates

    @CassiopeiaGhost.property(ChampionRatesData)
    @ghost_load_on
    @lazy
    def win_rates(self) -> SearchableDictionary:
        return self._data[ChampionRatesData].winRates

    @CassiopeiaGhost.property(ChampionRatesData)
    @ghost_load_on
    @lazy
    def ban_rates(self) -> SearchableDictionary:
        return self._data[ChampionRatesData].banRates
