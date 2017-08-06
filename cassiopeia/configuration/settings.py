import os
import logging

from ..data import Region, Platform
from .load import config


logging.basicConfig(format='%(asctime)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)


def create_default_pipeline(api_key, verbose=False):
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
        DDragonDataSource(),  # TODO: Should this be default?
        RiotAPI(api_key=api_key)
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
    pipeline = DataPipeline(services, [riotapi_transformer])
    pipeline._transformer = riotapi_transformer

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
        for transformer in riotapi_transformer:
            for t in transformer.transforms.items():
                print("Transformer:", t)
        print()

    return pipeline


class Settings(object):
    def __init__(self, settings):
        self.__key = settings["Riot API"]["key"]
        self.__default_region = Region(settings["Riot API"]["region"].upper())
        self.__limits = settings["Riot API"]["limits"]
        self.__pipeline = None
        for name in ["default", "core"]:
            logger = logging.getLogger(name)
            level = settings["logging"].get(name, logging.WARNING)  # Set default logging level to WARNING.
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)

    def set_pipeline(self, pipeline):
        self.__pipeline = pipeline

    def set_region(self, region):
        self.__default_region = region

    @property
    def pipeline(self):
        if self.__pipeline is None:
            if self.__key and not self.__key.startswith("RGAPI"):
                self.__key = os.environ[self.__key]
            self.__pipeline = create_default_pipeline(api_key=self.__key, verbose=False)
        return self.__pipeline

    @property
    def default_region(self):
        return self.__default_region

    @property
    def default_platform(self):
        return Platform[self.__default_region.name]

    @property
    def rate_limits(self):
        return self.__limits


settings = Settings(config)
