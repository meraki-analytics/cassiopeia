import os
from PIL.Image import Image as PILImage
from typing import Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform
from ..common import DataObject, CassiopeiaGhost
from .version import VersionListData


try:
    import ujson as json
except ImportError:
    import json

_profile_icon_names = None


##############
# Data Types #
##############


class ProfileIconListData(list):
    pass


class ProfileIconData(DataObject):
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


class ProfileIcons(SearchableList):
    pass


@searchable({int: ["id"], str: ["name", "url"], PILImage: ["image"]})
class ProfileIcon(CassiopeiaGhost):
    _data_types = {ProfileIconData}
    _load_types = {ProfileIconData: ProfileIcons}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    def __load_hook__(self, load_group, core) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item
        core = find_matching_attribute(core, "id", self.id)
        super().__load_hook__(load_group, core)

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
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
            self(version=version)
            return self._data[ProfileIconData].version

    @property
    def locale(self) -> str:
        """The locale for this profile icon."""
        return self._data[ProfileIconData].locale

    @property
    def id(self) -> int:
        return self._data[ProfileIconData].id

    @property
    def name(self) -> Union[str, None]:
        global _profile_icon_names
        if _profile_icon_names is None:
            module_directory = os.path.dirname(os.path.realpath(__file__))
            module_directory, _ = os.path.split(module_directory)  # Go up one directory
            filename = os.path.join(module_directory, 'profile_icon_names.json')
            _profile_icon_names = json.load(open(filename))
            _profile_icon_names = {int(key): value for key, value in _profile_icon_names.items()}
        try:
            return _profile_icon_names[self._data[ProfileIconData].id]
        except KeyError:
            return None

    @CassiopeiaGhost.property(ProfileIconData)
    @ghost_load_on(KeyError)
    def url(self) -> str:
        versions = settings.pipeline.get(VersionListData, query={"platform": settings.default_platform})
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/profileicon/{id}.png".format(version=versions[0], id=self.id)

    @CassiopeiaGhost.property(ProfileIconData)
    @ghost_load_on(KeyError)
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})
