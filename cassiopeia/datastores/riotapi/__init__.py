from typing import Iterable, Set, Dict
import os

from datapipelines import CompositeDataSource
from .common import RiotAPIService, RiotAPIRateLimiter


def _default_services(api_key: str, limiting_share: float = 1.0, request_by_id: bool = True, request_error_handling: Dict = None) -> Set[RiotAPIService]:
    from ..common import HTTPClient
    from ..image import ImageDataSource
    from .staticdata import StaticDataAPI
    from .champion import ChampionAPI
    from .summoner import SummonerAPI
    from .championmastery import ChampionMasteryAPI
    from .match import MatchAPI
    from .spectator import SpectatorAPI
    from .status import StatusAPI
    from .leagues import LeaguesAPI
    from .thirdpartycode import ThirdPartyCodeAPI

    app_rate_limiter = RiotAPIRateLimiter(limiting_share=limiting_share)

    client = HTTPClient()
    services = {
        ImageDataSource(client),
        ChampionAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        StaticDataAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        SummonerAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        ChampionMasteryAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        MatchAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        SpectatorAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        StatusAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        LeaguesAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client),
        ThirdPartyCodeAPI(api_key, app_rate_limiter=app_rate_limiter, request_by_id=request_by_id, request_error_handling=request_error_handling, http_client=client)
    }

    return services


class RiotAPI(CompositeDataSource):
    def __init__(self, api_key: str = None, services: Iterable[RiotAPIService] = None, limiting_share: float = 1.0, request_by_id: bool = True, request_error_handling: Dict = None) -> None:
        if api_key is None:
            api_key = "RIOT_API_KEY"  # Use this env variable.
        if not api_key.startswith("RGAPI"):
            api_key = os.environ.get(api_key, None)

        if services is None:
            services = _default_services(api_key=api_key, limiting_share=limiting_share, request_by_id=request_by_id, request_error_handling=request_error_handling)

        super().__init__(services)

    def set_api_key(self, key: str):
        for sources in self._sources.values():
            for source in sources:
                if isinstance(source, RiotAPIService):
                    source._headers["X-Riot-Token"] = key
