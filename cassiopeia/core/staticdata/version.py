from typing import Union

from merakicommons.cache import lazy_property

from ... import configuration
from ...data import Region, Platform
from ...dto.staticdata.version import VersionListDto
from ..common import DataObjectList, CassiopeiaList


class VersionListData(DataObjectList):
    _dto_type = VersionListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Versions(CassiopeiaList):
    _data_types = {VersionListData}

    def __init__(self, *args, region: Union[Region, str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[VersionListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
