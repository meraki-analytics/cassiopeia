from typing import Union

from merakicommons.cache import lazy_property
from merakicommons.container import SearchableList

from ...configuration import settings
from ...data import Region, Platform
from ..common import DataObject, DataObjectList, CassiopeiaGhostList
from ...dto.staticdata.language import LanguagesDto


class LanguagesData(DataObjectList):
    _dto_type = LanguagesDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class Languages(CassiopeiaGhostList):
    _data_types = {LanguagesData}

    def __init__(self, *args, region: Union[Region, str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(*args, **kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    def __load_hook__(self, load_group: DataObject, data: DataObject) -> None:
        self.clear()
        from ...transformers.staticdata import StaticDataTransformer
        SearchableList.__init__(self, data)
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[LanguagesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform
