from typing import Dict, Union

from merakicommons.cache import lazy_property
from merakicommons.container import searchable

from ...data import Region, Platform
from ..common import CoreData, CassiopeiaGhost, ghost_load_on
from ...dto.staticdata import realm as dto


##############
# Data Types #
##############


class RealmData(CoreData):
    _dto_type = dto.RealmDto
    _renamed = {"lg": "legacyMode", "dd": "latestDataDragon", "l": "language", "n": "latestVersions",
                "profileiconmax": "maxProfileIconId", "v": "version", "css": "cssVersion"}


##############
# Core Types #
##############


@searchable({})
class Realms(CassiopeiaGhost):
    _data_types = {RealmData}

    def __init__(self, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    @lazy_property
    def region(self) -> Region:
        """The region for this realm."""
        return Region(self._data[RealmData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this realm."""
        return self.region.platform

    @lazy_property
    def locale(self) -> Platform:
        """The locale for this realm."""
        return self._data[RealmData].locale

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def version(self) -> str:
        return self._data[RealmData].version

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def language(self) -> str:
        """Default language for this realm."""
        return self._data[RealmData].language

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def latest_versions(self) -> Dict[str, str]:
        """Latest changed version for each data type listed."""
        return self._data[RealmData].latestVersions

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def legacy_mode(self) -> str:
        return self._data[RealmData].legacyMode

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def latest_data_dragon(self) -> str:
        return self._data[RealmData].latestDataDragon

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def language(self) -> str:
        return self._data[RealmData].language

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def max_profile_icon_id(self) -> int:
        return self._data[RealmData].maxProfileIconId

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def store(self) -> str:
        return self._data[RealmData].store

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def cdn(self) -> str:
        return self._data[RealmData].cdn

    @CassiopeiaGhost.property(RealmData)
    @ghost_load_on
    def css_version(self) -> str:
        return self._data[RealmData].css_version
