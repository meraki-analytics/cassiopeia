from typing import List, Set, Mapping, Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...data import Region, Platform
from ..common import CoreData, CassiopeiaObject, CassiopeiaGhost, CoreDataList, get_latest_version, CassiopeiaLazyList, provide_default_region, ghost_load_on
from .common import ImageData, Sprite, Image
from .map import Map
from ...dto.staticdata import item as dto


##############
# Data Types #
##############


class ItemListData(CoreDataList):
    _dto_type = dto.ItemListDto
    _renamed = {"included_data": "includedData"}


class ItemTreeData(CoreData):
    _renamed = {}


class ItemStatsData(CoreData):
    _renamed = {"PercentCritDamageMod": "percentCriticalStrikeDamage", "PercentSpellBlockMod": "percentMagicResist", "PercentHPRegenMod": "percentHealthRegen", "PercentMovementSpeedMod": "percentMovespeed", "FlatSpellBlockMod": "magicResist", "FlatCritDamageMod": "criticalStrikeDamage", "FlatEnergyPoolMod": "energy", "PercentLifeStealMod": "lifeSteal", "FlatMPPoolMod": "mana", "FlatMovementSpeedMod": "movespeed", "PercentAttackSpeedMod": "percentAttackSpeed", "FlatBlockMod": "block", "PercentBlockMod": "percentBlock", "FlatEnergyRegenMod": "energyRegen", "PercentSpellVampMod": "spellVamp", "FlatMPRegenMod": "manaRegen", "PercentDodgeMod": "dodge", "FlatAttackSpeedMod": "attackSpeed", "FlatArmorMod": "armor", "FlatHPRegenMod": "healthRegen", "PercentMagicDamageMod": "percentAbilityPower", "PercentMPPoolMod": "percentMana", "FlatMagicDamageMod": "abilityPower", "PercentMPRegenMod": "percentManaRegen", "PercentPhysicalDamageMod": "percentAttackDamage", "FlatPhysicalDamageMod": "attackDamage", "PercentHPPoolMod": "percentHealth", "PercentArmorMod": "percentArmor", "PercentEXPBonus": "percentExpBonus", "FlatHPPoolMod": "health", "FlatCritChanceMod": "criticalStrikeChance", "FlatEXPBonus": "expBonus"}

    def __call__(self, **kwargs):
        if "flatCritChanceMode" in kwargs and "percentCritChanceMod" in kwargs:
            self.critical_strike_chance =  kwargs.pop("flatCritChanceMod") + kwargs.pop("percentCritChanceMod")
        super().__call__(**kwargs)
        return self


class GoldData(CoreData):
    _renamed = {}


class ItemData(CoreData):
    _dto_type = dto.ItemDto
    _renamed = {"hideFromAll": "hide", "colloq": "keywords", "requiredChampion": "champion", "depth": "tier", "stacks": "max_stacks", "included_data": "includedData"}

    def __call__(self, **kwargs):
        if "image" in kwargs:
            self.image = ImageData(**kwargs.pop("image"))
        if "gold" in kwargs:
            self.gold = GoldData(**kwargs.pop("gold"))
        if "into" in kwargs:
            self.buildsInto = [int(x) for x in kwargs.pop("into")]
        if "from" in kwargs:
            self.buildsFrom = [int(x) for x in kwargs.pop("from")]
        if "stats" in kwargs:
            self.stats = ItemStatsData(**kwargs.pop("stats"))
        if "colloq" in kwargs:
            self.keywords = set(kw for kw in kwargs.pop("colloq").split(";") if kw != "")
        if "maps" in kwargs:
            """List of maps where this item is available."""
            self.maps = [int(m) for m, tf in kwargs.pop("maps").items() if tf]
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class Items(CassiopeiaLazyList):
    _data_types = {ItemListData}

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
        return Region(self._data[ItemListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[ItemListData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="item")
            self(version=version)
            return self._data[ItemListData].version

    @property
    def locale(self) -> str:
        """The locale for this item."""
        return self._data[ItemListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additional information for this item when it's loaded."""
        return self._data[ItemListData].includedData


class ItemStats(CassiopeiaObject):
    _data_types = {ItemStatsData}

    @property
    def percent_critical_strike_damage(self) -> float:
        return self._data[ItemStatsData].percentCriticalStrikeDamage

    @property
    def percent_magic_resist(self) -> float:
        return self._data[ItemStatsData].percentMagicResist

    @property
    def percent_health_regen(self) -> float:
        return self._data[ItemStatsData].percentHealthRegen

    @property
    def percent_movespeed(self) -> float:
        return self._data[ItemStatsData].percentMovespeed

    @property
    def magic_resist(self) -> float:
        return self._data[ItemStatsData].magicResist

    @property
    def critical_strike_damage(self) -> float:
        return self._data[ItemStatsData].criticalStrikeDamage

    @property
    def energy(self) -> float:
        return self._data[ItemStatsData].energy

    @property
    def life_steal(self) -> float:
        return self._data[ItemStatsData].lifeSteal

    @property
    def mana(self) -> float:
        return self._data[ItemStatsData].mana

    @property
    def movespeed(self) -> float:
        return self._data[ItemStatsData].movespeed

    @property
    def percent_attack_speed(self) -> float:
        return self._data[ItemStatsData].percentAttackSpeed

    @property
    def block(self) -> float:
        return self._data[ItemStatsData].block

    @property
    def percent_block(self) -> float:
        return self._data[ItemStatsData].percentBlock

    @property
    def energy_regen(self) -> float:
        return self._data[ItemStatsData].energyRegen

    @property
    def spell_vamp(self) -> float:
        return self._data[ItemStatsData].spellVamp

    @property
    def mana_regen(self) -> float:
        return self._data[ItemStatsData].manaRegen

    @property
    def dodge(self) -> float:
        return self._data[ItemStatsData].dodge

    @property
    def attack_speed(self) -> float:
        return self._data[ItemStatsData].attackSpeed

    @property
    def armor(self) -> float:
        return self._data[ItemStatsData].armor

    @property
    def health_regen(self) -> float:
        return self._data[ItemStatsData].healthRegen

    @property
    def percent_ability_power(self) -> float:
        return self._data[ItemStatsData].percentAbilityPower

    @property
    def percent_mana_regen(self) -> float:
        return self._data[ItemStatsData].percentManaRegen

    @property
    def ability_power(self) -> float:
        return self._data[ItemStatsData].abilityPower

    @property
    def percent_mana_regen(self) -> float:
        return self._data[ItemStatsData].percentManaRegen

    @property
    def percent_attack_damage(self) -> float:
        return self._data[ItemStatsData].percentAttackDamage

    @property
    def attack_damage(self) -> float:
        return self._data[ItemStatsData].attackDamage

    @property
    def percent_health(self) -> float:
        return self._data[ItemStatsData].percentHealth

    @property
    def percent_armor(self) -> float:
        return self._data[ItemStatsData].percentArmor

    @property
    def percent_xp_bonus(self) -> float:
        return self._data[ItemStatsData].percentExpBonus

    @property
    def health(self) -> float:
        return self._data[ItemStatsData].health

    @property
    def critical_strike_chance(self) -> float:
        return self._data[ItemStatsData].criticalStrikeChance

    @property
    def xp_bonus(self) -> float:
        return self._data[ItemStatsData].expBonus


class Gold(CassiopeiaObject):
    _data_types = {GoldData}

    @property
    def sell(self) -> int:
        return self._data[GoldData].sell

    @property
    def total(self) -> int:
        return self._data[GoldData].total

    @property
    def base(self) -> int:
        return self._data[GoldData].base

    @property
    def purchasable(self) -> bool:
        return self._data[GoldData].purchasable


@searchable({str: ["name", "region", "platform", "locale", "keywords", "maps", "tags", "tier"], int: ["id"], Region: ["region"], Platform: ["platform"], Map: ["maps"]})
class Item(CassiopeiaGhost):
    _data_types = {ItemData}

    @provide_default_region
    def __init__(self, *, id: int = None, name: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if included_data is None:
            included_data = {"all"}
        if locale is None and region is not None:
            locale = Region(region).default_locale
        kwargs = {"region": region, "included_data": included_data, "locale": locale}
        if id is not None:
            kwargs["id"] = id
        if name is not None:
            kwargs["name"] = name
        if version is not None:
            kwargs["version"] = version
        super().__init__(**kwargs)

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale, "includedData": self.included_data}
        if hasattr(self._data[ItemData], "id"):
            query["id"] = self._data[ItemData].id
        if hasattr(self._data[ItemData], "name"):
            query["name"] = self._data[ItemData].name
        return query

    def __eq__(self, other: "Item"):
        if not isinstance(other, Item) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[ItemData], "id"): s["id"] = self.id
        if hasattr(other._data[ItemData], "id"): o["id"] = other.id
        if hasattr(self._data[ItemData], "name"): s["name"] = self.name
        if hasattr(other._data[ItemData], "name"): o["name"] = other.name
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = "?"
        name = "?"
        if hasattr(self._data[ItemData], "id"):
            id_ = self.id
        if hasattr(self._data[ItemData], "name"):
            name = self.name
        return "Item(name='{name}', id={id_}, region='{region}')".format(name=name, id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

    @lazy_property
    def region(self) -> Region:
        """The region for this item."""
        return Region(self._data[ItemData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this item."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this item."""
        try:
            return self._data[ItemData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="item")
            self(version=version)
            return self._data[ItemData].version

    @property
    def locale(self) -> str:
        """The locale for this item."""
        return self._data[ItemData].locale or self.region.default_locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this item when it's loaded."""
        return self._data[ItemData].includedData

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def id(self) -> int:
        """The item's ID."""
        return self._data[ItemData].id

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def gold(self) -> Gold:
        return Gold.from_data(self._data[ItemData].gold)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def plaintext(self) -> str:
        return self._data[ItemData].plaintext

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def hide(self) -> bool:
        return self._data[ItemData].hide

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def in_store(self) -> bool:
        return self._data[ItemData].in_store

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def builds_into(self) -> List["Item"]:
        if hasattr(self._data[ItemData], "buildsInto"):
            return SearchableList([Item(id=id_, region=self.region) for id_ in self._data[ItemData].buildsInto])
        else:
            return SearchableList([])

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def builds_from(self) -> List["Item"]:
        if hasattr(self._data[ItemData], "buildsFrom"):
            return SearchableList([Item(id=id_, region=self.region) for id_ in self._data[ItemData].buildsFrom])
        else:
            return SearchableList([])

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def stats(self) -> ItemStats:
        return self._data[ItemData].stats

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def keywords(self) -> List[str]:
        return SearchableList(self._data[ItemData].keywords)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    @lazy
    def maps(self) -> List[Map]:
        return [Map(id=id_, region=self.region, version=self.version) for id_ in self._data[ItemData].maps]

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def description(self) -> str:
        return self._data[ItemData].description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def tags(self) -> List[str]:
        return self._data[ItemData].tags

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def effect(self) -> Mapping[str, str]:
        return self._data[ItemData].effect

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(name=self._data[ItemData].champion, region=self.region, version=self.verion)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def group(self) -> str:
        return self._data[ItemData].group

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[ItemData].name

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def consume_on_full(self) -> bool:
        return self._data[ItemData].consume_on_full

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def consumed(self) -> bool:
        return self._data[ItemData].consumed

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def sanitized_description(self) -> str:
        return self._data[ItemData].sanitized_description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def tier(self) -> int:
        return self._data[ItemData].tier

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def max_stacks(self) -> int:
        return self._data[ItemData].max_stacks

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    def special_recipe(self) -> int:
        return self._data[ItemData].special_recipe

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        """The image information for this item."""
        image = Image.from_data(self._data[ItemData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
