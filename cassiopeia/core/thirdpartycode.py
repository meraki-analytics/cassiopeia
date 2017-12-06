from typing import Union

from merakicommons.cache import lazy_property

from ..data import Region, Platform
from .common import CoreData, CassiopeiaGhost, provide_default_region, ghost_load_on
from .summoner import Summoner


##############
# Data Types #
##############


class VerificationStringData(CoreData):
    _renamed = {}


##############
# Core Types #
##############


class VerificationString(CassiopeiaGhost):
    _data_types = {VerificationStringData}

    @provide_default_region
    def __init__(self, summoner: Summoner, region: Union[Region, str]):
        self.__summoner = summoner
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "summoner.id": self.summoner.id}

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Summoner, region: Union[Region, str]) -> dict:
        return {"region": region, "summoner.id": summoner.id}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[VerificationStringData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(VerificationStringData)
    @ghost_load_on
    def string(self) -> str:
        return self._data[VerificationStringData].string

    @property
    def summoner(self):
        return self.__summoner