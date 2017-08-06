from typing import List, Mapping, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableDictionary

from ..data import Region, Platform
from .common import CoreData, DataObjectList, CassiopeiaGhost, CassiopeiaGhostList
from .summoner import Summoner
from ..dto.masterypage import MasteryDto, MasteryPageDto, MasteryPagesDto
from .staticdata.mastery import Mastery as StaticdataMastery


##############
# Data Types #
##############


class MasteryPagesData(DataObjectList):
    _dto_type = MasteryPagesDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def summoner_id(self) -> str:
        return self._dto["summonerId"]


class MasteryData(CoreData):
    """This object contains mastery information."""
    _dto_type = MasteryDto
    _renamed = {"points": "rank"}

    @property
    def id(self) -> int:
        """Mastery ID. For static information correlating to masteries, please refer to the LoL Static Data API."""
        return self._dto["id"]

    @property
    def points(self) -> int:
        """Mastery rank (i.e., the number of points put into this mastery)."""
        return self._dto["rank"]


class MasteryPageData(CoreData):
    """This object contains mastery page information."""
    _dto_type = MasteryPageDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def current(self) -> bool:
        """Indicates if the mastery page is the current mastery page."""
        return self._dto["current"]

    @property
    def masteries(self) -> List[MasteryData]:
        """Collection of masteries associated with the mastery page."""
        return [MasteryData.from_dto(mastery) for mastery in self._dto["masteries"]]

    @property
    def name(self) -> str:
        """Mastery page name."""
        return self._dto["name"]

    @property
    def id(self) -> int:
        """Mastery page ID."""
        return self._dto["id"]


##############
# Core Types #
##############


class MasteryPages(CassiopeiaGhostList):
    _data_types = {MasteryPagesData}

    def __init__(self, *args, summoner: Union[Summoner, int, str], region: Union[Region, str] = None):
        super().__init__(*args, region=region)
        if isinstance(summoner, str):
            summoner = Summoner(name=summoner)
        elif isinstance(summoner, int):
            summoner = Summoner(id=summoner)
        self.__summoner = summoner

    def __get_query__(self):
        return {"summoner.id": self.__summoner.id, "region": self.region, "platform": self.platform}

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        self.clear()
        from ..transformers.masteries import MasteriesTransformer
        SearchableList.__init__(self, [MasteriesTransformer.mastery_page_data_to_core(None, i) for i in data])
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MasteryPagesData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform


@searchable({str: ["name", "masteries", "region", "platform", "locale"], int: ["id"], bool: ["current"], StaticdataMastery: ["masteries"], Region: ["region"], Platform: ["platform"]})
class MasteryPage(CassiopeiaGhost):
    _data_types = {MasteryPageData}
    _load_types = {MasteryPageData: MasteryPages}

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MasteryPageData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this mastery page."""
        return self.region.platform

    @property
    def locale(self) -> str:
        """The locale for this mastery page."""
        return self._data[MasteryPageData].locale

    @lazy_property
    def summoner(self) -> Summoner:
        return Summoner(id=self._data[MasteryPageData].summoner_id)

    @CassiopeiaGhost.property(MasteryPageData)
    @ghost_load_on(KeyError)
    def current(self) -> bool:
        return self._data[MasteryPageData].current

    @CassiopeiaGhost.property(MasteryPageData)
    @ghost_load_on(KeyError)
    @lazy
    def masteries(self) -> Mapping[StaticdataMastery, int]:
        return SearchableDictionary({StaticdataMastery(id=mastery.id, region=self.region.value): mastery.points for mastery in self._data[MasteryPageData].masteries})

    @CassiopeiaGhost.property(MasteryPageData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[MasteryPageData].name

    @CassiopeiaGhost.property(MasteryPageData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        return self._data[MasteryPageData].id
