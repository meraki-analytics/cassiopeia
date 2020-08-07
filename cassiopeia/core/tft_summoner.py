import arrow
import datetime
from typing import Union

from datapipelines import NotFoundError
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform, Rank
from .common import CoreData, CassiopeiaObject, CassiopeiaGhost, provide_default_region, ghost_load_on
from .staticdata import ProfileIcon
from ..dto.tft_summoner import TFTSummonerDto


##############
# Data Types #
##############


class TFTSummonerData(CoreData):
    _dto_type = TFTSummonerDto
    _renamed = {"summonerLevel": "level"}


##############
# Core Types #
##############


@searchable({str: ["name", "region", "platform", "id", "account_id", "puuid"], Region: ["region"], Platform: ["platform"]})
class TFTSummoner(CassiopeiaGhost):
    _data_types = {TFTSummonerData}

    @provide_default_region
    def __init__(self, *, id: str = None, account_id: str = None, puuid: str = None, name: str = None, region: Union[Region, str] = None):
        kwargs = {"region": region}

        if id is not None:
            kwargs["id"] = id
        if account_id is not None:
            kwargs["accountId"] = account_id
        if puuid is not None:
            kwargs["puuid"] = puuid
        if name is not None:
            kwargs["name"] = name
        super().__init__(**kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, id: str = None, account_id: str=None, puuid: str=None, name: str = None, region: Union[Region, str]) -> dict:
        query = {"region": region}
        if id is not None:
            query["id"] = id
        if account_id is not None:
            query["accountId"] = account_id
        if puuid is not None:
            query["puuid"] = puuid
        if name is not None:
            query["name"] = name
        return query

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform}
        try:
            query["puuid"] = self._data[TFTSummonerData].puuid
        except AttributeError:
            pass
        try:
            query["id"] = self._data[TFTSummonerData].id
        except AttributeError:
            pass
        try:
            query["accountId"] = self._data[TFTSummonerData].accountId
        except AttributeError:
            pass
        try:
            query["name"] = self._data[TFTSummonerData].name
        except AttributeError:
            pass
        assert "id" in query or "name" in query or "accountId" in query or "puuid" in query
        return query

    def __eq__(self, other: "TFTSummoner"):
        if not isinstance(other, TFTSummoner) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[TFTSummonerData], "id"): s["id"] = self.id
        if hasattr(other._data[TFTSummonerData], "id"): o["id"] = other.id
        if hasattr(self._data[TFTSummonerData], "name"): s["name"] = self.sanitized_name
        if hasattr(other._data[TFTSummonerData], "name"): o["name"] = other.sanitized_name
        if hasattr(self._data[TFTSummonerData], "accountId"): s["accountId"] = self.account_id
        if hasattr(other._data[TFTSummonerData], "accountId"): o["accountId"] = other.account_id
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        id_ = "?"
        name = "?"
        if hasattr(self._data[TFTSummonerData], "id"):
            id_ = self.id
        if hasattr(self._data[TFTSummonerData], "name"):
            name = self.name
        try:
            account_id = self._data[TFTSummonerData].accountId
        except AttributeError:
            account_id = "?"
        try:
            puuid = self._data[TFTSummonerData].puuid
        except AttributeError:
            puuid = "?"
        return "TFTSummoner(id={id_}, account_id={account_id}, name='{name}', puuid='{puuid}')".format(id_=id_, name=name, account_id=account_id, puuid=puuid)

    @property
    def exists(self):
        try:
            if not self._Ghost__all_loaded:
                self.__load__()
            self.revision_date  # Make sure we can access this attribute
            return True
        except (AttributeError, NotFoundError):
            return False

    @lazy_property
    def region(self) -> Region:
        """The region for this summoner."""
        return Region(self._data[TFTSummonerData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this summoner."""
        return self.region.platform

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def account_id(self) -> str:
        return self._data[TFTSummonerData].accountId

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def puuid(self) -> str:
        return self._data[TFTSummonerData].puuid

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[TFTSummonerData].id

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[TFTSummonerData].name

    @property
    def sanitized_name(self) -> str:
        return self.name.replace(" ", "").lower()

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def level(self) -> str:
        return self._data[TFTSummonerData].level

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(id=self._data[TFTSummonerData].profileIconId, region=self.region)

    @CassiopeiaGhost.property(TFTSummonerData)
    @ghost_load_on
    def revision_date(self) -> datetime.datetime:
        return arrow.get(self._data[TFTSummonerData].revisionDate / 1000)
