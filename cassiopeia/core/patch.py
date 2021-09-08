from typing import Union, Optional
from functools import total_ordering
from collections import defaultdict
import arrow
from itertools import tee

from .. import configuration
from ..dto.patch import PatchListDto

try:
    import ujson as json
except ImportError:
    import json

from ..data import Region, Season


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


@total_ordering
class Patch(object):
    __patches = None

    def __init__(self, region: Union[str, Region], season: Season, name: str, start: Union[arrow.Arrow, float], end: Optional[Union[arrow.Arrow, float]]):
        if not isinstance(start, arrow.Arrow):
            start = arrow.get(start)
        if end is not None and not isinstance(end, arrow.Arrow):
            end = arrow.get(end)
        if not isinstance(region, Region):
            region = Region(region)
        self._region = region
        self._season = season
        self._name = name
        self._start = start
        self._end = end

    def __str__(self) -> str:
        return self._name

    @classmethod
    def from_str(cls, string: str, region: Union[Region, str]) -> "Patch":
        if not cls.__patches:
            cls.__load__()
        if not isinstance(region, Region):
            region = Region(region)
        for patch in cls.__patches[region]:
            if string in patch.name:
                return patch
        else:
            raise ValueError("Unknown patch name {}".format(string))

    @classmethod
    def from_date(cls, date: Union[arrow.Arrow], region: Union[Region, str]) -> "Patch":
        if not cls.__patches:
            cls.__load__()
        if not isinstance(region, Region):
            region = Region(region)
        for patch in cls.__patches[region]:
            patch_end = patch.end or arrow.now().shift(seconds=1)
            if patch.start <= date < patch_end:
                return patch
        else:
            raise ValueError("Unknown patch date {}".format(date))

    @classmethod
    def latest(cls, region: Union[Region, str] = None) -> "Patch":
        if isinstance(region, str):
            region = Region(region)
        if cls.__patches is None:
            cls.__load__()
        return cls.__patches[region][-1]

    @classmethod
    def __load__(cls):
        data = configuration.settings.pipeline.get(PatchListDto, query={})
        patches = data["patches"]
        shifts = data["shifts"]
        cls.__patches = defaultdict(lambda: [None for _ in range(len(patches))])
        for i, (patch, next_patch) in enumerate(pairwise(patches)):
            for region in Region:
                start = arrow.get(patch["start"] + shifts[region.platform.value]).to(region.timezone)
                season = Season.from_id(patch["season"])
                name = patch["name"]
                end = arrow.get(next_patch["start"] + shifts[region.platform.value]).to(region.timezone)
                cls.__patches[region][i] = Patch(region=region, season=season, name=name, start=start, end=end)

        # Since pairwise skips the last patch in the list, add it manually here
        patch = patches[-1]
        for region in Region:
            start = arrow.get(patch["start"] + shifts[region.platform.value]).to(region.timezone)
            season = Season.from_id(patch["season"])
            name = patch["name"]
            end = None
            cls.__patches[region][-1] = Patch(region=region, season=season, name=name, start=start, end=end)

        # Sort each region's patches by start date
        for region in Region:
            cls.__patches[region].sort(key=lambda patch: patch.start)

    @property
    def region(self) -> Region:
        return self._region

    @property
    def season(self) -> Season:
        return self._season

    @property
    def name(self) -> str:
        return self._name

    @property
    def start(self) -> arrow.Arrow:
        return self._start

    @property
    def end(self) -> arrow.Arrow:
        return self._end

    @property
    def major(self) -> str:
        return self.name.split(".")[0]

    @property
    def minor(self) -> str:
        return self.name.split(".")[1]

    @property
    def majorminor(self) -> str:
        return ".".join(self.name.split(".")[:2])

    @property
    def revision(self) -> str:
        return ".".join(self.name.split(".")[2:])

    def __eq__(self, other: "Patch") -> bool:
        return self.name == other.name

    def __lt__(self, other: "Patch") -> bool:
        if int(self.major) < int(other.major) or (self.major == other.major and int(self.minor) < int(other.minor)):
            return True
        else:
            return False
