from typing import List, Union, Set

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Resource, Region, Platform, GameMode
from ..common import CoreData, DataObjectList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList, get_latest_version
from .common import ImageData, Image, Sprite
from ...dto.staticdata import summonerspell as dto


##############
# Data Types #
##############


class SummonerSpellListData(DataObjectList):
    _dto_type = dto.SummonerSpellListDto
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


class SummonerSpellData(CoreData):
    _dto_type = dto.SummonerSpellDto
    _renamed = {"variables": "vars", "sanitized_description": "sanitizedDescription", "sanitized_tooltip": "sanitizedTooltip", "max_rank": "maxrank", "cooldowns": "cooldown", "costs": "cost", "alternative_images": "altimages", "effects": "effect", "resource": "costType", "included_data": "includedData"}

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
    def included_data(self) -> str:
        return self._dto["includedData"]

    @property
    def modes(self) -> List[str]:
        return self._dto["modes"]

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
    def id(self) -> int:
        return self._dto["id"]

    @property
    def name(self) -> str:
        return self._dto["name"]


##############
# Core Types #
##############


class SummonerSpells(CassiopeiaGhostList):
    _data_types = {SummonerSpellListData}

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
        SearchableList.__init__(self, [StaticDataTransformer.summoner_spell_data_to_core(None, ss) for ss in data])
        super().__load_hook__(load_group, data)

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
        except KeyError:
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
        return self._data[SummonerSpellListData].included_data


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
class SummonerSpell(CassiopeiaGhost):
    _data_types = {SummonerSpellData}
    _load_types = {SummonerSpellData: SummonerSpellListData}

    def __init__(self, *, id: int = None, name: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None, included_data: Set[str] = None):
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

        # The `data` is a dict of summoner spell data instances
        if "name" in self._data[SummonerSpellData]._dto:
            find = "name", self.name
        elif "id" in self._data[SummonerSpellData]._dto:
            find = "id", self.id
        else:
            raise RuntimeError("Expected fields not present after loading.")
        data = find_matching_attribute(data, *find)

        super().__load_hook__(load_group, data)

    # What do we do about params like this that can exist in both data objects?
    # They will be set on both data objects always, so we can choose either one to return.
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
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="summoner")
            self(version=version)
            return self._data[SummonerSpellData].version

    @property
    def locale(self) -> str:
        """The locale for this summoner spell."""
        return self._data[SummonerSpellData].locale

    @property
    def included_data(self) -> Set[str]:
        """The data to included in the query for this summoner spell."""
        return self._data[SummonerSpellData].included_data

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def modes(self) -> List[GameMode]:
        return SearchableList([GameMode(mode) for mode in self._data[SummonerSpellData].modes])

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def variables(self) -> List[SpellVars]:
        """Contains spell data."""
        return SearchableList(SpellVars(v) for v in self._data[SummonerSpellData].variables)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def resource(self) -> Resource:
        """The resource consumed when using this spell."""
        return Resource(self._data[SummonerSpellData].resource)

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def sanitized_description(self) -> str:
        """The spell's sanitized description."""
        return self._data[SummonerSpellData].sanitized_description

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def sanitized_tooltip(self) -> str:
        """The spell's sanitized tooltip."""
        return self._data[SummonerSpellData].sanitized_tooltip

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def effects(self) -> List[List[float]]:
        """The level-by-level replacements for {{ e# }} tags in other values."""
        return SearchableList(self._data[SummonerSpellData].effects)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def tooltip(self) -> str:
        """The spell's tooltip."""
        return self._data[SummonerSpellData].tooltip

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def max_rank(self) -> int:
        """The maximum rank this spell can attain."""
        return self._data[SummonerSpellData].max_rank

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def range(self) -> List[Union[int, str]]:
        """The maximum range of this spell. `self` if it has no range."""
        return SearchableList(self._data[SummonerSpellData].range)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def cooldowns(self) -> List[float]:
        """The cooldowns of this spell (per level)."""
        return SearchableList(self._data[SummonerSpellData].cooldowns)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def costs(self) -> List[int]:
        """The resource costs of this spell (per level)."""
        return SearchableList(self._data[SummonerSpellData].costs)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def key(self) -> str:
        """The spell's key."""
        return self._data[SummonerSpellData].key

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def description(self) -> str:
        """The spell's description."""
        return self._data[SummonerSpellData].description

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def alternative_images(self) -> List[Image]:
        """The alternative images for this spell. These won't exist after patch NN, when Riot standardized all images."""
        return SearchableList(Image(alt) for alt in self._data[SummonerSpellData].alternative_images)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The spell's id."""
        return self._data[SummonerSpellData].id

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        """The spell's name."""
        return self._data[SummonerSpellData].name

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def image(self) -> Image:
        image = Image(self._data[SummonerSpellData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
