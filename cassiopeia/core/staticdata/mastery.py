from typing import Set, Union

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ...data import Region, Platform, MasteryTree
from ..common import CoreData, DataObjectList, CassiopeiaGhost, CassiopeiaList, get_latest_version, provide_default_region, ghost_load_on
from .common import Sprite, Image, ImageData
from ...dto.staticdata import mastery as dto


##############
# Data Types #
##############


class MasteryListData(DataObjectList):
    _dto_type = dto.MasteryListDto
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


class MasteryData(CoreData):
    _dto_type = dto.MasteryDto
    _renamed = {"prerequisite": "prereq", "tree": "masteryTree", "image_data": "image", "points": "ranks", "sanitized_description": "sanitizedDescription", "included_data": "includedData"}

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
    def prerequisite(self) -> id:
        """Always '0'"""
        return self._dto["prereq"]

    @property
    def tree(self) -> str:
        """Legal values: Cunning, Ferocity, Resolve"""
        return self._dto["masteryTree"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def points(self) -> list:
        return self._dto["ranks"]

    @property
    def image_data(self) -> str:
        return ImageData.from_dto(self._dto["image"])

    @property
    def id(self) -> str:
        return self._dto["id"]

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def description(self) -> str:
        return self._dto["description"]


##############
# Core Types #
##############


class Masteries(CassiopeiaList):
    _data_types = {MasteryListData}

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
        return Region(self._data[MasteryListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[MasteryListData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="mastery")
            self(version=version)
            return self._data[MasteryListData].version

    @property
    def locale(self) -> str:
        return self._data[MasteryListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additional information for this mastery when it's loaded."""
        return self._data[MasteryListData].included_data


@searchable({str: ["name", "key", "region", "platform", "locale", "tree"], int: ["id"], MasteryTree: ["tree"], Region: ["region"], Platform: ["platform"]})
class Mastery(CassiopeiaGhost):
    _data_types = {MasteryData}

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
        if "id" in self._data[MasteryData]._dto:
            query["id"] = self._data[MasteryData].id
        if "name" in self._data[MasteryData]._dto:
            query["name"] = self._data[MasteryData].name
        return query

    @lazy_property
    def region(self) -> Region:
        """The region for this mastery."""
        return Region(self._data[MasteryData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this mastery."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this mastery."""
        try:
            return self._data[MasteryData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="mastery")
            self(version=version)
            return self._data[MasteryData].version

    @property
    def locale(self) -> str:
        """The locale for this mastery."""
        return self._data[MasteryData].locale or self.region.default_locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additional information for this mastery when it's loaded."""
        return self._data[MasteryData].included_data

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def prerequisite(self) -> "Mastery":
        """The prerequisite masteries."""
        return Mastery(id=self._data[MasteryData].prerequisite, region=self.region, version=self.version)

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def tree(self) -> MasteryTree:
        """The mastery's tree (Cunning, Ferocity, Resolve)."""
        return MasteryTree(self._data[MasteryData].tree)

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def name(self) -> str:
        """The mastery's name."""
        return self._data[MasteryData].name

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def points(self) -> str:
        """The number of points that can be put into this mastery."""
        return self._data[MasteryData].points

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def id(self) -> int:
        """The mastery's ID."""
        return self._data[MasteryData].id

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def description(self) -> int:
        """The mastery's description."""
        return self._data[MasteryData].description

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def sanitized_description(self) -> int:
        """The mastery's sanitized description."""
        return self._data[MasteryData].sanitized_description

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    def id(self) -> int:
        """The mastery's ID."""
        return self._data[MasteryData].id

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on
    @lazy
    def image(self) -> Image:
        """The image information for this mastery."""
        image = Image.from_data(self._data[MasteryData].image_data)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
