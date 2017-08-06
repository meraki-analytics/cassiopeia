from typing import Union

from merakicommons.container import SearchableList
from merakicommons.cache import lazy_property

from ...configuration import settings
from ...data import Region, Platform
from ...dto.staticdata.version import VersionListDto
from ..common import CoreData, DataObjectList, CassiopeiaGhostList


class VersionListData(DataObjectList):
    _dto_type = VersionListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Versions(CassiopeiaGhostList):
    _data_types = {VersionListData}

    def __init__(self, *args, region: Union[Region, str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(*args, **kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        self.clear()
        SearchableList.__init__(self, [v for v in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[VersionListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
