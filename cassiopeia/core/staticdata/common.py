from merakicommons.cache import lazy_property

from ...configuration import settings
from ..common import DataObject, CassiopeiaObject
from ..datadragon import DataDragonImage


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
    def image(self) -> "PIL.Image":
        from PIL import Image
        image = settings.pipeline.get(DataDragonImage, query={"url": self.url})
        return Image.open(image)


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
