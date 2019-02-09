from typing import Iterable, Set

from datapipelines import CompositeDataSource
from .common import KernelSource


def _default_services(server_url: str, port: int) -> Set[KernelSource]:
    from ..common import HTTPClient
    from ..image import ImageDataSource
    from .champion import ChampionAPI
    from .summoner import SummonerAPI
    from .championmastery import ChampionMasteryAPI
    from .match import MatchAPI
    from .spectator import SpectatorAPI
    from .status import StatusAPI
    from .leagues import LeaguesAPI
    from .thirdpartycode import ThirdPartyCodeAPI

    client = HTTPClient()
    services = {
        ImageDataSource(client),
        ChampionAPI(server_url=server_url, port=port, http_client=client),
        SummonerAPI(server_url=server_url, port=port, http_client=client),
        ChampionMasteryAPI(server_url=server_url, port=port, http_client=client),
        MatchAPI(server_url=server_url, port=port, http_client=client),
        SpectatorAPI(server_url=server_url, port=port, http_client=client),
        StatusAPI(server_url=server_url, port=port, http_client=client),
        LeaguesAPI(server_url=server_url, port=port, http_client=client),
        ThirdPartyCodeAPI(server_url=server_url, port=port, http_client=client)
    }

    return services


class Kernel(CompositeDataSource):
    def __init__(self, server_url: str, port: int, services: Iterable[KernelSource] = None) -> None:

        if services is None:
            services = _default_services(server_url=server_url, port=port)

        super().__init__(services)

    def set_server_url_and_port(self, server_url: str, port: int):
        for sources in self._sources.values():
            for source in sources:
                if isinstance(source, KernelSource):
                    source._server_url = server_url
                    source._port = port
