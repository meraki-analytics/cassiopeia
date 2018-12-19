import arrow
import datetime
from typing import Union

from datapipelines import NotFoundError
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform, Rank
from .common import CoreData, CassiopeiaObject, CassiopeiaGhost, provide_default_region, ghost_load_on
from .staticdata import ProfileIcon
from ..dto.summoner import SummonerDto


##############
# Data Types #
##############


class AccountData(CoreData):
    _renamed = {"accountId": "id"}


class SummonerData(CoreData):
    _dto_type = SummonerDto
    _renamed = {"summonerLevel": "level"}

    def __call__(self, **kwargs):
        if "accountId" in kwargs and "puuid" in kwargs:
            self.account = AccountData(id=kwargs.pop("accountId"), puuid=kwargs.pop("puuid"))
        elif "accountId" in kwargs:
            self.account = AccountData(id=kwargs.pop("accountId"))
        elif "puuid" in kwargs:
            self.account = AccountData(puuid=kwargs.pop("puuid"))
        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


@searchable({str: ["id"]})
class Account(CassiopeiaObject):
    _data_types = {AccountData}

    @lazy_property
    def id(self) -> str:
        return self._data[AccountData].id

    @lazy_property
    def puuid(self) -> str:
        return self._data[AccountData].puuid


@searchable({str: ["name", "region", "platform"], str: ["id", "account", "puuid"], Region: ["region"], Platform: ["platform"]})
class Summoner(CassiopeiaGhost):
    _data_types = {SummonerData}

    @provide_default_region
    def __init__(self, *, id: str = None, account: Union[Account, str] = None, name: str = None, region: Union[Region, str] = None, puuid: str = None):
        kwargs = {"region": region}
        if id is not None:
            kwargs["id"] = id
        if name is not None:
            kwargs["name"] = name
        if account and isinstance(account, Account):
            self.__class__.account.fget._lazy_set(self, account)
            kwargs["accountId"] = account.id
            kwargs["puuid"] = account.puuid
        else:
            if account is not None:
                kwargs["accountId"] = account
            if puuid is not None:
                kwargs["puuid"] = puuid     
        super().__init__(**kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, id: str = None, account: Union[Account, str] = None, name: str = None, region: Union[Region, str], puuid: str=None) -> dict:
        query = {"region": region}
        if id is not None:
            query["id"] = id
        if name is not None:
            query["name"] = name
        if account and isinstance(account, Account):
            query["account.id"] = account.id
            if "puuid" in account:
                query["account.puuid"] = account.puuid
        else:
            if account is not None:
                query["account.id"] = account
            if puuid is not None:
                query["account.puuid"] = puuid
        return query

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform}
        try:
            query["account.puuid"] = self._data[SummonerData].account.puuid
        except AttributeError:
            pass
        try:
            query["id"] = self._data[SummonerData].id
        except AttributeError:
            pass
        try:
            query["account.id"] = self._data[SummonerData].account.id
        except AttributeError:
            pass
        try:
            query["name"] = self._data[SummonerData].name
        except AttributeError:
            pass
        assert "id" in query or "name" in query or "account.id" in query or "account.puuid" in query
        return query

    def __eq__(self, other: "Summoner"):
        if not isinstance(other, Summoner) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[SummonerData], "id"): s["id"] = self.id
        if hasattr(other._data[SummonerData], "id"): o["id"] = other.id
        if hasattr(self._data[SummonerData], "name"): s["name"] = self.sanitized_name
        if hasattr(other._data[SummonerData], "name"): o["name"] = other.sanitized_name
        if hasattr(self._data[SummonerData], "account"): s["account.id"] = self.account.id
        if hasattr(other._data[SummonerData], "account"): o["account.id"] = other.account.id
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        id_ = "?"
        name = "?"
        if hasattr(self._data[SummonerData], "id"):
            id_ = self.id
        if hasattr(self._data[SummonerData], "name"):
            name = self.name
        try:
            account = self._data[SummonerData].account.id
        except AttributeError:
            account = "?"
        try:
            puuid = self._data[SummonerData].account.puuid
        except AttributeError:
            puuid = "?"
        return "Summoner(id={id_}, account={account}, name='{name}', puuid='{puuid}')".format(id_=id_, name=name, account=account, puuid=puuid)

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
        return Region(self._data[SummonerData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this summoner."""
        return self.region.platform

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    @lazy
    def account(self) -> Account:
        return Account.from_data(self._data[SummonerData].account)

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[SummonerData].id

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[SummonerData].name

    @property
    def sanitized_name(self) -> str:
        return self.name.replace(" ", "").lower()

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def level(self) -> str:
        return self._data[SummonerData].level

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(id=self._data[SummonerData].profileIconId, region=self.region)

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def revision_date(self) -> datetime.datetime:
        return arrow.get(self._data[SummonerData].revisionDate / 1000)

    @property
    def match_history_uri(self) -> str:
        return "/v1/stats/player_history/{platform}/{id}".format(platform=self.platform.value, id=self.account.id)

    # Special core methods

    @property
    def champion_masteries(self) -> "ChampionMasteries":
        from .championmastery import ChampionMasteries
        return ChampionMasteries(summoner=self, region=self.region)

    @property
    def match_history(self) -> "MatchHistory":
        from .match import MatchHistory
        return MatchHistory(summoner=self)

    @property
    def current_match(self) -> "CurrentMatch":
        from .spectator import CurrentMatch
        return CurrentMatch(summoner=self, region=self.region)

    @property
    def leagues(self) -> "SummonerLeagues":
        from .league import League, SummonerLeagues
        positions = self.league_positions
        ids = {position.league_id for position in positions}
        return SummonerLeagues([League(id=id_, region=self.region) for id_ in ids])

    @property
    def league_positions(self) -> "LeagueEntries":
        from .league import LeagueEntries
        return LeagueEntries(summoner=self, region=self.region)

    @lazy_property
    def rank_last_season(self):
        most_recent_match = self.match_history[0]
        return most_recent_match.participants[self.name].rank_last_season

    @property
    def verification_string(self) -> str:
        from .thirdpartycode import VerificationString
        vs = VerificationString(summoner=self, region=self.region)
        return vs.string

    @lazy_property
    def ranks(self):
        ranks = {}
        for position in self.league_positions:
            ranks[position.queue] = Rank(tier=position.tier, division=position.division)
        return ranks
