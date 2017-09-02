from typing import Type, TypeVar, MutableMapping, Any, Iterable
import os

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from merakicommons.ratelimits import FixedWindowRateLimiter, MultiRateLimiter

from .dto import ChampionGGListDto
from ...datastores.common import HTTPClient, HTTPError

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class ChampionGG(DataSource):
    def __init__(self, api_key: str, http_client: HTTPClient = None) -> None:
        if not api_key.startswith("RGAPI"):
            api_key = os.environ[api_key]
        self._key = api_key

        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._rate_limiter = MultiRateLimiter(
            FixedWindowRateLimiter(600, 3000),
            FixedWindowRateLimiter(10, 50)
        )

        self._cached_data = {}

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    #############
    # Champions #
    #############

    _validate_get_gg_champion_list_query = Query. \
        has("patch").as_(str).also. \
        can_have("includedData").with_default(lambda *args, **kwargs: "kda,damage,minions,wards,overallPerformanceScore,goldEarned", supplies_type=str).also. \
        can_have("elo").with_default(lambda *args, **kwargs: "PLATINUM_DIAMOND_MASTER_CHALLENGER", supplies_type=str).also. \
        can_have("limit").with_default(lambda *args, **kwargs: 300, supplies_type=int)

    @get.register(ChampionGGListDto)
    def get_gg_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionGGListDto:
        self._validate_get_gg_champion_list_query(query, context)
        elos = ["BRONZE", "SILVER", "GOLD", "PLATINUM", "PLATINUM_DIAMOND_MASTER_CHALLENGER"]
        if not query["elo"] in elos:
            raise ValueError("`elo` must be one of {}".format(elos))

        try:
            return self._cached_data[(self.get_gg_champion_list, query["patch"])]
        except KeyError:
            params = {
                "api_key": self._key,
                "limit": query["limit"],
                "skip": 0,
                "elo": query["elo"],  # TODO For some reason I can't get this to work properly.
                #"champData": "kda,damage,minions,wins,wards,positions,normalized,averageGames,overallPerformanceScore,goldEarned,sprees,hashes,wins,maxMins,matchups",
                "champData": query["includedData"],
                "sort": "winRate-desc",
                "abriged": False
            }
            params = "&".join(["{key}={value}".format(key=key, value=value) for key, value in params.items()])

            url = "http://api.champion.gg/v2/champions"
            try:
                data, response_headers = self._client.get(url, params, rate_limiters=[self._rate_limiter], connection=None, encode_parameters=False)
            except HTTPError as error:
                if error.code == 403:
                    raise HTTPError(message="Forbidden", code=error.code)
                raise NotFoundError(str(error)) from error

            for datum in data:
                datum.pop("_id")
            result = ChampionGGListDto({"data": data})
            self._cached_data[(self.get_gg_champion_list, query["patch"])] = result
            return result
