import os
from PIL.Image import Image as PILImage
from typing import Union

from merakicommons.cache import lazy_property, lazy
from merakicommons.container import searchable

from ... import configuration
from ...data import Region, Platform
from ...dto.staticdata.profileicon import ProfileIconDetailsDto, ProfileIconDataDto
from ..common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, get_latest_version, provide_default_region, ghost_load_on


try:
    import ujson as json
except ImportError:
    import json

_profile_icon_names = None


##############
# Data Types #
##############


class ProfileIconListData(CoreDataList):
    _dto_type = ProfileIconDataDto
    _renamed = {"included_data": "includedData"}


class ProfileIconData(CoreData):
    _dto_type = ProfileIconDetailsDto
    _renamed = {"included_data": "includedData"}


##############
# Core Types #
##############


class ProfileIcons(CassiopeiaLazyList):
    _data_types = {ProfileIconListData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None, version: str = None, locale: str = None):
        kwargs = {"region": region}
        if version is not None:
            kwargs["version"] = version
        if locale is not None:
            kwargs["locale"] = locale
        CassiopeiaObject.__init__(self, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ProfileIconListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[ProfileIconListData].version
        except AttributeError:
            version = get_latest_version(region=self.region, endpoint="profileicon")
            self(version=version)
            return self._data[ProfileIconListData].version

    @property
    def locale(self) -> str:
        return self._data[ProfileIconListData].locale


@searchable({int: ["id"], str: ["name", "url"], PILImage: ["image"]})
class ProfileIcon(CassiopeiaGhost):
    _data_types = {ProfileIconData}
    _load_types = {ProfileIconData: ProfileIconListData}
    _load_type = ProfileIcons

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
        except AttributeError:
            pass
        return query

    def __eq__(self, other: "ProfileIcon"):
        if not isinstance(other, ProfileIcon) or self.region != other.region:
            return False
        return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = "?"
        if hasattr(self._data[ProfileIconData], "id"):
            id_ = self.id
        return "ProfileIcon(id={id_}, region='{region}')".format(id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

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
        except AttributeError:
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
            with open(filename) as f:
                _profile_icon_names = json.load(f)
            _profile_icon_names = {int(key): value for key, value in _profile_icon_names.items()}
        try:
            return _profile_icon_names[self._data[ProfileIconData].id] or None
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
