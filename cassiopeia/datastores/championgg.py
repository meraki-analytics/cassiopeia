from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from merakicommons.ratelimits import FixedWindowRateLimiter, MultiRateLimiter

from ..data import Platform
from ..dto.championgg import GGChampionDto, GGChampionListDto
from .common import HTTPClient, HTTPError
from .riotapi.staticdata import _get_default_version

try:
    import ujson as json
except ImportError:
    import json

T = TypeVar("T")


class ChampionGGSource(DataSource):
    def __init__(self, api_key: str, http_client: HTTPClient = None) -> None:
        self._key = api_key

        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client

        self._rate_limiter = MultiRateLimiter(
            FixedWindowRateLimiter(600, 3000),
            FixedWindowRateLimiter(10, 50)
        )

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
        has("platform").as_(Platform).also. \
        can_have("version").with_default(_get_default_version, supplies_type=str)

    @get.register(GGChampionListDto)
    def get_gg_champion_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> GGChampionListDto:
        self._validate_get_gg_champion_list_query(query, context)
        latest_version = _get_default_version(query=query, context=context)
        if query["version"] != latest_version:
            raise ValueError("Can only get champion.gg data for champions on the most recent version.")

        params = {
            "api_key": self._key,
            "limit": 300,
            "skip": 0,
            #"elo": "PLATINUM,DIAMOND,MASTER,CHALLENGER",
            #"champData": "kda,damage,minions,wins,wards,positions,normalized,averageGames,overallPerformanceScore,goldEarned,sprees,hashes,wins,maxMins,matchups",
            "sort": "winRate-desc",
            "abriged": False
        }
        params = "&".join(["{key}={value}".format(key=key, value=value) for key, value in params.items()])

        url = "http://api.champion.gg/v2/champions"
        try:
            data, response_headers = self._client.get(url, params, rate_limiter=self._rate_limiter, connection=None, encode_parameters=False)
        except HTTPError as error:
            raise NotFoundError(str(error)) from error

        for datum in data:
            datum.pop("_id")
        return GGChampionListDto({"region": query["platform"].region.value, "data": data})
