from .common import CoreData, CoreDataList
from ..dto import champion as dto


class ChampionStatusListData(CoreDataList):
    _dto_type = dto.ChampionListDto
    _renamed = {}


class ChampionStatusData(CoreData):
    _dto_type = dto.ChampionDto
    _renamed = {"rankedPlayEnabled": "rankedEnabled", "botEnabled": "customEnabled", "botMmEnabled": "coopAiEnabled", "active": "enabled", "freeToPlay": "freeToPlay"}


# No non-CoreData core type is needed
