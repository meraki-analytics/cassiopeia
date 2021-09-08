from typing import Union

from merakicommons.cache import lazy_property
from merakicommons.container import SearchableLazyList

from .common import CassiopeiaGhost, CoreData, ghost_load_on
from .staticdata.champion import Champion
from ..data import Region, Platform
from ..dto import champion as dto


class ChampionRotationData(CoreData):
    _dto_type = dto.ChampionRotationDto
    _renamed = {}


class ChampionRotation(CassiopeiaGhost):
    _data_types = {ChampionRotationData}

    def __init__(self, *, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ChampionRotationData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @CassiopeiaGhost.property(ChampionRotationData)
    @ghost_load_on
    def max_new_player_level(self) -> int:
        return self._data[ChampionRotationData].maxNewPlayerLevel

    @CassiopeiaGhost.property(ChampionRotationData)
    @ghost_load_on
    def free_champions(self) -> SearchableLazyList:
        gen = (Champion(region=self.region, id=id_) for id_ in self._data[ChampionRotationData].freeChampionIds)
        return SearchableLazyList(generator=gen)

    @CassiopeiaGhost.property(ChampionRotationData)
    @ghost_load_on
    def free_champions_for_new_players(self) -> SearchableLazyList:
        gen = (Champion(region=self.region, id=id_) for id_ in self._data[ChampionRotationData].freeChampionIdsForNewPlayers)
        return SearchableLazyList(generator=gen)
