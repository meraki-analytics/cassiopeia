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


class RuneData(CoreData):
    _dto_type = dto.RuneDto
    _renamed = {"longDesc": "longDescription", "shortDesc": "shortDescription", "endOfGameStatDescs": "endOfGameStatDescriptions", "included_data": "includedData"}


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

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[RuneData].includedData

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def type(self) -> RuneType:
        rune_types = {
            "80": RuneType.precision,
            "81": RuneType.domination,
            "82": RuneType.sorcery,
            "83": RuneType.inspiration,
            "84": RuneType.resolve,
            "91": RuneType.precision
        }
        return rune_types[str(self.id)[:2]]

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
        return self._data[RuneData].short_description

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def long_description(self) -> str:
        return self._data[RuneData].long_description

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on
    def end_of_game_descriptions(self) -> List[str]:
        return self._data[RuneData].endOfGameDescriptions

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
