from typing import Dict, List, Set, Union, Mapping, Any
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, Map
from ..common import DataObject, CassiopeiaObject, CassiopeiaGhost, Ghost
from .version import VersionListData
from ...dto.staticdata import map as dto


class MapListData(list):
    _dto_type = dto.MapListDto


##############
# Data Types #
##############


class SpriteData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def height(self) -> int:
        return self._dto["h"]


class ImageData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def full(self) -> str:
        return self._dto["full"]

    @property
    def group(self) -> str:
        return self._dto["group"]

    @property
    def height(self) -> int:
        return self._dto["h"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]


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


@searchable({str: ["sprite", "url"]})
class Sprite(CassiopeiaObject):
    _data_types = {SpriteData}
    _extension = "png"

    @property
    def version(self) -> str:
        return self._data[SpriteData].version

    @property
    def sprite(self) -> str:
        return self._data[SpriteData].sprite

    @property
    def y(self) -> int:
        return self._data[SpriteData].y

    @property
    def x(self) -> int:
        return self._data[SpriteData].x

    @property
    def width(self) -> int:
        return self._data[SpriteData].width

    @property
    def height(self) -> int:
        return self._data[SpriteData].height

    @property
    def url(self) -> str:
        sprite = self.sprite
        if "." in sprite:
            sprite, self._extension = sprite.split(".")
        # There are not multiple images for different regions; this one works for all regions, so we don't need it
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/sprite/{sprite}.{ext}".format(version=self.version, sprite=sprite, ext=self._extension)

    @lazy_property
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})


@searchable({str: ["full", "url"]})
class Image(CassiopeiaObject):
    _data_types = {ImageData}
    _extension = "png"

    @property
    def version(self) -> str:
        return self._data[ImageData].version

    @property
    def full(self) -> str:
        return self._data[ImageData].full

    @property
    def group(self) -> str:
        return self._data[ImageData].group

    @property
    def url(self) -> str:
        if "." in self.full:
            full, self._extension = self.full.split(".")
        # There are not multiple images for different regions; this one works for all regions, so we don't need it
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/{group}/{full}.{ext}".format(version=self.version, group=self.group, full=full, ext=self._extension)

    @lazy_property
    def sprite(self) -> Sprite:
        sprite = Sprite(w=self._data[ImageData].width,
                      h=self._data[ImageData].height,
                      x=self._data[ImageData].x,
                      y=self._data[ImageData].y,
                      sprite=self._data[ImageData].sprite,
                      version=self._data[ImageData].version)
        return sprite


@searchable({str: ["name", "locale"], int: ["id"]})
class Map(CassiopeiaGhost):
    _data_types = {MapData}
    _load_types = {MapData: MapListData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    def __load_hook__(self, load_group, dto) -> None:
        def find_matching_attribute(iterable, attrname, attrvalue):
            for item in iterable:
                if item.get(attrname, None) == attrvalue:
                    return item

        # The `dto` is a dict of map dto instances
        if "mapId" in self._data[MapData]._dto:
            find = "mapId", self.id
        elif "mapName" in self._data[MapData]._dto:
            find = "mapName", self.name
        else:
            raise ValueError("unknown `id` and `name`")
        dto = find_matching_attribute(dto["data"].values(), *find)

        super().__load_hook__(load_group, dto)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ItemData].region)

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
