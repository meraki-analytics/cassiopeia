from typing import List, Mapping
from collections import Counter

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ..data import Region, Platform
from .common import DataObject, CassiopeiaGhost
from ..dto.runepage import RuneSlotDto, RunePageDto
from .staticdata.rune import Rune as StaticdataRune


##############
# Data Types #
##############


class RuneSlotData(DataObject):
    """This object contains rune slot information."""
    _dto_type = RuneSlotDto
    _renamed = {"id": "runeId", "slot": "runeSlotId"}

    @property
    def id(self) -> int:
        """Rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API."""
        return self._dto["runeId"]

    @property
    def slot(self) -> int:
        """Rune slot ID."""
        return self._dto["runeSlotId"]


class RunePageData(DataObject):
    """This object contains rune page information."""
    _dto_type = RunePageDto
    _renamed = {"runes": "slots", "summoner_id": "summonerId"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def summoner_id(self) -> int:
        return self._dto["summonerId"]

    @property
    def current(self) -> bool:
        """Indicates if the rune page is the current rune page."""
        return self._dto["current"]

    @property
    def runes(self) -> List[RuneSlotData]:
        """Collection of rune slots associated with the rune page."""
        return [RuneSlotData(slot) for slot in self._dto["slots"]]

    @property
    def name(self) -> str:
        """Rune page name."""
        return self._dto["name"]

    @property
    def id(self) -> int:
        """Rune page ID."""
        return self._dto["id"]


class RunePagesData(list):
    pass


##############
# Core Types #
##############


class RunePages(SearchableList):  # TODO This needs a summoner id or something so that it can be loaded.
    pass


@searchable({str: ["name", "runes", "region", "platform", "locale"], int: ["id"], bool: ["current"], StaticdataRune: ["runes"], Region: ["region"], Platform: ["platform"]})
class RunePage(CassiopeiaGhost):
    _data_types = {RunePageData}
    _load_types = {RunePageData: RunePages}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[RunePageData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this rune page."""
        return self.region.platform

    @property
    def locale(self) -> str:
        """The locale for this rune page."""
        return self._data[RunePageData].locale

    @lazy_property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner
        return Summoner(id=self._data[RunePageData].summoner_id)

    @CassiopeiaGhost.property(RunePageData)
    @ghost_load_on(KeyError)
    def current(self) -> bool:
        return self._data[RunePageData].current

    @CassiopeiaGhost.property(RunePageData)
    @ghost_load_on(KeyError)
    @lazy
    def runes(self) -> Mapping[StaticdataRune, int]:
        counter = Counter(slot.id for slot in self._data[RunePageData].runes)
        return SearchableDictionary({StaticdataRune(id=id, region=self.region.value): count for id, count in counter.items()})

    @CassiopeiaGhost.property(RunePageData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[RunePageData].name

    @CassiopeiaGhost.property(RunePageData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        return self._data[RunePageData].id
