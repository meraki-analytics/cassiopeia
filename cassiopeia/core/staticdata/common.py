from PIL.Image import Image as PILImage

from merakicommons.container import searchable
from merakicommons.cache import lazy_property
from PIL.Image import Image as PILImage

from ...configuration import settings
from ..common import CoreData, CassiopeiaObject


class SpriteData(CoreData):
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


class ImageData(CoreData):
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


@searchable({str: ["sprite", "url"]})
class Sprite(CassiopeiaObject):
    _data_types = {SpriteData}

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
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/sprite/{sprite}".format(version=self.version, sprite=self.sprite)

    @lazy_property
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})


@searchable({str: ["full", "url"]})
class Image(CassiopeiaObject):
    _data_types = {ImageData}

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
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/{group}/{full}".format(version=self.version, group=self.group, full=self.full)

    @lazy_property
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})

    @lazy_property
    def sprite_info(self) -> Sprite:
        sprite = Sprite(w=self._data[ImageData].width,
                        h=self._data[ImageData].height,
                        x=self._data[ImageData].x,
                        y=self._data[ImageData].y,
                        sprite=self._data[ImageData].sprite,
                        version=self._data[ImageData].version)
        return sprite
