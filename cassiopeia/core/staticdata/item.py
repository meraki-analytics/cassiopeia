from typing import List, Set, Mapping, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ... import configuration
from ...data import Region, Platform
from ..common import CoreData, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList, DataObjectList, get_latest_version
from .common import ImageData, Sprite, Image
from .map import Map
from ...dto.staticdata import item as dto


##############
# Data Types #
##############


class ItemListData(DataObjectList):
    _dto_type = dto.ItemListDto
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
        return self._dto["includedData"]


class ItemTreeData(CoreData):
    _renamed = {}

    @property
    def header(self) -> str:
        return self._dto["header"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]


class ItemStatsData(CoreData):
    _renamed = {"percent_critical_strike_damage": "PercentCritDamageMod", "percent_magic_resist": "PercentSpellBlockMod", "percent_health_regen": "PercentHPRegenMod", "percent_movespeed": "PercentMovementSpeedMod", "magic_resist": "FlatSpellBlockMod", "critical_strike_damage": "FlatCritDamageMod", "energy": "FlatEnergyPoolMod", "life_steal": "PercentLifeStealMod", "mana": "FlatMPPoolMod", "movespeed": "FlatMovementSpeedMod", "percent_attack_speed": "PercentAttackSpeedMod", "block": "FlatBlockMod", "percent_block": "PercentBlockMod", "energy_regen": "FlatEnergyRegenMod", "spell_vamp": "PercentSpellVampMod", "mana_regen": "FlatMPRegenMod", "dodge": "PercentDodgeMod", "attack_speed": "FlatAttackSpeedMod", "armor": "FlatArmorMod", "health_regen": "FlatHPRegenMod", "percent_ability_power": "PercentMagicDamageMod", "percent_mana_regen": "PercentMPPoolMod", "ability_power": "FlatMagicDamageMod", "percent_mana_regen": "PercentMPRegenMod", "percent_attack_damage": "PercentPhysicalDamageMod", "attack_damage": "FlatPhysicalDamageMod", "percent_health": "PercentHPPoolMod", "percent_armor": "PercentArmorMod", "percent_xp_bonus": "PercentEXPBonus", "health": "FlatHPPoolMod", "critical_strike_chance": "FlatCritChanceMod", "xp_bonus": "FlatEXPBonus"}

    @property
    def percent_critical_strike_damage(self) -> float:
        return self._dto["PercentCritDamageMod"]

    @property
    def percent_magic_resist(self) -> float:
        return self._dto["PercentSpellBlockMod"]

    @property
    def percent_health_regen(self) -> float:
        return self._dto["PercentHPRegenMod"]

    @property
    def percent_movespeed(self) -> float:
        return self._dto["PercentMovementSpeedMod"]

    @property
    def magic_resist(self) -> str:
        return self._dto["FlatSpellBlockMod"]

    @property
    def critical_strike_damage(self) -> float:
        return self._dto["FlatCritDamageMod"]

    @property
    def energy(self) -> float:
        return self._dto["FlatEnergyPoolMod"]

    @property
    def life_steal(self) -> float:
        return self._dto["PercentLifeStealMod"]

    @property
    def mana(self) -> float:
        return self._dto["FlatMPPoolMod"]

    @property
    def movespeed(self) -> float:
        return self._dto["FlatMovementSpeedMod"]

    @property
    def percent_attack_speed(self) -> float:
        return self._dto["PercentAttackSpeedMod"]

    @property
    def block(self) -> float:
        return self._dto["FlatBlockMod"]

    @property
    def percent_block(self) -> float:
        return self._dto["PercentBlockMod"]

    @property
    def energy_regen(self) -> float:
        return self._dto["FlatEnergyRegenMod"]

    @property
    def spell_vamp(self) -> float:
        return self._dto["PercentSpellVampMod"]

    @property
    def mana_regen(self) -> float:
        return self._dto["FlatMPRegenMod"]

    @property
    def dodge(self) -> float:
        return self._dto["PercentDodgeMod"]

    @property
    def attack_speed(self) -> float:
        return self._dto["FlatAttackSpeedMod"]

    @property
    def armor(self) -> float:
        return self._dto["FlatArmorMod"]

    @property
    def health_regen(self) -> float:
        return self._dto["FlatHPRegenMod"]

    @property
    def percent_ability_power(self) -> float:
        return self._dto["PercentMagicDamageMod"]

    @property
    def percent_mana_regen(self) -> float:
        return self._dto["PercentMPPoolMod"]

    @property
    def ability_power(self) -> float:
        return self._dto["FlatMagicDamageMod"]

    @property
    def percent_mana_regen(self) -> float:
        return self._dto["PercentMPRegenMod"]

    @property
    def percent_attack_damage(self) -> float:
        return self._dto["PercentPhysicalDamageMod"]

    @property
    def attack_damage(self) -> float:
        return self._dto["FlatPhysicalDamageMod"]

    @property
    def percent_health(self) -> float:
        return self._dto["PercentHPPoolMod"]

    @property
    def percent_armor(self) -> float:
        return self._dto["PercentArmorMod"]

    @property
    def percent_xp_bonus(self) -> float:
        return self._dto["PercentEXPBonus"]

    @property
    def health(self) -> float:
        return self._dto["FlatHPPoolMod"]

    @property
    def critical_strike_chance(self) -> float:
        return self._dto["FlatCritChanceMod"] + self._dto["PercentCritChanceMod"]

    @property
    def xp_bonus(self) -> float:
        return self._dto["FlatEXPBonus"]


class GoldData(CoreData):
    _renamed = {}

    @property
    def sell(self) -> int:
        return self._dto["sell"]

    @property
    def total(self) -> int:
        return self._dto["total"]

    @property
    def base(self) -> int:
        return self._dto["base"]

    @property
    def purchaseable(self) -> bool:
        return self._dto["purchaseable"]


class ItemData(CoreData):
    _dto_type = dto.ItemDto
    _renamed = {"hide": "hideFromAll", "in_store": "inStore", "builds_into": "into", "builds_from": "from", "keywords": "colloq", "champion": "requiredChampion", "consume_on_full": "consumeOnFull", "sanitized_description": "sanitizedDescription", "tier": "depth", "max_stacks": "stacks", "included_data": "includedData"}

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
    def gold(self) -> GoldData:
        return GoldData.from_dto(self._dto["gold"])

    @property
    def plaintext(self) -> str:
        return self._dto["plaintext"]

    @property
    def hide(self) -> bool:
        return self._dto["hideFromAll"]

    @property
    def in_store(self) -> bool:
        return self._dto["inStore"]

    @property
    def builds_into(self) -> List[int]:  # TODO Convert str to int in transformer
        return self._dto["into"]

    @property
    def builds_from(self) -> List[int]:  # TODO Convert str to int in transformer
        return self._dto["from"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def stats(self) -> ItemStatsData:
        return ItemStatsData.from_dto(self._dto["stats"])

    @property
    def keywords(self) -> Set[str]:
        return set(kw for kw in self._dto["colloq"].split(";") if kw != "")

    @property
    def maps(self) -> List[int]:  # TODO Convert from Dict to List
        """List of maps where this item is available."""
        return [int(m) for m, tf in self._dto["maps"].items() if tf]

    @property
    def special_recipe(self) -> int:
        return self._dto["specialRecipe"]

    @property
    def image(self) -> ImageData:
        return ImageData.from_dto(self._dto["image"])

    @property
    def description(self) -> str:
        return self._dto["description"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]

    @property
    def effect(self) -> Mapping[str, str]:
        return self._dto["effect"]

    @property
    def champion(self) -> str:
        return self._dto["requiredChampion"]

    @property
    def group(self) -> str:
        return self._dto["group"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def consume_on_full(self) -> bool:
        return self._dto["consumeOnFull"]

    @property
    def consumed(self) -> bool:
        return self._dto["consumed"]

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def tier(self) -> int:
        return self._dto["depth"]

    @property
    def max_stacks(self) -> int:
        return self._dto["stacks"]


##############
# Core Types #
##############


class Items(CassiopeiaGhostList):
    _data_types = {ItemListData}

    def __init__(self, *args, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
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
        SearchableList.__init__(self, [StaticDataTransformer.item_data_to_core(None, i) for i in data])
        super().__load_hook__(load_group, data)

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
        except KeyError:
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
        return self._data[ItemListData].included_data


class ItemStats(CassiopeiaObject):
    _data_types = {ItemStatsData}

    @property
    def percent_critical_strike_damage(self) -> float:
        return self._data[ItemStatsData].percent_critical_strike_damage

    @property
    def percent_magic_resist(self) -> float:
        return self._data[ItemStatsData].percent_magic_resist

    @property
    def percent_health_regen(self) -> float:
        return self._data[ItemStatsData].percent_health_regen

    @property
    def percent_movespeed(self) -> float:
        return self._data[ItemStatsData].percent_movespeed

    @property
    def magic_resist(self) -> float:
        return self._data[ItemStatsData].magic_resist

    @property
    def critical_strike_damage(self) -> float:
        return self._data[ItemStatsData].critical_strike_damage

    @property
    def energy(self) -> float:
        return self._data[ItemStatsData].energy

    @property
    def life_steal(self) -> float:
        return self._data[ItemStatsData].life_steal

    @property
    def mana(self) -> float:
        return self._data[ItemStatsData].mana

    @property
    def movespeed(self) -> float:
        return self._data[ItemStatsData].movespeed

    @property
    def percent_attack_speed(self) -> float:
        return self._data[ItemStatsData].percent_attack_speed

    @property
    def block(self) -> float:
        return self._data[ItemStatsData].block

    @property
    def percent_block(self) -> float:
        return self._data[ItemStatsData].percent_block

    @property
    def energy_regen(self) -> float:
        return self._data[ItemStatsData].energy_regen

    @property
    def spell_vamp(self) -> float:
        return self._data[ItemStatsData].spell_vamp

    @property
    def mana_regen(self) -> float:
        return self._data[ItemStatsData].mana_regen

    @property
    def dodge(self) -> float:
        return self._data[ItemStatsData].dodge

    @property
    def attack_speed(self) -> float:
        return self._data[ItemStatsData].attack_speed

    @property
    def armor(self) -> float:
        return self._data[ItemStatsData].armor

    @property
    def health_regen(self) -> float:
        return self._data[ItemStatsData].health_regen

    @property
    def percent_ability_power(self) -> float:
        return self._data[ItemStatsData].percent_ability_power

    @property
    def percent_mana_regen(self) -> float:
        return self._data[ItemStatsData].percent_mana_regen

    @property
    def ability_power(self) -> float:
        return self._data[ItemStatsData].ability_power

    @property
    def percent_attack_damage(self) -> float:
        return self._data[ItemStatsData].percent_attack_damage

    @property
    def attack_damage(self) -> float:
        return self._data[ItemStatsData].attack_damage

    @property
    def percent_health(self) -> float:
        return self._data[ItemStatsData].percent_health

    @property
    def percent_armor(self) -> float:
        return self._data[ItemStatsData].percent_armor

    @property
    def percent_xp_bonus(self) -> float:
        return self._data[ItemStatsData].percent_xp_bonus

    @property
    def health(self) -> float:
        return self._data[ItemStatsData].health

    @property
    def critical_strike_chance(self) -> float:
        return self._data[ItemStatsData].critical_strike_chance

    @property
    def xp_bonus(self) -> float:
        return self._data[ItemStatsData].xp_bonus


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
    def purchaseable(self) -> bool:
        return self._data[GoldData].purchaseable


@searchable({str: ["name", "region", "platform", "locale", "keywords", "maps", "tags", "tier"], int: ["id"], Region: ["region"], Platform: ["platform"], Map: ["maps"]})
class Item(CassiopeiaGhost):
    _data_types = {ItemData}

    def __init__(self, *, id: int = None, name: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
            region = Region(region)
        if included_data is None:
            included_data = {"all"}
        if locale is None and region is not None:
            locale = region.default_locale
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
        if "id" in self._data[ItemData]._dto:
            query["id"] = self._data[ItemData].id
        if "name" in self._data[ItemData]._dto:
            query["name"] = self._data[ItemData].name
        return query

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
        except KeyError:
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
        return self._data[ItemData].included_data

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The item's ID."""
        return self._data[ItemData].id

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def gold(self) -> Gold:
        return Gold.from_data(self._data[ItemData].gold)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def plaintext(self) -> str:
        return self._data[ItemData].plaintext

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def hide(self) -> bool:
        return self._data[ItemData].hide

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def in_store(self) -> bool:
        return self._data[ItemData].in_store

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def builds_into(self) -> List["Item"]:
        return self._data[ItemData].builds_into

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def builds_from(self) -> List["Item"]:
        return self._data[ItemData].builds_from

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def stats(self) -> ItemStats:
        return self._data[ItemData].stats

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def keywords(self) -> List[str]:
        return SearchableList(self._data[ItemData].keywords)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    @lazy
    def maps(self) -> List[Map]:
        return [Map(id=id_, region=self.region, version=self.version) for id_ in self._data[ItemData].maps]

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def description(self) -> str:
        return self._data[ItemData].description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def tags(self) -> List[str]:
        return self._data[ItemData].tags

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def effect(self) -> Mapping[str, str]:
        return self._data[ItemData].effect

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def champion(self) -> "Champion":
        from .champion import Champion
        return Champion(name=self._data[ItemData].champion, region=self.region, version=self.verion)

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def group(self) -> str:
        return self._data[ItemData].group

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[ItemData].name

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def consume_on_full(self) -> bool:
        return self._data[ItemData].consume_on_full

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def consumed(self) -> bool:
        return self._data[ItemData].consumed

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def sanitized_description(self) -> str:
        return self._data[ItemData].sanitized_description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def tier(self) -> int:
        return self._data[ItemData].tier

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def max_stacks(self) -> int:
        return self._data[ItemData].max_stacks

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def special_recipe(self) -> int:
        return self._data[ItemData].special_recipe

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    @lazy
    def image(self) -> Image:
        """The image information for this item."""
        image = Image.from_data(self._data[ItemData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
