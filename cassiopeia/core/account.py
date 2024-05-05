from typing import Union

from datapipelines import NotFoundError
from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ..data import Region, Platform, Continent
from .common import CoreData, CassiopeiaGhost, ghost_load_on
from ..dto.account import AccountDto


##############
# Data Types #
##############


class AccountData(CoreData):
    _dto_type = AccountDto
    _renamed = {"gameName": "name", "tagLine": "tagline"}


##############
# Core Types #
##############


@searchable(
    {
        str: ["name", "tagline", "region", "platform", "continent", "puuid"],
        Region: ["region"],
        Platform: ["platform"],
        Continent: ["continent"],
    }
)
class Account(CassiopeiaGhost):
    _data_types = {AccountData}

    def __init__(
        self,
        *,
        puuid: str = None,
        name: str = None,
        tagline: str = None,
        region: Union[Region, str] = None,
    ):
        kwargs = {"region": region}

        if puuid is not None:
            kwargs["puuid"] = puuid
        if name is not None:
            kwargs["name"] = name
        if tagline is not None:
            kwargs["tagline"] = tagline
        super().__init__(**kwargs)

    @classmethod
    def __get_query_from_kwargs__(
        cls,
        *,
        puuid: str = None,
        name: str = None,
        tagline: str = None,
        region: Union[Region, str],
    ) -> dict:
        query = {"region": region}
        if puuid is not None:
            query["puuid"] = puuid
        if name is not None:
            query["name"] = name
        if tagline is not None:
            query["tagline"] = tagline
        return query

    def __get_query__(self):
        query = {"region": self.region, "platform": self.platform}
        try:
            query["puuid"] = self._data[AccountData].puuid
        except AttributeError:
            pass
        try:
            query["name"] = self._data[AccountData].name
        except AttributeError:
            pass
        try:
            query["tagline"] = self._data[AccountData].tagline
        except AttributeError:
            pass
        assert "puuid" in query or ("name" in query and "tagline" in query)
        return query

    def __eq__(self, other: "Account"):
        if not isinstance(other, Account) or self.region != other.region:
            return False
        s = {}
        o = {}
        if hasattr(self._data[AccountData], "puuid"):
            s["puuid"] = self.puuid
        if hasattr(other._data[AccountData], "puuid"):
            o["puuid"] = other.puuid
        if hasattr(self._data[AccountData], "name"):
            s["name"] = self.name
        if hasattr(other._data[AccountData], "name"):
            o["name"] = other.name
        if hasattr(self._data[AccountData], "tagline"):
            s["tagline"] = self.tagline
        if any(s.get(key, "s") == o.get(key, "o") for key in s):
            return True
        else:
            return self.id == other.id

    def __str__(self):
        puuid = "?"
        name = "?"
        tagline = "?"
        if hasattr(self._data[AccountData], "puuid"):
            puuid = self.puuid
        if hasattr(self._data[AccountData], "name"):
            name = self.name
        if hasattr(self._data[AccountData], "tagline"):
            tagline = self.tagline
        return f"Account(puuid={puuid}, name={name}, tagline='{tagline}')"

    @property
    def exists(self):
        try:
            if not self._Ghost__all_loaded:
                self.__load__()
            # Make sure we can access these attributes
            self.puuid
            self.name
            self.tagline
            return True
        except (AttributeError, NotFoundError):
            return False

    @lazy_property
    def region(self) -> Region:
        """The region for this summoner."""
        return Region(self._data[AccountData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this summoner."""
        return self.region.platform

    @lazy_property
    def continent(self) -> Platform:
        """The continent for this summoner."""
        return self.region.continent

    @CassiopeiaGhost.property(AccountData)
    @ghost_load_on
    def puuid(self) -> str:
        return self._data[AccountData].puuid

    @CassiopeiaGhost.property(AccountData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[AccountData].name

    @CassiopeiaGhost.property(AccountData)
    @ghost_load_on
    def tagline(self) -> str:
        return self._data[AccountData].tagline

    @property
    def name_with_tagline(self) -> str:
        return f"{self.name}#{self.tagline}"

    # Special core methods

    @property
    def summoner(self) -> "Summoner":
        from .summoner import Summoner

        return Summoner(puuid=self.puuid, region=self.region)


# Add circular references at the bottom
from .summoner import Summoner
