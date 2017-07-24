from typing import List, Union, Set

from PIL.Image import Image as PILImage
from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Resource, Region, Platform, GameMode
from ..common import DataObject, DataObjectList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaGhostList, get_latest_version
from .common import Image, ImageData
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


class SpellVarsData(DataObject):
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


class LevelTipData(DataObject):
    _renamed = {"effects": "effect", "keywords": "label"}

    @property
    def effects(self) -> List[str]:
        return self._dto["effect"]

    @property
    def keywords(self) -> List[str]:
        return self._dto["label"]


class SummonerSpellData(DataObject):
    _dto_type = dto.SummonerSpellDto
    _renamed = {"level_up_tips": "leveltip", "variables": "vars", "sanitized_description": "sanitizedDescription", "sanitized_tooltip": "sanitizedTooltip",
                "max_rank": "maxrank", "cooldowns": "cooldown", "costs": "cost", "alternative_images": "altimages", "effects": "effect", "resource": "costType"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def modes(self) -> List[str]:
        return self._dto["modes"]

    @property
    def level_up_tips(self) -> LevelTipData:
        return LevelTipData(self._dto["leveltip"])

    @property
    def variables(self) -> List[SpellVarsData]:
        return [SpellVarsData(v) for v in self._dto["vars"]]

    @property
    def resource(self) -> str:
        return self._dto["costType"]

    @property
    def image(self) -> ImageData:
        return ImageData(self._dto["image"])

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
        return [ImageData(alt) for alt in self._dto["altimages"]]

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

    def __get_query__(self):
        return {"region": self.region}

    def __load_hook__(self, load_group, data: DataObject):
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
        except AttributeError:
            version = get_latest_version(region=self.region)
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
    _load_types = {SummonerSpellData: SummonerSpells}

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
        if "name" in self._data[SummonerSpellData]._dto:
            find = "name", self.name
        elif "id" in self._data[SummonerSpellData]._dto:
            find = "id", self.id
        else:
            raise RuntimeError("Expected fields not present after loading.")
        core = find_matching_attribute(core, *find)

        super().__load_hook__(load_group, core)

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
        except AttributeError:
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[SummonerSpellData].version

    @property
    def locale(self) -> str:
        """The locale for this summoner spell."""
        return self._data[SummonerSpellData].locale

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def modes(self) -> List[str]:
        return SearchableList([GameMode(mode) for mode in self._data[SummonerSpellData].modes])

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def keywords(self) -> List[str]:
        """The keywords for this spell."""
        return SearchableList(self._data[SummonerSpellData].level_up_tips.keywords)

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def effects_by_level(self) -> List[str]:
        """The level-up changes, level-by-level."""
        return SearchableList(self._data[SummonerSpellData].level_up_tips.effects)

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

    @CassiopeiaGhost.property(SummonerSpellData)
    @ghost_load_on(KeyError)
    @lazy
    def image_info(self) -> Image:
        """The info about the spell's image, which can be pulled from datadragon."""
        return Image(self._data[SummonerSpellData].image)

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
