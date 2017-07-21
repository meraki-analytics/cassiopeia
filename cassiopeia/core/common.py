from abc import abstractmethod, abstractclassmethod
from typing import Mapping, Any, Set
from enum import Enum
import logging

from datapipelines import NotFoundError
from merakicommons.ghost import Ghost

from ..configuration import settings

try:
    import ujson as json
except ImportError:
    import json


LOGGER = logging.getLogger("core")


class DataObject(object):
    def __init__(self, dto):
        self._dto = dto

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
        result = {}
        for key in dir(self):  # `vars` won't recursively look in the obj for things like properties, see https://stackoverflow.com/questions/980249/difference-between-dir-and-vars-keys-in-python
            if not key.startswith("_"):
                # Don't just fail to print if the API didn't return a value.
                try:
                    value = getattr(self, key)
                    if isinstance(value, DataObject):
                        value = str(value)
                    elif isinstance(value, list) and len(value) > 0 and isinstance(value[0], DataObject):
                        value = [str(v) for v in value]
                    elif isinstance(value, dict) and len(value) > 0 and isinstance(next(iter(value.values())), DataObject):
                        value = {key: str(v) for key, v in value.items()}
                    result[key] = value
                except KeyError:  # A KeyError will be thrown when the properties try to do the dto lookup if the data doesn't exist
                    pass
        return str(result).replace("\\'", "'")

    def _update(self, data: Mapping[str, Any]) -> None:
        for key, value in data.items():
            self._set(key, value)

    def _set(self, item, value):
        name = self._renamed.get(item, item)
        self._dto[name] = value


class CheckCache(type):  # TODO Should all CassiopeiaObjects use this, or just CassiopeiaGhosts?
    def __call__(cls, *args, **kwargs):
        cache = settings.pipeline._cache
        if cache is not None:
            # Try to find the obj in the cache
            try:
                return cache.get(cls, query=kwargs)
            except NotFoundError:
                pass

        # If the obj was not found in the cache (or if there is no cache), create a new instance
        LOGGER.debug("Creating new {} from {}".format(cls.__name__, set(kwargs.keys())))
        obj = super().__call__(**kwargs)

        # Store the new obj in the cache
        if cache is not None:
            cache.put(cls, obj)

        return obj


class CassiopeiaObject(object):
    _retyped = {}

    def __init__(self, data: DataObject = None, **kwargs):
        # Note: Dto names are not allowed to be passed in.
        self._data = {type: type({}) for type in self._data_types}

        if data is not None:
            if data.__class__ not in self._data_types:
                raise TypeError("Wrong data type '{}' passed to '{}'".format(data.__class__.__name__, self.__class__.__name__))
            self._data[data.__class__] = data
            # Without the below for-loops, if a Champion is instantiated with a StaticData data with `id`
            # in it, and then `.free_to_play` is called on that object, the query won't have an `id`.
            # Also the Enums wouldn't be deconstructed.
            # This code is ~ duplicated from __call__.
            other_types = self._data_types - {data.__class__}
            for key in data:
                value = getattr(data, key)
                if isinstance(value, Enum):
                    value = value.name
                    self._data[data.__class__]._set(key, value)
                for type in other_types:
                    if key in dir(type):
                        self._data[type]._set(key, value)
        self(**kwargs)

    def __str__(self) -> str:
        # This is a bit strange because we'll print a list of dict-like objects rather than one joined dict, but we've decided it's appropritate.
        result = {}
        for type, data in self._data.items():
            result[str(type)] = str(data)
        return str(result).replace("\\'", "'")

    @property
    @abstractmethod
    def _data_types(self) -> Set[DataObject]:
        """The `DataObject`_ type that belongs to this core type."""
        pass

    def __call__(self, **kwargs) -> "CassiopeiaObject":
        """Updates `self` with `kwargs` and returns `self`.

        Useful for updating default API parameters, for example:

            for champion in cass.get_champions():
                champion(champData={"tags"}).tags  # only pulls the tag data
        """
        # Update underlying data and deconstruct any Enums the user passed in.
        # Note that this code is duplicated in __init__ as well.
        for key, value in kwargs.items():
            try:
                types_key, rightkey = self._retyped[key][value.__class__]
                _ = kwargs.pop(key)
                key = rightkey
                if types_key is not None:
                    value = getattr(value, types_key)
                kwargs[rightkey] = value
            except KeyError:
                pass
            found = False
            for type in self._data_types:
                # Don't allow dto names to be passed in.
                if key in dir(type):
                    u = {key: value}
                    self._data[type]._update(u)
                    found = True
            if not found:
                LOGGER.warning("When initializing {}, key {} is not in type(s) {}. Not set.".format(self.__class__.__name__, key, self._data_types))
        return self


class CassiopeiaGhost(CassiopeiaObject, Ghost, metaclass=CheckCache):
    def __str__(self) -> str:
        if not self._Ghost__all_loaded:
            self.__load__(load_group=None)
        return super().__str__()

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
            data = settings.pipeline.get(type=self._load_types[load_group], query=self._data[load_group]._dto)
            self.__load_hook__(load_group, data)

    @property
    def _load_types(self):
        return {t: t for t in self._data_types}

    def __load_hook__(self, load_group, data):
        self._data[load_group]._dto.update(data._dto)
