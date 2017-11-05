from abc import abstractmethod, abstractclassmethod
import types
from typing import Mapping, Any, Set, Union, Optional, Type, Generator
import functools
import logging

from merakicommons.ghost import Ghost, ghost_load_on as _ghost_load_on
from merakicommons.container import SearchableList, SearchableLazyList

from .. import configuration
from ..data import Region, Platform
from ..dto.common import DtoObject

try:
    import ujson as json
except ImportError:
    import json


LOGGER = logging.getLogger("core")


def ghost_load_on(method):
    return _ghost_load_on(KeyError, AttributeError)(method)


def provide_default_region(method):
    @functools.wraps(method)
    def default_region_wrapper(self=None, *args, **kwargs):
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
        else:
            if region is not None and not isinstance(region, Region):
                region = Region(region)
        if region is not None:  # region can still be None if the configuration doesn't have a default
            kwargs["region"] = region.value
        if self is not None:
                return method(self, *args, **kwargs)
        else:
            return method(*args, **kwargs)
    return default_region_wrapper


def get_latest_version(region: Union[Region, str], endpoint: Optional[str]):
    from .staticdata.realm import Realms
    if endpoint is not None:
        return Realms(region=region).latest_versions[endpoint]
    else:
        return Realms(region=region).version


class CoreData(object):
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
        # TODO Update this to return the correct stuff when we update the data for this layer.
        return str(self._dto)

    def _update(self, data: Mapping[str, Any]) -> None:
        for key, value in data.items():
            self._set(key, value)

    def _set(self, key, value):
        key = self._renamed.get(key, key)
        self._dto[key] = value


class DataObjectList(list, CoreData):
    def __str__(self):
        return list.__str__(self)

    def __init__(self, *args, **kwargs):
        list.__init__(self, *args)
        CoreData.__init__(self, **kwargs)

    def from_dto(cls, dto: Union[list, DtoObject]):
        self = CoreData.from_dto(dto)
        SearchableList.__init__(self, dto)


class DataObjectGenerator(CoreData):
    def __init__(self, generator: Generator = None, **kwargs):
        self._generator = generator
        super().__init__(**kwargs)


class CassiopeiaObject(object):
    _renamed = {}

    def __init__(self, **kwargs):
        # Note: Dto names are not allowed to be passed in.
        self._data = {_type: None for _type in self._data_types}
        self(**kwargs)

    def __str__(self) -> str:
        # This is a bit strange because we'll print a list of dict-like objects rather than one joined dict, but we've decided it's appropriate.
        result = {}
        for _type, data in self._data.items():
            result[str(_type)] = str(data)
        return str(result).replace("\\'", "'")

    @property
    @abstractmethod
    def _data_types(self) -> Set[type]:
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
                if key in dir(_type):
                    results[_type][key] = value
                    found = True
            if not found:
                # The user passed in a value that we don't know anything about -- raise a warning.
                LOGGER.warning("When initializing {}, key `{}` is not in type(s) {}. Not set.".format(self.__class__.__name__, key, self._data_types))

        # Now that we've parsed the data and know where to put it all, we can update our data.
        for _type, insert_this in results.items():
            if self._data[_type] is not None:
                self._data[_type]._update(insert_this)
            else:
                self._data[_type] = _type(**insert_this)
        return self


class GetFromPipeline(type):
    @provide_default_region
    def __call__(cls: "CassiopeiaPipelineObject", *args, **kwargs):
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
        return super(cls.__class__, cls).__call__(*args, **kwargs)

    @abstractmethod
    def __get_query__(self):
        pass

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, **kwargs):
        return kwargs


class CassiopeiaGhost(CassiopeiaPipelineObject, Ghost):
    def __load__(self, load_group: CoreData = None) -> None:
        if load_group is None:  # Load all groups
            if self._Ghost__all_loaded:
                raise ValueError("object has already been loaded.")
            for group in self._Ghost__load_groups:
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
    def _load_types(self):
        return {t: t for t in self._data_types}

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


class CassiopeiaList(SearchableList, CassiopeiaPipelineObject):
    def __init__(self, *args, **kwargs):
        SearchableList.__init__(self, args)
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    def from_data(cls, *args, **kwargs):
        return cls._construct_normally(*args, **kwargs)

    def __hash__(self):
        return id(self)

    def __str__(self):
        return SearchableList.__str__(self)


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

    def __hash__(self):
        return id(self)

    def __str__(self):
        return SearchableLazyList.__str__(self)
