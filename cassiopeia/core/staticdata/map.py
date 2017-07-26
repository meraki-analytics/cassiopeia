from typing import List
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform
from ..common import DataObject, CassiopeiaGhost, DataObjectList, CassiopeiaGhostList, get_latest_version
from .common import Sprite, Image, ImageData
from ...dto.staticdata import map as dto


##############
# Data Types #
##############


class MapListData(DataObjectList):
    _dto_type = dto.MapListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]


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
        return ImageData.from_dto(self._dto["image"])

    @property
    def name(self) -> str:
        return self._dto["mapName"]

    @property
    def unpurchasable_items(self) -> List[int]:
        return self._dto["unpurchasableItemList"]


##############
# Core Types #
##############


class Maps(CassiopeiaGhostList):
    _data_types = {MapListData}

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
        SearchableList.__init__(self, [StaticDataTransformer.map_data_to_core(None, i) for i in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MapListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[MapListData].version
        except KeyError:
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[MapListData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[MapListData].locale


@searchable({str: ["name", "locale"], int: ["id"]})
class Map(CassiopeiaGhost):
    _data_types = {MapData}
    _load_types = {MapData: Maps}

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
        except KeyError:
            version = get_latest_version(region=self.region)
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
