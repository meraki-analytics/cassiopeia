from typing import List
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform
from ..common import DataObject, CassiopeiaGhost
from .common import Sprite, Image, ImageData
from .version import VersionListData
from ...dto.staticdata import map as dto


##############
# Data Types #
##############


class MapListData(list):
    _dto_type = dto.MapListDto


class MapData(DataObject):
    _dto_type = dto.MapDto
    _renamed = {"id": "mapId", "name": "mapName", "unpurchasable_items": "unpurchasableItemList"}

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
    def id(self) -> int:
        return self._dto["mapId"]

    @property
    def image(self) -> ImageData:
        return ImageData(self._dto["image"])

    @property
    def name(self) -> str:
        return self._dto["mapName"]

    @property
    def unpurchasable_items(self) -> List[int]:
        return self._dto["unpurchasableItemList"]


##############
# Core Types #
##############


class Maps(SearchableList):
    pass


@searchable({str: ["name", "locale"], int: ["id"]})
class Map(CassiopeiaGhost):
    _data_types = {MapData}
    _load_types = {MapData: Maps}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    def __load_hook__(self, load_group, core) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item

        # The `core` is a dict of map core instances
        if "mapId" in self._data[MapData]._dto:
            find = "mapId", self.id
        elif "mapName" in self._data[MapData]._dto:
            find = "mapName", self.name
        else:
            raise ValueError("unknown `id` and `name`")
        core = find_matching_attribute(core, *find)
        super().__load_hook__(load_group, core)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[MapData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this map."""
        try:
            return self._data[MapData].version
        except AttributeError:
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
            self(version=version)
            return self._data[MapData].version

    @property
    def locale(self) -> str:
        """The locale for this map."""
        return self._data[MapData].locale

    @CassiopeiaGhost.property(MapData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The map's ID."""
        return self._data[MapData].id

    @CassiopeiaGhost.property(MapData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[MapData].name

    @CassiopeiaGhost.property(MapData)
    @ghost_load_on(KeyError)
    def unpurchasable_items(self) -> List[int]:
        return self._data[MapData].unpurchasable_items

    @CassiopeiaGhost.property(MapData)
    @ghost_load_on(KeyError)
    @lazy
    def image_info(self) -> Image:
        """The image information for this champion."""
        return Image(self._data[MapData].image, version=self.version)

    @lazy_property
    def image(self) -> PILImage:
        """The image icon for this champion."""
        return settings.pipeline.get(PILImage, query={"url": self.image_info.url})

    @lazy_property
    def sprite(self) -> Sprite:
        """The sprite that contains this champion's image icon."""
        return self.image_info.sprite.image
