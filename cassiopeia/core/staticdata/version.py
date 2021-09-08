from typing import Union

from merakicommons.cache import lazy_property

from ...data import Region, Platform
from ...dto.staticdata.version import VersionListDto
from ..common import CoreDataList, CassiopeiaObject, CassiopeiaLazyList


class VersionListData(CoreDataList):
    _dto_type = VersionListDto
    _renamed = {}


class Versions(CassiopeiaLazyList):
    _data_types = {VersionListData}

    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        CassiopeiaObject.__init__(self, **kwargs)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[VersionListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
