from typing import Union

from merakicommons.cache import lazy_property

from ... import configuration
from ...data import Region, Platform
from ..common import DataObjectList, CassiopeiaList
from ...dto.staticdata.language import LanguagesDto


class LanguagesData(DataObjectList):
    _dto_type = LanguagesDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Locales(CassiopeiaList):
    _data_types = {LanguagesData}

    def __init__(self, *args, region: Union[Region, str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LanguagesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
