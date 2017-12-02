from typing import Union

from merakicommons.cache import lazy_property

from ...data import Region, Platform
from ..common import CassiopeiaObject, CoreDataList, CassiopeiaLazyList, provide_default_region
from ...dto.staticdata.language import LanguagesDto


class LanguagesData(CoreDataList):
    _dto_type = LanguagesDto
    _renamed = {}


class Locales(CassiopeiaLazyList):
    _data_types = {LanguagesData}

    @provide_default_region
    def __init__(self, *, region: Union[Region, str] = None):
        CassiopeiaObject.__init__(self, region=region)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LanguagesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
