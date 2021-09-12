from typing import List, Union, Set

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...data import Resource, Region, Platform, GameMode
from ..common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, get_latest_version, ghost_load_on
from .common import ImageData, Image, Sprite
from ...dto.staticdata import summonerspell as dto


##############
# Data Types #
##############


class SummonerSpellListData(CoreDataList):
    _dto_type = dto.SummonerSpellListDto
    _renamed = {"included_data": "includedData"}


class SpellVarsData(CoreData):
    _renamed = {"dyn": "dynamic", "coeff": "coefficients"}


class LevelTipData(CoreData):
    _renamed = {"effect": "effects", "label": "keywords"}


class SummonerSpellData(CoreData):
    _dto_type = dto.SummonerSpellDto
    _renamed = {"maxrank": "maxRank", "cooldown": "cooldowns", "cost": "costs", "effect": "effects", "costType": "resource", "included_data": "includedData"}

    def __call__(self, **kwargs):
        if "vars" in kwargs:
            self.variables = [SpellVarsData(**v) for v in kwargs.pop("vars")]
        if "altimages" in kwargs:
            self.alternativeImages = [ImageData(**alt) for alt in kwargs.pop("altimages")]
        if "image" in kwargs:
            self.image = ImageData(**kwargs.pop("image"))
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class SummonerSpells(CassiopeiaLazyList):
    _data_types = {SummonerSpellListData}

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
        return Region(self._data[SummonerSpellListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[SummonerSpellListData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="summoner")
            self(version=version)
            return self._data[SummonerSpellListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[SummonerSpellListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[SummonerSpellListData].includedData


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


@searchable({str: ["name", "key", "keywords"]})
class SummonerSpell(CassiopeiaGhost):
    _data_types = {SummonerSpellData}

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
        if hasattr(self._data[SummonerSpellData], "id"):
            query["id"] = self._data[SummonerSpellData].id
        if hasattr(self._data[SummonerSpellData], "name"):
            query["name"] = self._data[SummonerSpellData].name
        return query

    def __eq__(self, other: "SummonerSpell"):
        if not isinstance(other, SummonerSpell) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[SummonerSpellData], "id"): s["id"] = self.id
        if hasattr(other._data[SummonerSpellData], "id"): o["id"] = other.id
        if hasattr(self._data[SummonerSpellData], "name"): s["name"] = self.name
        if hasattr(other._data[SummonerSpellData], "name"): o["name"] = other.name
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = "?"
        name = "?"
        if hasattr(self._data[SummonerSpellData], "id"):
            id_ = self.id
        if hasattr(self._data[SummonerSpellData], "name"):
            name = self.name
        return "SummonerSpell(name='{name}', id={id_}, region='{region}')".format(name=name, id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

    @lazy_property
    def region(self) -> Region:
        """The region for this summoner spell."""
        return Region(self._data[SummonerSpellData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this summoner spell."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this summoner spell."""
        try:
            return self._data[SummonerSpellData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="summoner")
            self(version=version)
            return self._data[SummonerSpellData].version

    @property
    def locale(self) -> str:
        """The locale for this summoner spell."""
        return self._data[SummonerSpellData].locale or self.region.default_locale

    @property
    def included_data(self) -> Set[str]:
        """The data to included in the query for this summoner spell."""
        return self._data[SummonerSpellData].includedData

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def modes(self) -> List[GameMode]:
        return SearchableList([GameMode(mode) for mode in self._data[SummonerSpellData].modes])

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def variables(self) -> List[SpellVars]:
        """Contains spell data."""
        return SearchableList(SpellVars(v) for v in self._data[SummonerSpellData].variables)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def resource(self) -> Resource:
        """The resource consumed when using this spell."""
        return Resource(self._data[SummonerSpellData].resource)

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[SummonerSpellData].sanitized_description

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def sanitized_tooltip(self) -> str:
        """The spell's sanitized tooltip."""
        return self._data[SummonerSpellData].sanitizedTooltip

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def effects(self) -> List[List[float]]:
        """The level-by-level replacements for {{ e# }} tags in other values."""
        return SearchableList(self._data[SummonerSpellData].effects)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def tooltip(self) -> str:
        """The spell's tooltip."""
        return self._data[SummonerSpellData].tooltip

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def max_rank(self) -> int:
        """The maximum rank this spell can attain."""
        return self._data[SummonerSpellData].maxRank

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def range(self) -> List[Union[int, str]]:
        """The maximum range of this spell. `self` if it has no range."""
        return SearchableList(self._data[SummonerSpellData].range)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def cooldowns(self) -> List[float]:
        """The cooldowns of this spell (per level)."""
        return SearchableList(self._data[SummonerSpellData].cooldowns)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def costs(self) -> List[int]:
        """The resource costs of this spell (per level)."""
        return SearchableList(self._data[SummonerSpellData].costs)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def key(self) -> str:
        """The spell's key."""
        return self._data[SummonerSpellData].key

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def description(self) -> str:
        """The spell's description."""
        return self._data[SummonerSpellData].description

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def alternative_images(self) -> List[Image]:
        """The alternative images for this spell. These won't exist after patch NN, when Riot standardized all images."""
        return SearchableList(Image.from_data(alt) for alt in self._data[SummonerSpellData].alternativeImages)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def id(self) -> int:
        """The spell's id."""
        return self._data[SummonerSpellData].id

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    def name(self) -> str:
        """The spell's name."""
        return self._data[SummonerSpellData].name

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        image = Image.from_data(self._data[SummonerSpellData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.spriteInfo
