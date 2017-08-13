from .common import CoreData, DataObjectList
from ..dto import championgg as dto


class GGChampionListData(DataObjectList):
    _dto_type = dto.GGChampionListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class GGChampionData(CoreData):
    _dto_type = dto.GGChampionDto
    _renamed = {"win_rate": "winRate", "id": "championId", "play_rate": "playRate"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def id(self) -> str:
        return self._dto["championId"]

    @property
    def win_rate(self) -> str:
        return self._dto["winRate"]

    @property
    def play_rate(self) -> str:
        return self._dto["playRate"]


# No non-CoreData core type is needed
