from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ...configuration import settings
from ...data import Region, Platform, MasteryTree
from ..common import DataObject, CassiopeiaGhost
from .common import Sprite, Image
from .version import VersionListData
from ...dto.staticdata import mastery as dto


class MasteryListData(list):
    _dto_type = dto.MasteryListDto


##############
# Data Types #
##############


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


@searchable({str: ["name", "key", "region", "platform", "locale", "tree"], int: ["id"], MasteryTree: ["tree"], Region: ["region"], Platform: ["platform"]})
class Mastery(CassiopeiaGhost):
    _data_types = {MasteryData}

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
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
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
