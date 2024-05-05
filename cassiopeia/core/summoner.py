import arrow
import datetime
from typing import Union

from datapipelines import NotFoundError
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform, Continent, Rank
from .common import CoreData, CassiopeiaGhost, ghost_load_on
from .staticdata import ProfileIcon
from ..dto.summoner import SummonerDto


##############
# Data Types #
##############


class SummonerData(CoreData):
    _dto_type = SummonerDto
    _renamed = {"summonerLevel": "level"}


##############
# Core Types #
##############


@searchable(
    {
        str: ["region", "platform", "id", "account_id", "puuid"],
        Region: ["region"],
        Platform: ["platform"],
    }
)
class Summoner(CassiopeiaGhost):
    _data_types = {SummonerData}

    def __init__(
        self,
        *,
        id: str = None,
        account_id: str = None,
        puuid: str = None,
        region: Union[Region, str] = None,
    ):
        kwargs = {"region": region}

        if id is not None:
            kwargs["id"] = id
        if account_id is not None:
            kwargs["accountId"] = account_id
        if puuid is not None:
            kwargs["puuid"] = puuid
        super().__init__(**kwargs)

    @classmethod
    def __get_query_from_kwargs__(
        cls,
        *,
        id: str = None,
        account_id: str = None,
        puuid: str = None,
        region: Union[Region, str],
    ) -> dict:
        query = {"region": region}
        if id is not None:
            query["id"] = id
        if account_id is not None:
            query["accountId"] = account_id
        if puuid is not None:
            query["puuid"] = puuid
        return query

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform}
        try:
            query["puuid"] = self._data[SummonerData].puuid
        except AttributeError:
            pass
        try:
            query["id"] = self._data[SummonerData].id
        except AttributeError:
            pass
        try:
            query["accountId"] = self._data[SummonerData].accountId
        except AttributeError:
            pass
        assert "id" in query or "accountId" in query or "puuid" in query
        return query

    def __eq__(self, other: "Summoner"):
        if not isinstance(other, Summoner) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[SummonerData], "id"):
            s["id"] = self.id
        if hasattr(other._data[SummonerData], "id"):
            o["id"] = other.id
        if hasattr(self._data[SummonerData], "accountId"):
            s["accountId"] = self.account_id
        if hasattr(other._data[SummonerData], "accountId"):
            o["accountId"] = other.account_id
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        id_ = "?"
        if hasattr(self._data[SummonerData], "id"):
            id_ = self.id
        try:
            account_id = self._data[SummonerData].accountId
        except AttributeError:
            account_id = "?"
        try:
            puuid = self._data[SummonerData].puuid
        except AttributeError:
            puuid = "?"
        return f"Summoner(id={id_}, account_id={account_id}, puuid='{puuid}')"

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

    @lazy_property
    def continent(self) -> Continent:
        """The continent for this summoner."""
        return self.region.continent

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def account_id(self) -> str:
        return self._data[SummonerData].accountId

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def puuid(self) -> str:
        return self._data[SummonerData].puuid

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def id(self) -> str:
        return self._data[SummonerData].id

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def level(self) -> str:
        return self._data[SummonerData].level

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def profile_icon(self) -> ProfileIcon:
        return ProfileIcon(
            id=self._data[SummonerData].profileIconId, region=self.region
        )

    @CassiopeiaGhost.property(SummonerData)
    @ghost_load_on
    def revision_date(self) -> datetime.datetime:
        return arrow.get(self._data[SummonerData].revisionDate / 1000)

    @property
    def match_history_uri(self) -> str:
        return self.match_history[0].participants[self].match_history_uri

    # Special core methods

    @property
    def champion_masteries(self) -> "ChampionMasteries":
        from .championmastery import ChampionMasteries

        return ChampionMasteries(summoner=self, region=self.region)

    @property
    def match_history(self) -> "MatchHistory":
        from .match import MatchHistory

        return MatchHistory(continent=self.region.continent, puuid=self.puuid)

    @property
    def current_match(self) -> "CurrentMatch":
        from .spectator import CurrentMatch

        return CurrentMatch(summoner=self, region=self.region)

    @property
    def league_entries(self) -> "LeagueSummonerEntries":
        from .league import LeagueSummonerEntries

        leagues = LeagueSummonerEntries(summoner=self)
        return leagues

    @property
    def verification_string(self) -> str:
        from .thirdpartycode import VerificationString

        vs = VerificationString(summoner=self, region=self.region)
        return vs.string

    @lazy_property
    def ranks(self):
        ranks = {}
        for position in self.league_entries:
            ranks[position.queue] = Rank(tier=position.tier, division=position.division)
        return ranks


# Add circular references at the bottom
from .championmastery import ChampionMasteries
from .match import MatchHistory
from .spectator import CurrentMatch
from .league import LeagueSummonerEntries
from .thirdpartycode import VerificationString
