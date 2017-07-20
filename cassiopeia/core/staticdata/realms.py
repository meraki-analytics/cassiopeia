from typing import Dict, List, Set, Union, Mapping, Any
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, Map
from ..common import DataObject, CassiopeiaObject, CassiopeiaGhost, Ghost
from .common import ImageData, SpriteData, Image, Sprite
from .version import VersionListData
from ...dto.staticdata import realms as dto


##############
# Data Types #
##############


class RealmData(DataObject):
    _dto_type = dto.RealmDto
    _renamed = {"legacy_mode": "lg", "latest_data_dragon": "dd", "language": "l", "latest_versions": "n", "max_profile_icon_id": "profileiconmax", "store": "store", "version": "v", "cdn": "cdn", "css_version": "css"}


    @property
    def legacy_mode(self) -> str:
        """Legacy script mode for IE6 or older."""
        return self._dto["lg"]

    @property
    def latest_data_dragon(self) -> str:
        """Latest changed version of Dragon Magic."""
        return self._dto["dd"]

    @property
    def language(self) -> str:
        """Default language for this realm."""
        return self._dto["l"]

    @property
    def latest_versions(self) -> Dict[str, str]:
        """Latest changed version for each data type listed."""
        return self._dto["n"]

    @property
    def max_profile_icon_id(self) -> int:
        """Special behavior number identifying the largest profile icon ID that can be used under 500. Any profile icon that is requested between this number and 500 should be mapped to 0."""
        return ImageData(self._dto["profileiconmax"])

    @property
    def store(self) -> str:
        """Additional API data drawn from other sources that may be related to Data Dragon functionality."""
        return self._dto["store"]

    @property
    def version(self) -> str:
        """Current version of this file for this realm."""
        return self._dto["v"]

    @property
    def cdn(self) -> str:
        """The base CDN URL."""
        return self._dto["cdn"]

    @property
    def css_version(self) -> str:
        """Latest changed version of Dragon Magics CSS file."""
        return self._dto["css"]


##############
# Core Types #
##############


@searchable({})
class Realm(CassiopeiaGhost):
    _data_types = {RealmData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this realm."""
        return Region(self._data[RealmData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this realm."""
        return self.region.platform

    @lazy_property
    def locale(self) -> Platform:
        """The locale for this realm."""
        return self._data[RealmData].locale

    @property
    def version(self) -> str:
        """The version for this map."""
        try:
            return self._data[RealmData].version
        except AttributeError:
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
            self(version=version)
            return self._data[RealmData].version

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def legacy_mode(self) -> str:
        return self._data[RealmData].legacy_mode

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def latest_data_dragon(self) -> str:
        return self._data[RealmData].latest_data_dragon

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def language(self) -> str:
        return self._data[RealmData].language

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def max_profile_icon_id(self) -> Image:
        return self._data[RealmData].max_profile_icon_id

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def store(self) -> str:
        return self._data[RealmData].store

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def cdn(self) -> str:
        return self._data[RealmData].cdn

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on(KeyError)
    def css_version(self) -> str:
        return self._data[RealmData].css_version
