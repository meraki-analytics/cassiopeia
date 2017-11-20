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


class RuneStatsData(CoreData):
    _renamed = {}


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
        return self._data[RuneStatsData].percentTimeDeadModPerLevel

    @property
    def percent_armor_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percentArmorPenetrationModPerLevel

    @property
    def percent_crit_damage_mod(self) -> float:
        return self._data[RuneStatsData].percentCritDamageMod

    @property
    def percent_spell_block_mod(self) -> float:
        return self._data[RuneStatsData].percentSpellBlockMod

    @property
    def percent_hp_regen_mod(self) -> float:
        return self._data[RuneStatsData].percentHpRegenMod

    @property
    def percent_movement_speed_mod(self) -> float:
        return self._data[RuneStatsData].percentMovementSpeedMod

    @property
    def flat_spell_block_mod(self) -> float:
        return self._data[RuneStatsData].flatSpellBlockMod

    @property
    def flat_energy_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatEnergyRegenModPerLevel

    @property
    def flat_energy_pool_mod(self) -> float:
        return self._data[RuneStatsData].flatEnergyPoolMod

    @property
    def flat_magic_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatMagicPenetrationModPerLevel

    @property
    def percent_life_steal_mod(self) -> float:
        return self._data[RuneStatsData].percentLifeStealMod

    @property
    def flat_mp_pool_mod(self) -> float:
        return self._data[RuneStatsData].flatMpPoolMod

    @property
    def percent_cooldown_mod(self) -> float:
        return self._data[RuneStatsData].percentCooldownMod

    @property
    def percent_magic_penetration_mod(self) -> float:
        return self._data[RuneStatsData].percentMagicPenetrationMod

    @property
    def flat_armor_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatArmorPenetrationModPerLevel

    @property
    def flat_movement_speed_mod(self) -> float:
        return self._data[RuneStatsData].flatMovementSpeedMod

    @property
    def flat_time_dead_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatTimeDeadModPerLevel

    @property
    def flat_armor_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatArmorModPerLevel

    @property
    def percent_attack_speed_mod(self) -> float:
        return self._data[RuneStatsData].percentAttackSpeedMod

    @property
    def flat_dodge_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatDodgeModPerLevel

    @property
    def percent_magic_damage_mod(self) -> float:
        return self._data[RuneStatsData].percentMagicDamageMod

    @property
    def percent_block_mod(self) -> float:
        return self._data[RuneStatsData].percentBlockMod

    @property
    def flat_dodge_mod(self) -> float:
        return self._data[RuneStatsData].flatDodgeMod

    @property
    def flat_energy_regen_mod(self) -> float:
        return self._data[RuneStatsData].flatEnergyRegenMod

    @property
    def flat_hp_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatHpModPerLevel

    @property
    def percent_attack_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percentAttackSpeedModPerLevel

    @property
    def percent_spell_vamp_mod(self) -> float:
        return self._data[RuneStatsData].percentSpellVampMod

    @property
    def flat_mp_regen_mod(self) -> float:
        return self._data[RuneStatsData].flatMpRegenMod

    @property
    def percent_hp_pool_mod(self) -> float:
        return self._data[RuneStatsData].percentHpPoolMod

    @property
    def percent_dodge_mod(self) -> float:
        return self._data[RuneStatsData].percentDodgeMod

    @property
    def flat_attack_speed_mod(self) -> float:
        return self._data[RuneStatsData].flatAttackSpeedMod

    @property
    def flat_armor_mod(self) -> float:
        return self._data[RuneStatsData].flatArmorMod

    @property
    def flat_magic_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatMagicDamageModPerLevel

    @property
    def flat_hp_regen_mod(self) -> float:
        return self._data[RuneStatsData].flatHpRegenMod

    @property
    def percent_physical_damage_mod(self) -> float:
        return self._data[RuneStatsData].percentPhysicalDamageMod

    @property
    def flat_crit_chance_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatCritChanceModPerLevel

    @property
    def flat_spell_block_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatSpellBlockModPerLevel

    @property
    def percent_time_dead_mod(self) -> float:
        return self._data[RuneStatsData].percentTimeDeadMod

    @property
    def flat_block_mod(self) -> float:
        return self._data[RuneStatsData].flatBlockMod

    @property
    def percent_mp_pool_mod(self) -> float:
        return self._data[RuneStatsData].percentMpPoolMod

    @property
    def flat_magic_damage_mod(self) -> float:
        return self._data[RuneStatsData].flatMagicDamageMod

    @property
    def percent_mp_regen_mod(self) -> float:
        return self._data[RuneStatsData].percentMpRegenMod

    @property
    def percent_movement_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percentMovementSpeedModPerLevel

    @property
    def percent_cooldown_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percentCooldownModPerLevel

    @property
    def flat_mp_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatMpModPerLevel

    @property
    def flat_energy_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatEnergyModPerLevel

    @property
    def flat_physical_damage_mod(self) -> float:
        return self._data[RuneStatsData].flatPhysicalDamageMod

    @property
    def flat_hp_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatHpRegenModPerLevel

    @property
    def flat_crit_damage_mod(self) -> float:
        return self._data[RuneStatsData].flatCritDamageMod

    @property
    def percent_armor_mod(self) -> float:
        return self._data[RuneStatsData].percentArmorMod

    @property
    def flat_magic_penetration_mod(self) -> float:
        return self._data[RuneStatsData].flatMagicPenetrationMod

    @property
    def percent_crit_chance_mod(self) -> float:
        return self._data[RuneStatsData].percentCritChanceMod

    @property
    def flat_physical_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatPhysicalDamageModPerLevel

    @property
    def percent_armor_penetration_mod(self) -> float:
        return self._data[RuneStatsData].percentArmorPenetrationMod

    @property
    def percent_exp_bonus(self) -> float:
        return self._data[RuneStatsData].percentExpBonus

    @property
    def flat_mp_regen_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatMpRegenModPerLevel

    @property
    def percent_magic_penetration_mod_per_level(self) -> float:
        return self._data[RuneStatsData].percentMagicPenetrationModPerLevel

    @property
    def flat_time_dead_mod(self) -> float:
        return self._data[RuneStatsData].flatTimeDeadMod

    @property
    def flat_movement_speed_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatMovementSpeedModPerLevel

    @property
    def flat_gold_per_10_mod(self) -> float:
        return self._data[RuneStatsData].flatGoldPer_10Mod

    @property
    def flat_armor_penetration_mod(self) -> float:
        return self._data[RuneStatsData].flatArmorPenetrationMod

    @property
    def flat_crit_damage_mod_per_level(self) -> float:
        return self._data[RuneStatsData].flatCritDamageModPerLevel

    @property
    def flat_hp_pool_mod(self) -> float:
        return self._data[RuneStatsData].flatHpPoolMod

    @property
    def flat_crit_chance_mod(self) -> float:
        return self._data[RuneStatsData].flatCritChanceMod

    @property
    def flat_exp_bonus(self) -> float:
        return self._data[RuneStatsData].flatExpBonus


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
