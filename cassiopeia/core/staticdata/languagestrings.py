from typing import Dict

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ...configuration import settings
from ...data import Region, Platform
from ..common import DataObject, CassiopeiaGhost, get_latest_version
from ...dto.staticdata import realm as dto


##############
# Data Types #
##############


class LanguageStringsData(DataObject):
    _dto_type = dto.RealmDto
    _renamed = {"strings": "data"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def type(self) -> str:
        return self._dto["type"]

    @property
    def strings(self) -> Dict[str, str]:
        return self._dto["data"]


##############
# Core Types #
##############


@searchable({})
class LanguageStrings(CassiopeiaGhost):
    _data_types = {LanguageStringsData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this realm."""
        return Region(self._data[LanguageStringsData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this realm."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this map."""
        try:
            return self._data[LanguageStringsData].version
        except AttributeError:
            version = get_latest_version(region=self.region)
            self(version=version)
            return self._data[LanguageStringsData].version

    @CassiopeiaGhost.property(LanguageStringsData)
    @ghost_load_on(KeyError)
    def type(self) -> str:
        return self._data[LanguageStringsData].type

    @CassiopeiaGhost.property(LanguageStringsData)
    @ghost_load_on(KeyError)
    def strings(self) -> Dict[str, str]:
        return self._data[LanguageStringsData].strings
