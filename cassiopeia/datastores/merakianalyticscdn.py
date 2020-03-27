from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, NotFoundError

from ..dto.patch import PatchListDto
from ..dto.staticdata.champion import ChampionAllRatesDto, ChampionRatesDto
from .common import HTTPClient, HTTPError

try:
    import ujson as json
except ImportError:
    import json
    json.decode = json.loads

T = TypeVar("T")


class MerakiAnalyticsCDN(DataSource):
    def __init__(self, http_client: HTTPClient = None) -> None:
        if http_client is None:
            self._client = HTTPClient()
        else:
            self._client = http_client
        self._cache = {}

    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    def calculate_hash(self, query):
        hash = list(value for _, value in sorted(query.items()))
        return tuple(hash)

    ##############
    # Patch List #
    ##############

    @get.register(PatchListDto)
    def get_patch_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> PatchListDto:
        url = "https://cdn.merakianalytics.com/riot/lol/resources/patches.json"
        try:
            body = self._client.get(url)[0]
            body = json.decode(body)
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        return PatchListDto(**body)


    ##################
    # Champion Rates #
    ##################

    @get.register(ChampionAllRatesDto)
    def get_champion_all_rates(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionAllRatesDto:
        try:
            return self._cache[ChampionRatesDto]
        except KeyError:
            pass
        url = "http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/championrates.json"
        try:
            body = self._client.get(url)[0]
            body = json.decode(body)
            body["data"] = {int(k): v for k, v in body["data"].items()}
        except HTTPError as e:
            raise NotFoundError(str(e)) from e

        result = ChampionAllRatesDto(**body)
        self._cache[ChampionRatesDto] = result
        return result

    @get.register(ChampionRatesDto)
    def get_champion_rates(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionRatesDto:
        data = self.get_champion_all_rates(query, context)
        rates = data["data"][query["id"]]
        return ChampionRatesDto(**rates)
