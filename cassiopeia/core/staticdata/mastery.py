from typing import Set
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, MasteryTree
from ..common import DataObject, DataObjectList, CassiopeiaGhost, CassiopeiaGhostList, get_latest_version
from .common import Sprite, Image
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


class MasteryData(DataObject):
    _dto_type = dto.MasteryDto
    _renamed = {"prerequisite": "prereq", "tree": "masteryTree", "image_data": "image", "points": "ranks", "sanitized_description": "sanitizedDescription"}

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
        return self._dto["image"]

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


class Masteries(CassiopeiaGhostList):
    _data_types = {MasteryListData}

    def __get_query__(self):
        query = {"platform": self.platform, "version": self.version}
        try:
            query["locale"] = self.locale
        except KeyError:
            pass
        return query

    def __load_hook__(self, load_group, data: DataObject):
        self.clear()
        from ...transformers.staticdata import StaticDataTransformer
        SearchableList.__init__(self, [StaticDataTransformer.mastery_data_to_core(None, i) for i in data])
        super().__load_hook__(load_group, data)

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
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[MasteryListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[MasteryListData].locale

    @property
    def included_data(self) -> Set[str]:
        """A set of tags to return additonal information for this champion when it's loaded."""
        return self._data[MasteryListData].included_data


@searchable({str: ["name", "key", "region", "platform", "locale", "tree"], int: ["id"], MasteryTree: ["tree"], Region: ["region"], Platform: ["platform"]})
class Mastery(CassiopeiaGhost):
    _data_types = {MasteryData}
    _load_types = {MasteryData: Masteries}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

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
        except AttributeError:
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[MasteryData].version

    @property
    def locale(self) -> str:
        """The locale for this mastery."""
        return self._data[MasteryData].locale

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def prerequisite(self) -> "Mastery":
        """The prerequisite masteries."""
        return Mastery(self._data[MasteryData].prerequisite)

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def tree(self) -> MasteryTree:
        """The mastery's tree (Cunning, Ferocity, Resolve)."""
        return MasteryTree(self._data[MasteryData].tree)

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        """The mastery's name."""
        return self._data[MasteryData].name

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def points(self) -> str:
        """The number of points that can be put into this mastery."""
        return self._data[MasteryData].points

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The mastery's ID."""
        return self._data[MasteryData].id

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def description(self) -> int:
        """The mastery's description."""
        return self._data[MasteryData].description

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def sanitized_description(self) -> int:
        """The mastery's sanitized description."""
        return self._data[MasteryData].sanitized_description

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The mastery's ID."""
        return self._data[MasteryData].id

    @CassiopeiaGhost.property(MasteryData)
    @ghost_load_on(KeyError)
    @lazy
    def image_info(self) -> Image:
        """The image information for this mastery."""
        return Image(self._data[MasteryData].image, version=self.version)

    @lazy_property
    def image(self) -> PILImage:
        """The image icon for this mastery."""
        return settings.pipeline.get(PILImage, query={"url": self.image_info.url})

    @lazy_property
    def sprite(self) -> Sprite:
        """The sprite that contains this mastery's image icon."""
        return self.image_info.sprite.image
