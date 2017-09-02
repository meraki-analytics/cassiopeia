from typing import TypeVar, Type, Set, Iterable

from datapipelines import CompositeDataSource, CompositeDataSink

from .common import SimpleKVDiskService

T = TypeVar("T")


def _default_services() -> Set[SimpleKVDiskService]:
    from .staticdata import StaticDataDiskService
    from .champion import ChampionDiskService
    from .summoner import SummonerDiskService
    from .championmastery import ChampionMasteryDiskService
    #from .runepage import RunePageDiskService
    #from .masterypage import MasteryPageDiskService
    #from .match import MatchDiskService
    #from .spectator import SpectatorDiskService
    #from .status import StatusDiskService
    #from .leagues import LeaguesDiskStore

    services = {
        StaticDataDiskService(),
        ChampionDiskService(),
        SummonerDiskService(),
        ChampionMasteryDiskService()
    }

    return services


class SimpleKVDiskStore(CompositeDataSource, CompositeDataSink):
    def __init__(self, services: Iterable[SimpleKVDiskService] = None):
        if services is None:
            services = _default_services()

        CompositeDataSource.__init__(self, services)
        CompositeDataSink.__init__(self, services)

    def clear(self, type: Type[T] = None):
        sinks = {sink for many_sinks in self._sinks.values() for sink in many_sinks}
        for sink in sinks:
            for key in sink._store:
                if type is None:
                    sink._store.delete(key)
                elif key.startswith("{}.".format(type.__name__)):
                        sink._store.delete(key)

    def delete(self, item: Type[T]):
        raise NotImplemented
