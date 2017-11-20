from typing import List, Set, Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ...data import Region, Platform, RuneType
from ..common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaList, get_latest_version, provide_default_region, ghost_load_on
from .common import ImageData, Sprite, Image
from ...dto.staticdata import rune as dto


##############
# Data Types #
##############


class RuneListData(CoreDataList):
    _dto_type = dto.RuneListDto
    _renamed = {"included_data": "includedData"}


class MetadataData(CoreData):
    _renamed = {}
    # TODO Convert the type in the transformer from str to int


class RuneStatsData(CoreData):
    _renamed = {"percent_time_dead_mod_per_level": "PercentTimeDeadModPerLevel", "percent_armor_penetration_mod_per_level": "PercentArmorPenetrationModPerLevel", "percent_crit_damage_mod": "PercentCritDamageMod", "percent_spell_block_mod": "PercentSpellBlockMod", "percent_hp_regen_mod": "PercentHPRegenMod", "percent_movement_speed_mod": "PercentMovementSpeedMod", "flat_spell_block_mod": "FlatSpellBlockMod", "flat_energy_regen_mod_per_level": "FlatEnergyRegenModPerLevel", "flat_energy_pool_mod": "FlatEnergyPoolMod", "flat_magic_penetration_mod_per_level": "FlatMagicPenetrationModPerLevel", "percent_life_steal_mod": "PercentLifeStealMod", "flat_mp_pool_mod": "FlatMPPoolMod", "percent_cooldown_mod": "PercentCooldownMod", "percent_magic_penetration_mod": "PercentMagicPenetrationMod", "flat_armor_penetration_mod_per_level": "FlatArmorPenetrationModPerLevel", "flat_movement_speed_mod": "FlatMovementSpeedMod", "flat_time_dead_mod_per_level": "FlatTimeDeadModPerLevel", "flat_armor_mod_per_level": "FlatArmorModPerLevel", "percent_attack_speed_mod": "PercentAttackSpeedMod", "flat_dodge_mod_per_level": "FlatDodgeModPerLevel", "percent_magic_damage_mod": "PercentMagicDamageMod", "percent_block_mod": "PercentBlockMod", "flat_dodge_mod": "FlatDodgeMod", "flat_energy_regen_mod": "FlatEnergyRegenMod", "flat_hp_mod_per_level": "FlatHPModPerLevel", "percent_attack_speed_mod_per_level": "PercentAttackSpeedModPerLevel", "percent_spell_vamp_mod": "PercentSpellVampMod", "flat_mp_regen_mod": "FlatMPRegenMod", "percent_hp_pool_mod": "PercentHPPoolMod", "percent_dodge_mod": "PercentDodgeMod", "flat_attack_speed_mod": "FlatAttackSpeedMod", "flat_armor_mod": "FlatArmorMod", "flat_magic_damage_mod_per_level": "FlatMagicDamageModPerLevel", "flat_hp_regen_mod": "FlatHPRegenMod", "percent_physical_damage_mod": "PercentPhysicalDamageMod", "flat_crit_chance_mod_per_level": "FlatCritChanceModPerLevel", "flat_spell_block_mod_per_level": "FlatSpellBlockModPerLevel", "percent_time_dead_mod": "PercentTimeDeadMod", "flat_block_mod": "FlatBlockMod", "percent_mp_pool_mod": "PercentMPPoolMod", "flat_magic_damage_mod": "FlatMagicDamageMod", "percent_mp_regen_mod": "PercentMPRegenMod", "percent_movement_speed_mod_per_level": "PercentMovementSpeedModPerLevel", "percent_cooldown_mod_per_level": "PercentCooldownModPerLevel", "flat_mp_mod_per_level": "FlatMPModPerLevel", "flat_energy_mod_per_level": "FlatEnergyModPerLevel", "flat_physical_damage_mod": "FlatPhysicalDamageMod", "flat_hp_regen_mod_per_level": "FlatHPRegenModPerLevel", "flat_crit_damage_mod": "FlatCritDamageMod", "percent_armor_mod": "PercentArmorMod", "flat_magic_penetration_mod": "FlatMagicPenetrationMod", "percent_crit_chance_mod": "PercentCritChanceMod", "flat_physical_damage_mod_per_level": "FlatPhysicalDamageModPerLevel", "percent_armor_penetration_mod": "PercentArmorPenetrationMod", "percent_exp_bonus": "PercentEXPBonus", "flat_mp_regen_mod_per_level": "FlatMPRegenModPerLevel", "percent_magic_penetration_mod_per_level": "PercentMagicPenetrationModPerLevel", "flat_time_dead_mod": "FlatTimeDeadMod", "flat_movement_speed_mod_per_level": "FlatMovementSpeedModPerLevel", "flat_gold_per_10_mod": "FlatGoldPer10Mod", "flat_armor_penetration_mod": "FlatArmorPenetrationMod", "flat_crit_damage_mod_per_level": "FlatCritDamageModPerLevel", "flat_hp_pool_mod": "FlatHPPoolMod", "flat_crit_chance_mod": "FlatCritChanceMod", "flat_exp_bonus": "FlatEXPBonus"}
    # TODO rename......


class RuneData(CoreData):
    _dto_type = dto.RuneDto
    _renamed = {"metadata": "rune", "sanitized_description": "sanitizedDescription", "included_data": "includedData"}

    def __call__(self, **kwargs):
        if "rune" in kwargs:
            self.metadata = MetadataData(**kwargs.pop("rune"))
        if "stats" in kwargs:
            self.stats = RuneStatsData(**kwargs.pop("stats"))
        if "image" in kwargs:
            self.image = ImageData(**kwargs.pop("image"))
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class Runes(CassiopeiaList):
    _data_types = {RuneListData}

    @provide_default_region
    def __init__(self, *args, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
        if included_data is None:
            included_data = {"all"}
        if locale is None and region is not None:
            locale = Region(region).default_locale
        kwargs = {"region": region, "included_data": included_data, "locale": locale}
        if version:
            kwargs["version"] = version
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[RuneListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[RuneListData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="rune")
            self(version=version)
            return self._data[RuneListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[RuneListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[RuneListData].includedData


class RuneStats(CassiopeiaObject):
    _data_types = {RuneStatsData}

    @property
    def percent_time_dead_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_time_dead_mod_per_level

    @property
    def percent_armor_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_armor_penetration_mod_per_level

    @property
    def percent_crit_damage_mod(self) -> float:
        return self._data[RuneStatsData].percent_crit_damage_mod

    @property
    def percent_spell_block_mod(self) -> float:
        return self._data[RuneStatsData].percent_spell_block_mod

    @property
    def percent_hp_regen_mod(self) -> float:
        return self._data[RuneStatsData].percent_hp_regen_mod

    @property
    def percent_movement_speed_mod(self) -> float:
        return self._data[RuneStatsData].percent_movement_speed_mod

    @property
    def flat_spell_block_mod(self) -> float:
        return self._data[RuneStatsData].flat_spell_block_mod

    @property
    def flat_energy_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_energy_regen_mod_per_level

    @property
    def flat_energy_pool_mod(self) -> float:
        return self._data[RuneStatsData].flat_energy_pool_mod

    @property
    def flat_magic_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_magic_penetration_mod_per_level

    @property
    def percent_life_steal_mod(self) -> float:
        return self._data[RuneStatsData].percent_life_steal_mod

    @property
    def flat_mp_pool_mod(self) -> float:
        return self._data[RuneStatsData].flat_mp_pool_mod

    @property
    def percent_cooldown_mod(self) -> float:
        return self._data[RuneStatsData].percent_cooldown_mod

    @property
    def percent_magic_penetration_mod(self) -> float:
        return self._data[RuneStatsData].percent_magic_penetration_mod

    @property
    def flat_armor_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_armor_penetration_mod_per_level

    @property
    def flat_movement_speed_mod(self) -> float:
        return self._data[RuneStatsData].flat_movement_speed_mod

    @property
    def flat_time_dead_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_time_dead_mod_per_level

    @property
    def flat_armor_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_armor_mod_per_level

    @property
    def percent_attack_speed_mod(self) -> float:
        return self._data[RuneStatsData].percent_attack_speed_mod

    @property
    def flat_dodge_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_dodge_mod_per_level

    @property
    def percent_magic_damage_mod(self) -> float:
        return self._data[RuneStatsData].percent_magic_damage_mod

    @property
    def percent_block_mod(self) -> float:
        return self._data[RuneStatsData].percent_block_mod

    @property
    def flat_dodge_mod(self) -> float:
        return self._data[RuneStatsData].flat_dodge_mod

    @property
    def flat_energy_regen_mod(self) -> float:
        return self._data[RuneStatsData].flat_energy_regen_mod

    @property
    def flat_hp_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_hp_mod_per_level

    @property
    def percent_attack_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_attack_speed_mod_per_level

    @property
    def percent_spell_vamp_mod(self) -> float:
        return self._data[RuneStatsData].percent_spell_vamp_mod

    @property
    def flat_mp_regen_mod(self) -> float:
        return self._data[RuneStatsData].flat_mp_regen_mod

    @property
    def percent_hp_pool_mod(self) -> float:
        return self._data[RuneStatsData].percent_hp_pool_mod

    @property
    def percent_dodge_mod(self) -> float:
        return self._data[RuneStatsData].percent_dodge_mod

    @property
    def flat_attack_speed_mod(self) -> float:
        return self._data[RuneStatsData].flat_attack_speed_mod

    @property
    def flat_armor_mod(self) -> float:
        return self._data[RuneStatsData].flat_armor_mod

    @property
    def flat_magic_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_magic_damage_mod_per_level

    @property
    def flat_hp_regen_mod(self) -> float:
        return self._data[RuneStatsData].flat_hp_regen_mod

    @property
    def percent_physical_damage_mod(self) -> float:
        return self._data[RuneStatsData].percent_physical_damage_mod

    @property
    def flat_crit_chance_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_crit_chance_mod_per_level

    @property
    def flat_spell_block_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_spell_block_mod_per_level

    @property
    def percent_time_dead_mod(self) -> float:
        return self._data[RuneStatsData].percent_time_dead_mod

    @property
    def flat_block_mod(self) -> float:
        return self._data[RuneStatsData].flat_block_mod

    @property
    def percent_mp_pool_mod(self) -> float:
        return self._data[RuneStatsData].percent_mp_pool_mod

    @property
    def flat_magic_damage_mod(self) -> float:
        return self._data[RuneStatsData].flat_magic_damage_mod

    @property
    def percent_mp_regen_mod(self) -> float:
        return self._data[RuneStatsData].percent_mp_regen_mod

    @property
    def percent_movement_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_movement_speed_mod_per_level

    @property
    def percent_cooldown_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_cooldown_mod_per_level

    @property
    def flat_mp_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_mp_mod_per_level

    @property
    def flat_energy_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_energy_mod_per_level

    @property
    def flat_physical_damage_mod(self) -> float:
        return self._data[RuneStatsData].flat_physical_damage_mod

    @property
    def flat_hp_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_hp_regen_mod_per_level

    @property
    def flat_crit_damage_mod(self) -> float:
        return self._data[RuneStatsData].flat_crit_damage_mod

    @property
    def percent_armor_mod(self) -> float:
        return self._data[RuneStatsData].percent_armor_mod

    @property
    def flat_magic_penetration_mod(self) -> float:
        return self._data[RuneStatsData].flat_magic_penetration_mod

    @property
    def percent_crit_chance_mod(self) -> float:
        return self._data[RuneStatsData].percent_crit_chance_mod

    @property
    def flat_physical_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_physical_damage_mod_per_level

    @property
    def percent_armor_penetration_mod(self) -> float:
        return self._data[RuneStatsData].percent_armor_penetration_mod

    @property
    def percent_exp_bonus(self) -> float:
        return self._data[RuneStatsData].percent_exp_bonus

    @property
    def flat_mp_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_mp_regen_mod_per_level

    @property
    def percent_magic_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percent_magic_penetration_mod_per_level

    @property
    def flat_time_dead_mod(self) -> float:
        return self._data[RuneStatsData].flat_time_dead_mod

    @property
    def flat_movement_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_movement_speed_mod_per_level

    @property
    def flat_gold_per_10_mod(self) -> float:
        return self._data[RuneStatsData].flat_gold_per_10_mod

    @property
    def flat_armor_penetration_mod(self) -> float:
        return self._data[RuneStatsData].flat_armor_penetration_mod

    @property
    def flat_crit_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flat_crit_damage_mod_per_level

    @property
    def flat_hp_pool_mod(self) -> float:
        return self._data[RuneStatsData].flat_hp_pool_mod

    @property
    def flat_crit_chance_mod(self) -> float:
        return self._data[RuneStatsData].flat_crit_chance_mod

    @property
    def flat_exp_bonus(self) -> float:
        return self._data[RuneStatsData].flat_exp_bonus


@searchable({str: ["name", "tags", "type", "region", "platform", "locale"], int: ["id"], RuneType: ["type"], Region: ["region"], Platform: ["platform"]})
class Rune(CassiopeiaGhost):
    _data_types = {RuneData}

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
        if hasattr(self._data[RuneData], "id"):
            query["id"] = self._data[RuneData].id
        if hasattr(self._data[RuneData], "name"):
            query["name"] = self._data[RuneData].name
        return query

    @lazy_property
    def region(self) -> Region:
        """The region for this rune."""
        return Region(self._data[RuneData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this rune."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this rune."""
        try:
            return self._data[RuneData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="rune")
            self(version=version)
            return self._data[RuneData].version

    @property
    def locale(self) -> str:
        """The locale for this rune."""
        return self._data[RuneData].locale or self.region.default_locale

    @lazy_property
    def included_data(self) -> Set[str]:
        """The region for this rune."""
        return self._data[RuneData].includedData

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def tier(self) -> int:
        return self._data[RuneData].metadata.tier

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def type(self) -> RuneType:
        return RuneType(self._data[RuneData].metadata.type)

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def name(self) -> str:
        """The rune's name."""
        return self._data[RuneData].name

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def id(self) -> int:
        """The rune's ID."""
        return self._data[RuneData].id

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def description(self) -> int:
        """The rune's description."""
        return self._data[RuneData].description

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def sanitized_description(self) -> int:
        """The rune's sanitized description."""
        return self._data[RuneData].sanitizedDescription

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def stats(self) -> RuneStats:
        return RuneStats.from_data(self._data[RuneData].stats)

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def tags(self) -> List[str]:
        return self._data[RuneData].id

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        """The image information for this rune."""
        image = Image.from_data(self._data[RuneData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.spriteInfo
