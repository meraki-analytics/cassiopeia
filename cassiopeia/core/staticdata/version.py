from merakicommons.container import SearchableList
from merakicommons.cache import lazy_property

from ...data import Region, Platform
from ...dto.staticdata.version import VersionListDto
from ..common import DataObject, DataObjectList, CassiopeiaGhostList


class VersionListData(DataObjectList):
    _dto_type = VersionListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Versions(CassiopeiaGhostList):
    _data_types = {VersionListData}

    def __get_query__(self):
        return {"platform": self.platform}

    def __load_hook__(self, load_group, data: DataObject):
        self.clear()
        SearchableList.__init__(self, [v for v in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[VersionListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
