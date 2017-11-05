import os
from PIL.Image import Image as PILImage
from typing import Union

from merakicommons.cache import lazy_property, lazy
from merakicommons.container import searchable

from ... import configuration
from ...data import Region, Platform
from ...dto.staticdata.profileicon import ProfileIconDetailsDto, ProfileIconDataDto
from ..common import CoreData, DataObjectList, CassiopeiaGhost, CassiopeiaList, get_latest_version, provide_default_region, ghost_load_on


try:
    import ujson as json
except ImportError:
    import json

_profile_icon_names = None


##############
# Data Types #
##############


class ProfileIconListData(DataObjectList):
    _dto_type = ProfileIconDataDto
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


class ProfileIconData(CoreData):
    _dto_type = ProfileIconDetailsDto
    _renamed = {"id": "profileIconId"}

    @property
    def id(self) -> int:
        return self._dto["profileIconId"]

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]


##############
# Core Types #
##############


class ProfileIcons(CassiopeiaList):
    _data_types = {ProfileIconData}

    @provide_default_region
    def __init__(self, *args, region: Union[Region, str] = None, version: str = None, locale: str = None):
        kwargs = {"region": region}
        if version is not None:
            kwargs["version"] = version
        if locale is not None:
            kwargs["locale"] = locale
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ProfileIconData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[ProfileIconData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="profileicon")
            self(version=version)
            return self._data[ProfileIconData].version

    @property
    def locale(self) -> str:
        return self._data[ProfileIconData].locale


@searchable({int: ["id"], str: ["name", "url"], PILImage: ["image"]})
class ProfileIcon(CassiopeiaGhost):
    _data_types = {ProfileIconData}
    _load_types = {ProfileIconData: ProfileIconListData}

    @provide_default_region
    def __init__(self, *, id: int = None, region: Union[Region, str] = None, version: str = None, locale: str = None):
        kwargs = {"region": region}
        if id is not None:
            kwargs["id"] = id
        if version is not None:
            kwargs["version"] = version
        if locale is not None:
            kwargs["locale"] = locale
        super().__init__(**kwargs)

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform, "version": self.version}
        try:
            query["locale"] = self.locale
        except KeyError:
            pass
        return query

    def __load_hook__(self, load_group, data) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item
        data = find_matching_attribute(data, "id", self.id)
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        """The region for this profile icon."""
        return Region(self._data[ProfileIconData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this profile icon."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this profile icon."""
        try:
            return self._data[ProfileIconData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="profileicon")
            self(version=version)
            return self._data[ProfileIconData].version

    @property
    def locale(self) -> str:
        """The locale for this profile icon."""
        return self._data[ProfileIconData].locale

    @property
    def id(self) -> int:
        return self._data[ProfileIconData].id

    @lazy_property
    def name(self) -> Union[str, None]:
        global _profile_icon_names
        if _profile_icon_names is None:
            module_directory = os.path.dirname(os.path.realpath(__file__))
            module_directory, _ = os.path.split(module_directory)  # Go up one directory
            module_directory, _ = os.path.split(module_directory)  # Go up another directory
            filename = os.path.join(module_directory, "profile_icon_names.json")
            _profile_icon_names = json.load(open(filename))
            _profile_icon_names = {int(key): value for key, value in _profile_icon_names.items()}
        try:
            return _profile_icon_names[self._data[ProfileIconData].id]
        except KeyError:
            return None

    @CassiopeiaGhost.property(ProfileIconData)
    @ghost_load_on
    def url(self) -> str:
        version = get_latest_version(region=self.region, endpoint="profileicon")
        return "https://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{id}.png".format(version=version, id=self.id)

    @CassiopeiaGhost.property(ProfileIconData)
    @ghost_load_on
    @lazy
    def image(self) -> PILImage:
        return configuration.settings.pipeline.get(PILImage, query={"url": self.url})
