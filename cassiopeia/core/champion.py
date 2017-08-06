from .common import CoreData
from ..dto import champion as dto


class ChampionListData(list):
    _dto_type = dto.ChampionListDto


class ChampionData(CoreData):
    _dto_type = dto.ChampionDto
    _renamed = {"ranked_enabled": "rankedPlayEnabled", "custom_enabled": "botEnabled", "coop_ai_enabled": "botMmEnabled",
                "enabled": "active", "free_to_play": "freeToPlay", "champ_data": "champData"}

    @property
    def enabled(self) -> bool:
        return self._dto["active"]

    @property
    def custom_enabled(self) -> bool:
        return self._dto["botEnabled"]

    @property
    def coop_ai_enabled(self) -> bool:
        return self._dto["botMmEnabled"]

    @property
    def free_to_play(self) -> bool:
        return self._dto["freeToPlay"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def ranked_enabled(self) -> bool:
        return self._dto["rankedPlayEnabled"]

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def platform(self) -> str:
        return self._dto["platform"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]

    @property
    def champ_data(self) -> set:
        return self._dto["champData"]


# No non-CoreData core type is needed
