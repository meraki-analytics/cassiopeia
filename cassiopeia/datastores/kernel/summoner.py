from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import KernelSource, APINotFoundError
from ...data import Platform
from ...dto.summoner import SummonerDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class SummonerAPI(KernelSource):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_summoner_query = Query. \
        has("id").as_(str). \
        or_("accountId").as_(str). \
        or_("puuid").as_(str). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(SummonerDto)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerDto:
        parameters = {"platform": query["platform"].value}
        if "id" in query:
            endpoint = "lol/summoner/v4/summoners/{summonerId}".format(summonerId=query["id"])
        elif "accountId" in query:
            endpoint = "lol/summoner/v4/summoners/by-account/{accountId}".format(accountId=query["accountId"])
        elif "name" in query:
            endpoint = "lol/summoner/v4/summoners/by-name/{name}".format(name=query["name"].replace(" ", "%20"))
        elif "puuid" in query:
            endpoint = "lol/summoner/v4/summoners/by-puuid/{puuid}".format(puuid=query["puuid"])
        else:
            RuntimeError("Impossible")

        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return SummonerDto(**data)
