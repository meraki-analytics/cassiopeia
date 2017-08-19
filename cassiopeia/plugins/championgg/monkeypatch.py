from merakicommons.cache import lazy_property

from ...data import Patch
from ...core.common import get_latest_version
from ...core.staticdata.champion import Champion
from .core import ChampionGGStats


def championgg(self) -> ChampionGGStats:
    """The champion.gg data for this champion."""
    latest_version = get_latest_version(self.region, endpoint="champion")
    if self.version != latest_version:
        raise ValueError("Can only get champion.gg data for champions on the most recent version.")
    return ChampionGGStats(id=self.id, patch=Patch.from_str(".".join(self.version.split(".")[:-1])))

championgg = lazy_property(championgg)

Champion.championgg = championgg
