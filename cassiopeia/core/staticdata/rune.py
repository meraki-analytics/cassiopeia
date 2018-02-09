from typing import List, Set, Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ...data import Region, Platform, RunePath
from ..common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, get_latest_version, provide_default_region, ghost_load_on
from .common import Sprite, Image
from ...dto.staticdata import rune as dto


##############
# Data Types #
##############


class RuneListData(CoreDataList):
    _dto_type = dto.RuneListDto
    _renamed = {"included_data": "includedData"}


class RuneData(CoreData):
    _dto_type = dto.RuneDto
    _renamed = {"longDesc": "longDescription", "shortDesc": "shortDescription", "endOfGameStatDescs": "endOfGameStatDescriptions", "included_data": "includedData"}


##############
# Core Types #
##############


class Runes(CassiopeiaLazyList):
    _data_types = {RuneListData}

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

    @property
    def precision(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.path == RunePath.precision)

    @property
    def dominion(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.path == RunePath.dominion)

    @property
    def sorcery(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.path == RunePath.sorcery)

    @property
    def resolve(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.path == RunePath.resolve)

    @property
    def inspiration(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.path == RunePath.inspiration)

    @property
    def keystones(self) -> List["Rune"]:
        return self.filter(lambda rune: rune.is_keystone)


@searchable({str: ["name", "tags", "path", "region", "platform", "locale"], int: ["id"], RunePath: ["path"], Region: ["region"], Platform: ["platform"]})
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

    def __eq__(self, other: "Rune"):
        if not isinstance(other, Rune) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[RuneData], "id"): s["id"] = self.id
        if hasattr(other._data[RuneData], "id"): o["id"] = other.id
        if hasattr(self._data[RuneData], "name"): s["name"] = self.name
        if hasattr(other._data[RuneData], "name"): o["name"] = other.name
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    __hash__ = CassiopeiaGhost.__hash__

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

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[RuneData].includedData

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def path(self) -> RunePath:
        return RunePath(self._data[RuneData].path)

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def tier(self) -> int:
        return self._data[RuneData].tier

    @property
    def is_keystone(self) -> bool:
        return self.tier == 0

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
    def short_description(self) -> str:
        return self._data[RuneData].shortDescription

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def long_description(self) -> str:
        return self._data[RuneData].longDescription

    #@CassiopeiaGhost.property(RuneData)
    #@ghost_load_on
    #def end_of_game_stat_descriptions(self) -> List[str]:
    #    print(self._data[RuneData].to_dict().keys())
    #    return self._data[RuneData].endOfGameStatDescriptions

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        """The image information for this rune."""
        raise NotImplemented  # TODO
        image = Image.from_data(self._data[RuneData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.spriteInfo
