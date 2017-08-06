from typing import Dict, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ...configuration import settings
from ...data import Region, Platform
from ..common import CoreData, CassiopeiaGhost, get_latest_version
from ...dto.staticdata import realm as dto


##############
# Data Types #
##############


class LanguageStringsData(CoreData):
    _dto_type = dto.RealmDto
    _renamed = {"strings": "data"}

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

    def __init__(self, *, strings: Dict[str, str] = None, region: Union[Region, str] = None, version: str = None, locale: str = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        if locale is None:
            locale = region.default_locale
        kwargs = {"region": region, "locale": locale}
        if version is not None:
            kwargs["version"] = version
        if strings is not None:
            kwargs["strings"] = strings
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "version": self.version, "locale": self.locale}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LanguageStringsData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @property
    def version(self) -> str:
        try:
            return self._data[LanguageStringsData].version
        except KeyError:
            version = get_latest_version(region=self.region, endpoint="language")
            self(version=version)
            return self._data[LanguageStringsData].version

    @lazy_property
    def locale(self) -> str:
        return self._data[LanguageStringsData].locale

    @CassiopeiaGhost.property(LanguageStringsData)
    @ghost_load_on(KeyError)
    def type(self) -> str:
        return self._data[LanguageStringsData].type

    @CassiopeiaGhost.property(LanguageStringsData)
    @ghost_load_on(KeyError)
    def strings(self) -> Dict[str, str]:
        return self._data[LanguageStringsData].strings
