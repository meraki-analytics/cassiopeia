import os
import logging
from typing import Dict, Union

from ..data import Region, Platform
from .load import config


logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)


def create_default_pipeline(riot_api_key: str, championgg_api_key: str = None, limiting_share: float = 1.0, handler_configs: Dict = None, verbose: bool = False):
    from datapipelines import DataPipeline, CompositeDataTransformer
    from ..datastores.cache import Cache
    from ..datastores.riotapi import RiotAPI
    from ..datastores.ddragon import DDragonDataSource
    from ..transformers.staticdata import StaticDataTransformer
    from ..transformers.champion import ChampionTransformer
    from ..transformers.championmastery import ChampionMasteryTransformer
    from ..transformers.summoner import SummonerTransformer
    from ..transformers.match import MatchTransformer
    from ..transformers.masteries import MasteriesTransformer
    from ..transformers.runes import RunesTransformer
    from ..transformers.spectator import SpectatorTransformer
    from ..transformers.status import StatusTransformer
    from ..transformers.leagues import LeagueTransformer

    services = [
        Cache(),  # TODO Add expirations from file
        DDragonDataSource(),
        RiotAPI(api_key=riot_api_key, limiting_share=limiting_share, handler_configs=handler_configs),
    ]
    riotapi_transformer = CompositeDataTransformer([
        StaticDataTransformer(),
        ChampionTransformer(),
        ChampionMasteryTransformer(),
        SummonerTransformer(),
        MatchTransformer(),
        MasteriesTransformer(),
        RunesTransformer(),
        SpectatorTransformer(),
        StatusTransformer(),
        LeagueTransformer()
    ])
    transformers = [riotapi_transformer]

    if "championgg" in settings.plugins:
        from ..plugins.championgg.datastores import ChampionGGSource
        from ..plugins.championgg.transformers import ChampionGGTransformer
        transformers.append(
            ChampionGGTransformer()
        )
        services.append(
            ChampionGGSource(api_key=championgg_api_key)
        )
    pipeline = DataPipeline(services, transformers)

    # Manually put the cache on the pipeline. TODO Is this the best way?
    for datastore in services:
        if isinstance(datastore, Cache):
            pipeline._cache = datastore
            break
    else:
        pipeline._cache = None

    if verbose:
        for service in services:
            for p in service.provides:
                print("Provides:", p)
        for transformer in transformers:
            for t in transformer.transforms.items():
                print("Transformer:", t)
        print()

    return pipeline


class Settings(object):
    def __init__(self, settings):
        riot_api_config = settings.get("Riot API", {})
        self.__riot_api_key = riot_api_config.get("key", None)
        self.__default_region = riot_api_config.get("region", None)
        if self.__default_region is not None:
            self.__default_region = Region(self.__default_region.upper())
        self.__limiting_share = riot_api_config.get("limiting_share", 1.0)
        self.__request_handler_configs = riot_api_config.get("request_handling", {})
        self.__pipeline = None
        self.__plugins = settings.get("plugins", [])
        logging_config = settings.get("logging", {})
        self.__default_print_calls = logging_config.get("print_calls", True)
        self.__default_print_api_key = logging_config.get("print_api_key", False)
        for name in ["default", "core"]:
            logger = logging.getLogger(name)
            level = logging_config.get(name, logging.WARNING)
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

    def set_pipeline(self, pipeline):
        self.__pipeline = pipeline

    def set_region(self, region: Union[Region, str]):
        if isinstance(region, str):
            region = Region(region.upper())
        self.__default_region = region

    @property
    def pipeline(self):
        if self.__pipeline is None:
            if self.__riot_api_key and not self.__riot_api_key.startswith("RGAPI"):
                self.__riot_api_key = os.environ[self.__riot_api_key]
            if "championgg" in self.__plugins:
                championgg_api_key = self.__plugins["championgg"]["key"]
                championgg_api_key = os.environ.get(championgg_api_key, championgg_api_key)
            else:
                championgg_api_key = None
            self.__pipeline = create_default_pipeline(riot_api_key=self.__riot_api_key,
                                                      championgg_api_key=championgg_api_key,
                                                      limiting_share=self.__limiting_share,
                                                      handler_configs=self.__request_handler_configs,
                                                      verbose=False)
            from ..cassiopeia import print_calls
            print_calls(self.__default_print_calls, self.__default_print_api_key)
        return self.__pipeline

    @property
    def default_region(self):
        return self.__default_region

    @property
    def default_platform(self):
        return Platform[self.__default_region.name]

    @property
    def plugins(self):
        return self.__plugins

    def set_riot_api_key(self, key):
        from ..datastores.riotapi import RiotAPI
        for sources in self.pipeline._sources:
            for source in sources:
                if isinstance(source, RiotAPI):
                    source.set_api_key(key)

settings = Settings(config)
