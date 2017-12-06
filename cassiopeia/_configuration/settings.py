from typing import TypeVar, Type, Dict, Union, List
import logging
import importlib
import inspect
import copy

from datapipelines import DataPipeline, DataSink, DataSource, CompositeDataTransformer, DataTransformer

from ..data import Region, Platform

T = TypeVar("T")

logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)


def create_pipeline(service_configs: Dict, enable_ghost_loading: bool, verbose: int = 0) -> DataPipeline:
    transformers = []

    # Always use the Riot API transformers
    from ..transformers import __transformers__ as riotapi_transformer
    transformers.extend(riotapi_transformer)

    # Add sources / sinks by name from config
    services = []
    for store_name, config in service_configs.items():
        package = config.pop("package", None)
        if package is None:
            package = "cassiopeia.datastores"
        module = importlib.import_module(name=package)
        store_cls = getattr(module, store_name)
        store = store_cls(**config)
        services.append(store)
        service_transformers = getattr(module, "__transformers__", [])
        transformers.extend(service_transformers)

    from ..datastores import Cache, PatchSource

    # Automatically insert the ghost store if it isn't there (and if the setting for ghost loading is on)
    if enable_ghost_loading:
        from ..datastores import UnloadedGhostStore
        found = False
        for datastore in services:
            if isinstance(datastore, UnloadedGhostStore):
                found = True
                break
        if not found:
            if any(isinstance(service, Cache) for service in services):
                # Find the cache and insert the ghost store directly after it
                for i, datastore in enumerate(services):
                    if isinstance(datastore, Cache):
                        services.insert(i+1, UnloadedGhostStore())
                        break
            else:
                # Insert the ghost store at the beginning of the pipeline
                services.insert(0, UnloadedGhostStore())
    else:
        # Enable the data -> core transformers for ghost objects
        enable_ghost_transformers(riotapi_transformer)

    services.append(PatchSource())
    pipeline = DataPipeline(services, transformers)

    # Manually put the cache on the pipeline.
    for datastore in services:
        if isinstance(datastore, Cache):
            pipeline._cache = datastore
            break
    else:
        pipeline._cache = None

    if verbose > 0:
        for service in services:
            print("Service:", service)
            if verbose > 1:
                if isinstance(service, DataSource):
                    for p in service.provides:
                        print("  Provides:", p)
                if isinstance(service, DataSink):
                    for p in service.accepts:
                        print("  Accepts:", p)
        if verbose > 2:
            for transformer in transformers:
                for t in transformer.transforms.items():
                    print("Transformer:", t)
            print()

    return pipeline


def register_transformer_conversion(transformer: DataTransformer, from_type, to_type):
    # Find the method that takes a `from_type` and returns a `to_type` and register it
    methods = inspect.getmembers(transformer, predicate=inspect.ismethod)
    for name, method in methods:
        annotations = copy.copy(method.__annotations__)
        return_type = annotations.pop("return")
        annotations.pop("context", None)
        try:
            if to_type is return_type and from_type in annotations.values():
                transformer.transform.register(from_type, to_type)(method.__func__).__get__(transformer, transformer.__class__)
                break
        except TypeError:
            continue
    else:
        raise RuntimeError("Could not find method to register: {} to {} in {}.".format(from_type, to_type, transformer))


def enable_ghost_transformers(riotapi_transformers: List[CompositeDataTransformer]):
    # Enable the data -> core transformers for ghost objects

    # First, find all the transformer objects in te composite data transformer(s)
    from ..transformers import ChampionMasteryTransformer, LeagueTransformer, MatchTransformer, SpectatorTransformer, StaticDataTransformer, StatusTransformer, SummonerTransformer, ThirdPartyCodeTransformer
    data_transformers = set([transformer
                             for composite_transformer in riotapi_transformers
                             for transformer in composite_transformer._transformers.values()
                             ])

    # Then, for each transformer we want to enable, register the function that's defined
    for transformer in data_transformers:
        if isinstance(transformer, ChampionMasteryTransformer):
            from ..core.championmastery import ChampionMasteryData, ChampionMastery
            register_transformer_conversion(transformer, ChampionMasteryData, ChampionMastery)
        elif isinstance(transformer, LeagueTransformer):
            from ..core.league import LeagueListData, League, ChallengerLeagueListData, ChallengerLeague, MasterLeagueListData, MasterLeague
            register_transformer_conversion(transformer, LeagueListData, League)
            register_transformer_conversion(transformer, ChallengerLeagueListData, ChallengerLeague)
            register_transformer_conversion(transformer, MasterLeagueListData, MasterLeague)
        elif isinstance(transformer, MatchTransformer):
            from ..core.match import MatchData, Match, MatchReferenceData, TimelineData, Timeline
            register_transformer_conversion(transformer, MatchData, Match)
            register_transformer_conversion(transformer, MatchReferenceData, Match)
            register_transformer_conversion(transformer, TimelineData, Timeline)
        elif isinstance(transformer, SpectatorTransformer):
            from ..core.spectator import CurrentGameInfoData, CurrentMatch
            register_transformer_conversion(transformer, CurrentGameInfoData, CurrentMatch)
        elif isinstance(transformer, StaticDataTransformer):
            from ..core.staticdata.champion import ChampionData, Champion
            from ..core.staticdata.rune import RuneData, Rune
            from ..core.staticdata.item import ItemData, Item
            from ..core.staticdata.summonerspell import SummonerSpellData, SummonerSpell
            from ..core.staticdata.map import MapData, Map
            from ..core.staticdata.profileicon import ProfileIconData, ProfileIcon
            register_transformer_conversion(transformer, ChampionData, Champion)
            register_transformer_conversion(transformer, RuneData, Rune)
            register_transformer_conversion(transformer, ItemData, Item)
            register_transformer_conversion(transformer, SummonerSpellData, SummonerSpell)
            register_transformer_conversion(transformer, MapData, Map)
            register_transformer_conversion(transformer, ProfileIconData, ProfileIcon)
        elif isinstance(transformer, StatusTransformer):
            from ..core.status import ShardStatusData, ShardStatus
            register_transformer_conversion(transformer, ShardStatusData, ShardStatus)
        elif isinstance(transformer, SummonerTransformer):
            from ..core.summoner import SummonerData, Summoner
            register_transformer_conversion(transformer, SummonerData, Summoner)
        elif isinstance(transformer, ThirdPartyCodeTransformer):
            from ..core.thirdpartycode import VerificationStringData, VerificationString
            register_transformer_conversion(transformer, VerificationStringData, VerificationString)

    # Re-init the composite transformers to redefine their transformers
    for composite_transformer in riotapi_transformers:
        data_transformers = [transformer for transformer in composite_transformer._transformers.values()]
        composite_transformer.__init__(data_transformers)


def get_default_config():
    return {
        "global": {
            "version_from_match": "patch",
            "default_region": None,
            "enable_ghost_loading": True
        },
        "plugins": {},
        "pipeline": {
            "Cache": {},
            "DDragon": {},
            "RiotAPI": {
                "api_key": "RIOT_API_KEY"
            }
        },
        "logging": {
            "print_calls": True,
            "print_riot_api_key": False,
            "default": "WARNING",
            "core": "WARNING"
        }
    }


class Settings(object):
    def __init__(self, settings):
        _defaults = get_default_config()
        globals_ = settings.get("global", _defaults["global"])
        self.__version_from_match = globals_.get("version_from_match", _defaults["global"]["version_from_match"])  # Valid json values are: "version", "patch", and null
        self.__default_region = globals_.get("default_region", _defaults["global"]["default_region"])
        if self.__default_region is not None:
            self.__default_region = Region(self.__default_region.upper())
        self.__enable_ghost_loading = globals_.get("enable_ghost_loading", _defaults["global"]["enable_ghost_loading"])

        self.__plugins = settings.get("plugins", _defaults["plugins"])

        self.__pipeline_args = settings.get("pipeline", _defaults["pipeline"])
        self.__pipeline = None  # type: DataPipeline

        logging_config = settings.get("logging", _defaults["logging"])
        self.__default_print_calls = logging_config.get("print_calls", _defaults["logging"]["print_calls"])
        self.__default_print_riot_api_key = logging_config.get("print_riot_api_key", _defaults["logging"]["print_riot_api_key"])
        for name in ["default", "core"]:
            logger = logging.getLogger(name)
            level = logging_config.get(name, _defaults["logging"][name])
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

    def set_region(self, region: Union[Region, str]):
        if isinstance(region, str):
            region = Region(region.upper())
        self.__default_region = region

    @property
    def pipeline(self) -> DataPipeline:
        if self.__pipeline is None:
            self.__pipeline = create_pipeline(service_configs=self.__pipeline_args,
                                              enable_ghost_loading=self.__enable_ghost_loading,
                                              verbose=0)
        return self.__pipeline

    @property
    def default_region(self):
        return self.__default_region

    @property
    def default_platform(self):
        return Platform[self.__default_region.name]

    @property
    def version_from_match(self):
        return self.__version_from_match

    @property
    def plugins(self):
        return self.__plugins

    def set_riot_api_key(self, key):
        from ..datastores.riotapi import RiotAPI
        for sources in self.pipeline._sources:
            for source in sources:
                if isinstance(source, RiotAPI):
                    source.set_api_key(key)

    def clear_sinks(self, type: Type[T] = None):
        types = {type}
        if type is not None:
            from ..core.common import CoreData, CassiopeiaObject
            if issubclass(type, CassiopeiaObject):
                for t in type._data_types:
                    types.add(t)
                    types.add(t._dto_type)
            elif issubclass(type, CoreData):
                types.add(type._dto_type)

        for sink in self.pipeline._sinks:
            for type in types:
                sink.clear(type)

    def expire_sinks(self, type: Type[T] = None):
        types = {type}
        if type is not None:
            from ..core.common import CoreData, CassiopeiaObject
            if issubclass(type, CassiopeiaObject):
                for t in type._data_types:
                    types.add(t)
                    types.add(t._dto_type)
            elif issubclass(type, CoreData):
                types.add(type._dto_type)

        for sink in self.pipeline._sinks:
            for type in types:
                sink.expire(type)
