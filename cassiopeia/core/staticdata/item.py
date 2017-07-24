from typing import List, Set, Mapping
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, Map
from ..common import DataObject, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList, DataObjectList, get_latest_version
from .common import Sprite, Image
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


class ItemTreeData(DataObject):
    _renamed = {}

    @property
    def header(self) -> str:
        return self._dto["header"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]


class SpriteData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def height(self) -> int:
        return self._dto["h"]


class ImageData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def full(self) -> str:
        return self._dto["full"]

    @property
    def group(self) -> str:
        return self._dto["group"]

    @property
    def height(self) -> int:
        return self._dto["h"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]


class ItemStatsData(DataObject):
    _renamed = {"percent_crit_damage_mod": "PercentCritDamageMod", "percent_spell_block_mod": "PercentSpellBlockMod", "percent_hp_regen_mod": "PercentHPRegenMod", "percent_movement_speed_mod": "PercentMovementSpeedMod", "flat_spell_block_mod": "FlatSpellBlockMod", "flat_crit_damage_mod": "FlatCritDamageMod", "flat_energy_pool_mod": "FlatEnergyPoolMod", "percent_lifesteal_mod": "PercentLifeStealMod", "flat_mp_pool_mod": "FlatMPPoolMod", "flat_movement_speed_mod": "FlatMovementSpeedMod", "percent_attack_speed_mod": "PercentAttackSpeedMod", "flat_block_mod": "FlatBlockMod", "percent_block_mod": "PercentBlockMod", "flat_energy_regen_mod": "FlatEnergyRegenMod", "percent_spellvamp_mod": "PercentSpellVampMod", "flat_mp_regen_mod": "FlatMPRegenMod", "percent_dodge_mod": "PercentDodgeMod", "flat_attack_speed_mod": "FlatAttackSpeedMod", "flat_armor_mod": "FlatArmorMod", "flat_hp_regen_mod": "FlatHPRegenMod", "percent_magic_damage_mod": "PercentMagicDamageMod", "percent_mp_pool_mod": "PercentMPPoolMod", "flat_magic_damage_mod": "FlatMagicDamageMod", "percent_mp_regen_mod": "PercentMPRegenMod", "percent_physical_damage_mod": "PercentPhysicalDamageMod", "flat_physical_damage_mod": "FlatPhysicalDamageMod", "percent_hp_pool_mod": "PercentHPPoolMod", "percent_armor_mod": "PercentArmorMod", "percent_crit_chance_mod": "PercentCritChanceMod", "percent_exp_bonus": "PercentEXPBonus", "flat_hp_pool_mod": "FlatHPPoolMod", "flat_crit_chance_mod": "FlatCritChanceMod", "flat_exp_bonus": "FlatEXPBonus"}

    @property
    def percent_crit_damage_mod(self) -> float:
        return self._dto["PercentCritDamageMod"]

    @property
    def percent_spell_block_mod(self) -> float:
        return self._dto["PercentSpellBlockMod"]

    @property
    def percent_hp_regen_mod(self) -> float:
        return self._dto["PercentHPRegenMod"]

    @property
    def percent_movememnt_speed_mod(self) -> float:
        return self._dto["PercentMovementSpeedMod"]

    @property
    def flat_spell_block_mod(self) -> str:
        return self._dto["FlatSpellBlockMod"]

    @property
    def flat_crit_damage_mod(self) -> float:
        return self._dto["FlatCritDamageMod"]

    @property
    def flat_energy_pool_mod(self) -> float:
        return self._dto["FlatEnergyPoolMod"]

    @property
    def percent_lifesteal_mod(self) -> float:
        return self._dto["PercentLifeStealMod"]

    @property
    def flat_mp_pool_mod(self) -> float:
        return self._dto["FlatMPPoolMod"]

    @property
    def flat_movement_speed_mod(self) -> float:
        return self._dto["FlatMovementSpeedMod"]

    @property
    def percent_attack_speed_mod(self) -> float:
        return self._dto["PercentAttackSpeedMod"]

    @property
    def flat_block_mod(self) -> float:
        return self._dto["FlatBlockMod"]

    @property
    def percent_block_mod(self) -> float:
        return self._dto["PercentBlockMod"]

    @property
    def flat_energy_regen_mod(self) -> float:
        return self._dto["FlatEnergyRegenMod"]

    @property
    def percent_spellvamp_mod(self) -> float:
        return self._dto["PercentSpellVampMod"]

    @property
    def flat_mp_regen_mod(self) -> float:
        return self._dto["FlatMPRegenMod"]

    @property
    def percent_dodge_mod(self) -> float:
        return self._dto["PercentDodgeMod"]

    @property
    def flat_attack_speed_mod(self) -> float:
        return self._dto["FlatAttackSpeedMod"]

    @property
    def flat_armor_mod(self) -> float:
        return self._dto["FlatArmorMod"]

    @property
    def flat_hp_regen_mod(self) -> float:
        return self._dto["FlatHPRegenMod"]

    @property
    def percent_magic_damage_mod(self) -> float:
        return self._dto["PercentMagicDamageMod"]

    @property
    def percent_mp_pool_mod(self) -> float:
        return self._dto["PercentMPPoolMod"]

    @property
    def flat_magic_damage_mod(self) -> float:
        return self._dto["FlatMagicDamageMod"]

    @property
    def percent_mp_regen_mod(self) -> float:
        return self._dto["PercentMPRegenMod"]

    @property
    def percent_physical_damage_mod(self) -> float:
        return self._dto["PercentPhysicalDamageMod"]

    @property
    def flat_physical_damage_mod(self) -> float:
        return self._dto["FlatPhysicalDamageMod"]

    @property
    def percent_hp_pool_mod(self) -> float:
        return self._dto["PercentHPPoolMod"]

    @property
    def percent_armor_mod(self) -> float:
        return self._dto["PercentArmorMod"]

    @property
    def percent_crit_change_mod(self) -> float:
        return self._dto["PercentCritChangeMod"]

    @property
    def percent_exp_bonus(self) -> float:
        return self._dto["PercentEXPBonus"]

    @property
    def flat_hp_pool_mod(self) -> float:
        return self._dto["FlatHPPoolMod"]

    @property
    def flat_crit_chance_mod(self) -> float:
        return self._dto["FlatCritChanceMod"]

    @property
    def flat_exp_bonus(self) -> float:
        return self._dto["FlatEXPBonus"]


class GoldData(DataObject):
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


class ItemData(DataObject):
    _dto_type = dto.ItemDto
    _renamed = {"hide": "hideFromAll", "in_store": "inStore", "builds_into": "into", "builds_from": "from", "keywords": "colloq", "champion": "requiredChampion", "consume_on_full": "consumeOnFull", "sanitized_description": "sanitizedDescription", "tier": "depth", "max_stacks": "stacks"}

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
        return self._dto["gold"]

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
        return ItemStatsData(self._dto["stats"])

    @property
    def keywords(self) -> List[str]:  # TODO Convert from str to List[str]
        return self._dto["colloq"]

    @property
    def maps(self) -> List[Map]:  # TODO Convert from Dict to List
        """List of maps where this item is available."""
        return self._dto["maps"]

    #@property
    #def special_recipe(self) -> int:
    #    return self._dto["specialRecipe"]

    @property
    def image(self) -> ImageData:
        return ImageData(self._dto["image"])

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
    def champion(self) -> int:
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

    def __get_query__(self):
        return {"region": self.region, "version": self.version}

    def __load_hook__(self, load_group, data: DataObject):
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
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[ItemListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ItemListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[ItemListData].included_data


class ItemStats(CassiopeiaObject):
    _data_types = {ItemStatsData}

    @property
    def percent_crit_damage_mod(self) -> float:
        return self._data[ItemStatsData].percent_crit_damage_mod

    @property
    def percent_spell_block_mod(self) -> float:
        return self._data[ItemStatsData].percent_spell_block_mod

    @property
    def percent_hp_regen_mod(self) -> float:
        return self._data[ItemStatsData].percent_hp_regen_mod

    @property
    def percent_movememnt_speed_mod(self) -> float:
        return self._data[ItemStatsData].percent_movememnt_speed_mod

    @property
    def flat_spell_block_mod(self) -> float:
        return self._data[ItemStatsData].flat_spell_block_mod

    @property
    def flat_crit_damage_mod(self) -> float:
        return self._data[ItemStatsData].flat_crit_damage_mod

    @property
    def flat_energy_pool_mod(self) -> float:
        return self._data[ItemStatsData].flat_energy_pool_mod

    @property
    def percent_lifesteal_mod(self) -> float:
        return self._data[ItemStatsData].percent_lifesteal_mod

    @property
    def flat_mp_pool_mod(self) -> float:
        return self._data[ItemStatsData].flat_mp_pool_mod

    @property
    def flat_movement_speed_mod(self) -> float:
        return self._data[ItemStatsData].flat_movement_speed_mod

    @property
    def percent_attack_speed_mod(self) -> float:
        return self._data[ItemStatsData].percent_attack_speed_mod

    @property
    def flat_block_mod(self) -> float:
        return self._data[ItemStatsData].flat_block_mod

    @property
    def percent_block_mod(self) -> float:
        return self._data[ItemStatsData].percent_block_mod

    @property
    def flat_energy_regen_mod(self) -> float:
        return self._data[ItemStatsData].flat_energy_regen_mod

    @property
    def percent_spellvamp_mod(self) -> float:
        return self._data[ItemStatsData].percent_spellvamp_mod

    @property
    def flat_mp_regen_mod(self) -> float:
        return self._data[ItemStatsData].flat_mp_regen_mod

    @property
    def percent_dodge_mod(self) -> float:
        return self._data[ItemStatsData].percent_dodge_mod

    @property
    def flat_attack_speed_mod(self) -> float:
        return self._data[ItemStatsData].flat_attack_speed_mod

    @property
    def flat_armor_mod(self) -> float:
        return self._data[ItemStatsData].flat_armor_mod

    @property
    def flat_hp_regen_mod(self) -> float:
        return self._data[ItemStatsData].flat_hp_regen_mod

    @property
    def percent_magic_damage_mod(self) -> float:
        return self._data[ItemStatsData].percent_magic_damage_mod

    @property
    def percent_mp_pool_mod(self) -> float:
        return self._data[ItemStatsData].percent_mp_pool_mod

    @property
    def flat_magic_damage_mod(self) -> float:
        return self._data[ItemStatsData].flat_magic_damage_mod

    @property
    def percent_mp_regen_mod(self) -> float:
        return self._data[ItemStatsData].percent_mp_regen_mod

    @property
    def percent_physical_damage_mod(self) -> float:
        return self._data[ItemStatsData].percent_physical_damage_mod

    @property
    def flat_physical_damage_mod(self) -> float:
        return self._data[ItemStatsData].flat_physical_damage_mod

    @property
    def percent_hp_pool_mod(self) -> float:
        return self._data[ItemStatsData].percent_hp_pool_mod

    @property
    def percent_armor_mod(self) -> float:
        return self._data[ItemStatsData].percent_armor_mod

    @property
    def percent_crit_change_mod(self) -> float:
        return self._data[ItemStatsData].percent_crit_change_mod

    @property
    def percent_exp_bonus(self) -> float:
        return self._data[ItemStatsData].percent_exp_bonus

    @property
    def flat_hp_pool_mod(self) -> float:
        return self._data[ItemStatsData].flat_hp_pool_mod

    @property
    def flat_crit_chance_mod(self) -> float:
        return self._data[ItemStatsData].flat_crit_chance_mod

    @property
    def flat_exp_bonus(self) -> float:
        return self._data[ItemStatsData].flat_exp_bonus


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
    _load_types = {ItemData: Items}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    def __load_hook__(self, load_group, core) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item

        # The `core` is a dict of summoner spell core instances
        if "id" in self._data[ItemData]._dto:
            find = "id", self.id
        elif "name" in self._data[ItemData]._dto:
            find = "name", self.name
        else:
            raise RuntimeError("Expected fields not present after loading.")
        core = find_matching_attribute(core, *find)

        super().__load_hook__(load_group, core)

    # What do we do about params like this that can exist in both data objects?
    # They will be set on both data objects always, so we can choose either one to return.
    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ItemData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this champion."""
        try:
            return self._data[ItemData].version
        except AttributeError:
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[ItemData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ItemData].locale

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
        return self._data[ItemData].gold

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
    def maps(self) -> List[Map]:
        return self._data[ItemData].maps

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
        return self._data[ItemData].champion

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
    def image_info(self) -> Image:
        """The image information for this champion."""
        return Image(self._data[ItemData].image, version=self.version)

    @lazy_property
    def image(self) -> PILImage:
        """The image icon for this champion."""
        return settings.pipeline.get(PILImage, query={"url": self.image_info.url})

    @lazy_property
    def sprite(self) -> Sprite:
        """The sprite that contains this champion's image icon."""
        return self.image_info.sprite.image
