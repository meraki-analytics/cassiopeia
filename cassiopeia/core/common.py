from abc import abstractmethod, abstractclassmethod
from typing import Mapping, Any, Set, Dict
from enum import Enum
import functools
import copy
import logging

from datapipelines import NotFoundError, UnsupportedError
from merakicommons.ghost import Ghost

from ..configuration import settings
from ..data import Region, Platform

try:
    import ujson as json
except ImportError:
    import json


LOGGER = logging.getLogger("core")


def provide_default_region(method):
    @functools.wraps(method)
    def default_region_wrapper(self=None, **kwargs):
        region = kwargs.pop("region", None)
        platform = kwargs.pop("platform", None)
        if region is None:
            if platform is None:
                region = settings.default_region
            else:
                if isinstance(platform, Platform):
                    region = platform.region
                else:
                    region = Platform(platform).region
        else:
            if not isinstance(region, Region):
                region = Region(region)
        kwargs["region"] = region.value
        if self:
                return method(self, **kwargs)
        else:
            return method(**kwargs)
    return default_region_wrapper


def get_latest_version(region):
    from .staticdata.version import Versions
    versions = settings.pipeline.get(Versions, query={"region": region})
    return versions[0]

class DataObject(object):
    def __init__(self, **kwargs):
        self._dto = {}
        self._update(kwargs)

    @classmethod
    def from_dto(cls, dto):
        self = cls()
        self._dto = dto
        return self

    @property
    @abstractclassmethod
    def _renamed(cls) -> Mapping[str, str]:
        """A mapping of the new method names to the old. If a name wasn't changed, it is not in this mapping."""
        pass

    def __contains__(self, item):
        return self._renamed.get(item, item) in self._dto

    def __iter__(self):
        for key in dir(self):
            if key in self:
                yield key

    def __str__(self):
        return str(self._dto)
        #result = {}
        #for key in dir(self):  # `vars` won't recursively look in the obj for things like properties, see htt#ps://stackoverflow.com/questions/980249/difference-between-dir-and-vars-keys-in-python
        #    if not key.startswith("_") and key is not "from_dto":
        #        # Don't just fail to print if the API didn't return a value.
        #        try:
        #            value = getattr(self, key)
        #            if isinstance(value, DataObject):
        #                value = str(value)
        #            elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], DataObject):
        #                value = [str(v) for v in value]
        #            elif isinstance(value, dict) and len(value) > 0 and isinstance(next(iter(value.values())), DataObject):
        #                value = {key: str(v) for key, v in value.items()}
        #            result[key] = value
        #        except KeyError:  # A KeyError will be thrown when the properties try to do the dto lookup if the data doesn't exist
        #            pass
        #return str(result).replace("\\'", "'")

    def _update(self, data: Mapping[str, Any]) -> None:
        for key, value in data.items():
            self._set(key, value)

    def _set(self, key, value):
        key = self._renamed.get(key, key)
        self._dto[key] = value


class CheckCache(type):  # TODO Should all CassiopeiaObjects use this, or just CassiopeiaGhosts?
    def __call__(cls, data: DataObject = None, **kwargs):
        try:
            region = data.region
        except (AttributeError, KeyError):
            try:
                region = kwargs["region"]
            except KeyError:
                try:
                    platform = kwargs["platform"]
                    if isinstance(platform, Platform):
                        region = platform.region.value
                    else:
                        region = Platform(platform).region.value
                except KeyError:
                    region = settings.default_region

        cache = settings.pipeline._cache
        if cache is not None:
            # Try to find the obj in the cache
            from ..datastores.uniquekeys import construct_query
            assert not data or not kwargs  # Only one or the other should be provided.
            if data:
                query = construct_query(cls, data)
            else:  # have kwargs
                query = construct_query(cls, **kwargs)
            if "region" not in query:
                query["region"] = region
            if hasattr(cls, "version") and "version" not in query:
                try:
                    query["version"] = data.version
                except (AttributeError, KeyError):
                    query["version"] = get_latest_version(query["region"])
            try:
                assert "data" not in query
                return cache.get(cls, query=query)
            except (NotFoundError, UnsupportedError):
                pass

        # If the obj was not found in the cache (or if there is no cache), create a new instance
        LOGGER.debug("Creating new {} from {}".format(cls.__name__, set(kwargs.keys())))
        return super().__call__(**kwargs)


class CassiopeiaObject(object, metaclass=CheckCache):
    _renamed = {}

    def __init__(self, **kwargs):
        # Note: Dto names are not allowed to be passed in.
        self._data = {type: type() for type in self._data_types}
        self(**kwargs)

    @classmethod
    def from_data(cls, data: DataObject):
        assert data is not None
        self = cls(data)
        self._data = {type: type() for type in self._data_types}
        if data.__class__ not in self._data_types:
            raise TypeError("Wrong data type '{}' passed to '{}.from_data'".format(data.__class__.__name__, self.__class__.__name__))
        self._data[data.__class__] = data
        # Without the below for-loops, if a Champion is instantiated with a StaticData data with `id`
        # in it, and then `.free_to_play` is called on that object, the query won't have an `id`.
        other_types = self._data_types - {data.__class__}
        for type in other_types:
            for key in data:
                value = getattr(data, key)
                if key in dir(type):
                    self._data[type]._set(key, value)
        return self

    def __str__(self) -> str:
        # This is a bit strange because we'll print a list of dict-like objects rather than one joined dict, but we've decided it's appropritate.
        result = {}
        for type, data in self._data.items():
            result[str(type)] = str(data)
        return str(result).replace("\\'", "'")

    @property
    @abstractmethod
    def _data_types(self) -> Set[type]:
        """The `DataObject`_ types that belongs to this core type."""
        pass

    def __call__(self, **kwargs) -> "CassiopeiaObject":
        """Updates `self` with `kwargs` and returns `self`.

        Useful for updating default API parameters, for example:

            for champion in cass.get_champions():
                champion(champData={"tags"}).tags  # only pulls the tag data
        """
        # Update underlying data and deconstruct any Enums the user passed in.
        found = False
        for key, value in kwargs.items():
            for type in self._data_types:
                # Don't allow dto names to be passed in.
                if key in dir(type):
                    u = {key: value}
                    self._data[type]._update(u)
                    found = True
            if not found:
                LOGGER.warning("When initializing {}, key `{}` is not in type(s) {}. Not set.".format(self.__class__.__name__, key, self._data_types))
        return self


class CassiopeiaGhost(CassiopeiaObject, Ghost):
    def __load__(self, load_group: DataObject = None) -> None:
        if load_group is None:  # Load all groups
            if self._Ghost__all_loaded:
                raise ValueError("object has already been loaded.")
            for group in self._Ghost__load_groups:
                if not self._Ghost__is_loaded(group):
                    self.__load__(group)
        else:  # Load the specific load group
            if self._Ghost__is_loaded(load_group):
                raise ValueError("object has already been loaded.")
            query = copy.deepcopy(self._data[load_group]._dto)
            if hasattr(self.__class__, "version") and "version" not in query:
                from .staticdata import Versions
                versions = settings.pipeline.get(Versions, query={"region": query["region"]})
                query["version"] = versions[0]

            from ..datastores.uniquekeys import construct_query
            query = self.__get_query__()
            data = settings.pipeline.get(type=self._load_types[load_group], query=query)
            self.__load_hook__(load_group, data)

    @property
    def _load_types(self):
        return {t: t for t in self._data_types}

    @abstractmethod
    def __get_query__(self):
        pass

    def __load_hook__(self, load_group, data: DataObject):
        if not isinstance(data, DataObject):
            raise TypeError("expected subclass of DataObject, got {cls}".format(cls=data.__class__))
        self._data[load_group] = data
