from typing import Iterable, Set

from datapipelines import CompositeDataSource
from .common import RiotAPIService


def _default_services(api_key: str) -> Set[RiotAPIService]:
    from ..common import HTTPClient
    from ..image import ImageDataSource
    from .staticdata import StaticDataAPI
    from .champion import ChampionAPI
    from .summoner import SummonerAPI
    from .championmastery import ChampionMasteryAPI
    from .runepage import RunePageAPI
    from .masterypage import MasteryPageAPI
    from .match import MatchAPI
    from .spectator import SpectatorAPI
    from .status import StatusAPI
    from .leagues import LeaguesAPI

    application_rate_limiters = {}

    client = HTTPClient()
    services = {
        ImageDataSource(client),
        ChampionAPI(api_key, client, application_rate_limiters),
        StaticDataAPI(api_key, client, application_rate_limiters),
        SummonerAPI(api_key, client, application_rate_limiters),
        ChampionMasteryAPI(api_key, client, application_rate_limiters),
        RunePageAPI(api_key, client, application_rate_limiters),
        MasteryPageAPI(api_key, client, application_rate_limiters),
        MatchAPI(api_key, client, application_rate_limiters),
        SpectatorAPI(api_key, client, application_rate_limiters),
        StatusAPI(api_key, client, application_rate_limiters),
        LeaguesAPI(api_key, client, application_rate_limiters)
    }

    return services


class RiotAPI(CompositeDataSource):
    def __init__(self, api_key: str, services: Iterable[RiotAPIService] = None) -> None:
        if services is None:
            services = _default_services(api_key)

        super().__init__(services)
