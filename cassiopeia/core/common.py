from abc import abstractmethod, abstractclassmethod
import types
from typing import Mapping, Set, Union, Optional, Type, Generator
import functools
import logging
from enum import Enum
import arrow
import datetime
import inspect

from merakicommons.ghost import Ghost, ghost_load_on as _ghost_load_on
from merakicommons.container import SearchableLazyList

from .. import configuration
from ..data import Region, Platform

import json  # Can't use ujson here because of the encoder


LOGGER = logging.getLogger("core")


def ghost_load_on(method):
    return _ghost_load_on(AttributeError)(method)


def add_region_to_kwargs(kwargs):
    region = kwargs.pop("region", None)
    platform = kwargs.pop("platform", None)
    if region is None:
        if platform is None:
            region = configuration.settings.default_region
        else:
            if isinstance(platform, Platform):
                region = platform.region
            else:
                region = Platform(platform).region
    elif not isinstance(region, Region):
        region = Region(region)
    if region is not None:  # region can still be None if the configuration doesn't have a default
        kwargs["region"] = region.value
    return kwargs


def provide_default_region(method):
    @functools.wraps(method)
    def default_region_wrapper(*args, **kwargs):
        kwargs = add_region_to_kwargs(kwargs)
        return method(*args, **kwargs)
    #def default_region_wrapper(self=None, *args, **kwargs):
    #    kwargs = add_region_to_kwargs(kwargs)
    #    if self is not None:
    #        return method(self, *args, **kwargs)
    #    else:
    #        return method(*args, **kwargs)
    return default_region_wrapper


def get_latest_version(region: Union[Region, str], endpoint: Optional[str]):
    from .staticdata.realm import Realms
    if endpoint is not None:
        return Realms(region=region).latest_versions[endpoint]
    else:
        return Realms(region=region).version


class CoreData(object):
    @property
    @abstractclassmethod
    def _renamed(cls) -> Mapping[str, str]:
        pass

    def __init__(self, **kwargs):
        self(**kwargs)

    def __call__(self, **kwargs):
        for key, value in kwargs.items():
            new_key = self._renamed.get(key, key)
            setattr(self, new_key, value)
        return self

    def to_dict(self):
        d = {}
        attrs = {attrname for attrname in dir(self)} - {attrname for attrname in dir(self.__class__)}
        for attr in attrs:
            v = getattr(self, attr)
            if isinstance(v, CoreData):
                v = v.to_dict()
            elif hasattr(v, "__iter__") and not isinstance(v, str):
                if isinstance(v, dict):
                    new_v = {}
                    for k, vi in v.items():
                        if isinstance(vi, CoreData):
                            new_v[k] = vi.to_dict()
                        else:
                            new_v[k] = vi
                    v = new_v
                else:
                    v = [vi.to_dict() if isinstance(vi, CoreData) else vi for vi in v]
            d[attr] = v
        return d


class CoreDataList(list, CoreData):
    def __str__(self):
        return list.__str__(self)

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        CoreData.__init__(self, **kwargs)


class CassiopeiaObject(object):
    _renamed = {}

    def __init__(self, **kwargs):
        # Note: Dto names are not allowed to be passed in.
        self._data = {_type: None for _type in self._data_types}
        # Re-implement __call__ code here so that __call__ can be overridden in subclasses
        results = {_type: {}  for _type in self._data_types}
        found = False
        for key, value in kwargs.items():
            # We don't know which type to put the piece of data under, so put it in any type that supports this key
            for _type in self._data_types:
                if issubclass(_type, CoreData) or key in dir(_type):
                    results[_type][key] = value
                    found = True
            if not found:
                # The user passed in a value that we don't know anything about -- raise a warning.
                LOGGER.warning("When initializing {}, key `{}` is not in type(s) {}. Not set.".format(self.__class__.__name__, key, self._data_types))

        # Now that we've parsed the data and know where to put it all, we can update our data.
        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)

    def __str__(self) -> str:
        # This is a bit strange because we'll print a list of dict-like objects rather than one joined dict, but we've decided it's appropriate.
        result = {}
        for _type, data in self._data.items():
            result[str(_type)] = str(data)
        return str(result).replace("\\'", "'")

    @property
    @abstractclassmethod
    def _data_types(cls) -> Set[type]:
        """The `CoreData`_ types that belongs to this core type."""
        pass

    @classmethod
    def from_data(cls, data: CoreData):
        assert data is not None
        self = cls()

        if data.__class__ not in self._data_types:
            raise TypeError("Wrong data type '{}' passed to '{}.from_data'".format(
                data.__class__.__name__, self.__class__.__name__))
        self._data[data.__class__] = data
        return self

    def __call__(self, **kwargs) -> "CassiopeiaObject":
        """Updates `self` with `kwargs` and returns `self`.

        Useful for updating default API parameters, for example:

            for champion in cass.get_champions():
                champion(champData={"tags"}).tags  # only pulls the tag data
        """
        # Update underlying data and deconstruct any Enums the user passed in.
        results = {_type: {}  for _type in self._data_types}
        found = False
        for key, value in kwargs.items():
            # We don't know which type to put the piece of data under, so put it in any type that supports this key
            for _type in self._data_types:
                if issubclass(_type, CoreData) or key in dir(_type):
                    results[_type][key] = value
                    found = True
            if not found:
                # The user passed in a value that we don't know anything about -- raise a warning.
                LOGGER.warning("When initializing {}, key `{}` is not in type(s) {}. Not set.".format(self.__class__.__name__, key, self._data_types))

        # Now that we've parsed the data and know where to put it all, we can update our data.
        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type] = self._data[_type](**insert_this)
            else:
                self._data[_type] = _type(**insert_this)
        return self

    def to_dict(self):
        d = {}
        for data_type in self._data_types:
            new = self._data[data_type].to_dict()
            d.update(new)
        return d

    def to_json(self, **kwargs):
        return json.dumps(self.to_dict(), cls=CassiopeiaJsonEncoder, **kwargs)

    def __json__(self, **kwargs):
        return self.to_json(**kwargs)


class GetFromPipeline(type):
    def __call__(cls: "CassiopeiaPipelineObject", *args, **kwargs):
        if 'region' in inspect.signature(cls.__get_query_from_kwargs__).parameters:
            kwargs = add_region_to_kwargs(kwargs)
        pipeline = configuration.settings.pipeline
        query = cls.__get_query_from_kwargs__(**kwargs)
        if hasattr(cls, "version") and query.get("version", None) is None and cls.__name__ not in ["Realms", "Match"]:
            query["version"] = get_latest_version(region=query["region"], endpoint=None)
        return pipeline.get(cls, query=query)


class CassiopeiaPipelineObject(CassiopeiaObject, metaclass=GetFromPipeline):
    @classmethod
    def _construct_normally(cls, *args, **kwargs) -> "CassiopeiaObject":
        # cls.__class__ will be this class's metaclass (GetFromPipeline), so supering that will find the metaclass's
        # class, which is `type` in this case. Then `type`'s `__call__` will be called.
        # This has the effect of skipping the GetFromPipeline instantiation, and defaulting to the normal class
        # instantiation for the class.
        # TODO I don't know how to handle includedData -> included_data for core...
        if "includedData" in kwargs:
            kwargs["included_data"] = kwargs.pop("includedData")
        return super(cls.__class__, cls).__call__(*args, **kwargs)

    @abstractmethod
    def __get_query__(self):
        pass

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, **kwargs):
        return kwargs

    def __hash__(self):
        stuff = sorted(self.__get_query__().items())
        for i, (key, value) in enumerate(stuff):
            if isinstance(value, set):
                stuff[i] = (key, tuple(value))
        return hash(tuple(stuff))

    def __eq__(self, other: "CassiopeiaPipelineObject") -> bool:
        if not isinstance(other, self.__class__):  # Using isinstance here seems bad
            return False
        else:
            return hash(self) == hash(other)

    def __ne__(self, other: "CassiopeiaPipelineObject") -> bool:
        return not self == other


class CassiopeiaGhost(CassiopeiaPipelineObject, Ghost):
    def load(self, load_groups: Set = None) -> "CassiopeiaGhost":
        if load_groups is None:
            load_groups = self._Ghost__load_groups
        if self._Ghost__all_loaded:
            return self
        self.__load__()
        for load_group in load_groups:
            self._Ghost__set_loaded(load_group)  # __load__ doesn't trigger __set_loaded.
        return self

    def __load__(self, load_group: CoreData = None, load_groups: Set = None) -> None:
        if load_groups is None:
            load_groups = self._Ghost__load_groups
        if load_group is None:  # Load all groups
            if self._Ghost__all_loaded:
                raise ValueError("object has already been loaded.")
            for group in load_groups:
                if not self._Ghost__is_loaded(group):
                    self.__load__(group)
        else:  # Load the specific load group
            if self._Ghost__is_loaded(load_group):
                raise ValueError("object has already been loaded.")
            query = self.__get_query__()
            if hasattr(self.__class__, "version") and "version" not in query and not self.__class__.__name__ == "Realms":
                query["version"] = get_latest_version(region=query["region"], endpoint=None)
            data = configuration.settings.pipeline.get(type=self._load_types[load_group], query=query)
            self.__load_hook__(load_group, data)

    @property
    def _load_types(cls):
        return {t: t for t in cls._data_types}

    @property
    def _load_type(cls):
        return cls

    @classmethod
    def from_data(cls, data: CoreData, loaded_groups: Optional[Set[Type[CoreData]]] = None):
        assert data is not None
        # Manually skip the CheckCache (well, all metaclass' __call__s) for ghost objects if they are
        # created via this constructor.
        self = cls._construct_normally()

        # Make spots for the data and put it in
        self._data = {_type: None for _type in self._data_types}
        if data.__class__ not in self._data_types:
            raise TypeError("Wrong data type '{}' passed to '{}.from_data'".format(
                data.__class__.__name__, self.__class__.__name__))
        self._data[data.__class__] = data

        # Set as loaded
        if loaded_groups is None:
            for load_group in self._Ghost__load_groups:
                self._Ghost__set_loaded(load_group)
        else:
            for load_group in loaded_groups:
                self._Ghost__set_loaded(load_group)
        return self

    def __load_hook__(self, load_group: CoreData, data: CoreData) -> None:
        if not isinstance(data, CoreData):
            raise TypeError("expected subclass of CoreData, got {cls}".format(cls=data.__class__))
        self._data[load_group] = data


class CassiopeiaLazyList(SearchableLazyList, CassiopeiaPipelineObject):
    def __init__(self, *args, **kwargs):
        if "generator" in kwargs:
            generator = kwargs.pop("generator")
        else:
            if len(args) == 1 and isinstance(args[0], types.GeneratorType):
                generator = args[0]
            else:
                def generator(*args):
                    for arg in args:
                        yield arg
                generator = generator(args)
        SearchableLazyList.__init__(self, generator)
        # Something feels very wrong; this is meant to work with MatchHistory.from_generator
        if self.__class__ is not CassiopeiaLazyList:
            self.__init__(**kwargs)
        else:
            CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    def from_data(cls, *args, **kwargs):
        return cls._construct_normally(*args, **kwargs)

    @classmethod
    def from_generator(cls, generator: Generator, **kwargs):
        self = cls.__new__(cls)
        CassiopeiaLazyList.__init__(self, generator=generator, **kwargs)
        return self

    def __hash__(self):
        return id(self)

    def __str__(self):
        return SearchableLazyList.__str__(self)


class CassiopeiaJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        elif isinstance(obj, (datetime.datetime, arrow.Arrow)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return obj.seconds
        return json.JSONEncoder.default(self, obj)
