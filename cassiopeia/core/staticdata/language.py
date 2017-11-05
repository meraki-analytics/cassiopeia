from typing import Union

from merakicommons.cache import lazy_property

from ...data import Region, Platform
from ..common import DataObjectList, CassiopeiaList, provide_default_region
from ...dto.staticdata.language import LanguagesDto


class LanguagesData(DataObjectList):
    _dto_type = LanguagesDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Locales(CassiopeiaList):
    _data_types = {LanguagesData}

    @provide_default_region
    def __init__(self, *args, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LanguagesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
