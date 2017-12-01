from typing import Union, Optional
import datetime
from functools import total_ordering
from collections import defaultdict

from .. import configuration
from ..dto.patch import PatchListDto

try:
    import ujson as json
except ImportError:
    import json

from ..data import Region


@total_ordering
class Patch(object):
    __patches = None

    def __init__(self, region: Union[str, Region], season: str, name: str, start: Union[datetime.datetime, float], end: Optional[Union[datetime.datetime, float]]):
        if not isinstance(start, datetime.datetime):
            start = datetime.datetime.utcfromtimestamp(start)
        if end is not None and not isinstance(end, datetime.datetime):
            end = datetime.datetime.utcfromtimestamp(end)
        if not isinstance(region, Region):
            region = Region(region)
        self._region = region
        self._season = season
        self._name = name
        self._start = start
        self._end = end

    def __str__(self):
        return self._name

    @classmethod
    def from_str(cls, string: str, region: Union[Region, str] = None) -> "Patch":
        if not cls.__patches:
            cls.__load__()
        if region is None:
            region = configuration.settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        for patch in cls.__patches[region]:
            if string in patch.name:
                return patch
        else:
            raise ValueError("Unknown patch name {}".format(string))

    @classmethod
    def from_date(cls, date: Union[datetime.datetime], region: Union[Region, str] = None) -> "Patch":
        if not cls.__patches:
            cls.__load__()
        if region is None:
            region = configuration.settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        for patch in cls.__patches[region]:
            patch_end = patch.end or datetime.datetime.today() + datetime.timedelta(seconds=1)
            if patch.start <= date < patch_end:
                return patch
        else:
            raise ValueError("Unknown patch date {}".format(date))

    @classmethod
    def __load__(cls):
        patches = configuration.settings.pipeline.get(PatchListDto, query={})["patches"]
        cls.__patches = defaultdict(lambda: [None for _ in range(len(patches))])
        for i, patch in enumerate(patches):
            for region in Region:
                start = patch["start"].get(region, patch["start"]["NA"])
                start = datetime.datetime.utcfromtimestamp(start)
                end = patch["end"].get(region, patch["end"]["NA"])
                if end is not None:
                    end = datetime.datetime.utcfromtimestamp(end)
                cls.__patches[region][i] = Patch(region=region, season=patch["season"], name=patch["name"], start=start, end=end)

    @property
    def region(self):
        return self._region

    @property
    def season(self):
        return self._season

    @property
    def name(self):
        return self._name

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def major(self):
        return self.name.split(".")[0]

    @property
    def minor(self):
        return self.name.split(".")[1]

    @property
    def majorminor(self):
        return ".".join(self.name.split(".")[:2])

    @property
    def revision(self):
        return ".".join(self.name.split(".")[2:])

    def __eq__(self, other: "Patch"):
        return self.name == other.name

    def __lt__(self, other: "Patch"):
        if self.major < other.major or (self.major == other.major and self.minor < other.minor):
            return True
        else:
            return False
