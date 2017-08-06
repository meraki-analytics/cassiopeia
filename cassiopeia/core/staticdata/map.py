from typing import List, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform
from ..common import CoreData, CassiopeiaGhost, DataObjectList, CassiopeiaGhostList, get_latest_version
from .common import ImageData, Sprite, Image
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


class MapData(CoreData):
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

    def __init__(self, *args, region: Union[Region, str] = None, version: str = None, locale: str = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        if locale is None:
            locale = region.default_locale
        kwargs = {"region": region, "locale": locale}
        if version is not None:
            kwargs["version"] = version
        super().__init__(*args, **kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
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
            version = get_latest_version(region=self.region, endpoint="map")
            self(version=version)
            return self._data[MapListData].version

    @property
    def locale(self) -> str:
        return self._data[MapListData].locale


@searchable({str: ["name", "locale"], int: ["id"]})
class Map(CassiopeiaGhost):
    _data_types = {MapData}
    _load_types = {MapData: MapListData}

    def __init__(self, *, id: int = None, name: str = None, region: Union[Region, str] = None, version: str = None, locale: str = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        if locale is None:
            locale = region.default_locale
        kwargs = {"region": region, "locale": locale}
        if version is not None:
            kwargs["version"] = version
        if id is not None:
            kwargs["id"] = id
        if name is not None:
            kwargs["name"] = name
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale}

    def __load_hook__(self, load_group, data) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item
            else:
                raise ValueError("could not find matching {}={} in {}".format(attrname, attrvalue, datalist))

        # The `data` is a dict of map data instances
        if "mapId" in self._data[MapData]._dto:
            find = "id", self.id
        elif "mapName" in self._data[MapData]._dto:
            find = "name", self.name
        else:
            raise ValueError("unknown `id` and `name`")
        data = find_matching_attribute(data, *find)
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MapData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this map."""
        try:
            return self._data[MapData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="map")
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
    def image(self) -> Image:
        image = Image.from_data(self._data[MapData].image)
        image(version=self.version)
        return image

    @lazy_property
    def sprite(self) -> Sprite:
        return self.image.sprite_info
