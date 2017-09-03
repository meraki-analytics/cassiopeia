import os
import datetime

try:
    import ujson as json
except ImportError:
    import json

from typing import Optional as Optional, Union as Union


class Patch(object):
    def __init__(self, season: str, name: str, start: Union[datetime.datetime, float], end: Optional[Union[datetime.datetime, float]]):
        if not isinstance(start, datetime.datetime):
            start = datetime.datetime.fromtimestamp(start)
        if end is not None and not isinstance(end, datetime.datetime):
            end = datetime.datetime.fromtimestamp(end)
        self._season = season
        self._name = name
        self._start = start
        self._end = end

    def __str__(self):
        return self._name

    @classmethod
    def from_str(cls, string: str) -> "Patch":
        for patch in cls.__patches:
            if string in patch.name:
                return patch
        else:
            raise ValueError("Unknown patch name {}".format(string))

    @classmethod
    def from_date(cls, date: Union[datetime.datetime]) -> "Patch":
        for patch in cls.__patches:
            patch_end = patch.end or datetime.datetime.today() + datetime.timedelta(seconds=1)
            if patch.start <= date < patch_end:
                return patch
        else:
            raise ValueError("Unknown patch date {}".format(date))

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


direc, _ = os.path.split(__file__)
with open(os.path.join(direc, "patches.json")) as f:
    patches = json.load(f)
patches = [Patch(**kwargs) for kwargs in patches]

Patch._Patch__patches = patches
