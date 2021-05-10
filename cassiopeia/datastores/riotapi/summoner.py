from typing import Type, TypeVar, MutableMapping, Any, Iterable
import urllib

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.summoner import SummonerDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class SummonerAPI(RiotAPIService):
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
        if "id" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["id"])
            endpoint = "summoners/summonerId"
        elif "accountId" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-account/{accountId}".format(platform=query["platform"].value.lower(), accountId=query["accountId"])
            endpoint = "summoners/by-account/accountId"
        elif "name" in query:
            name = query["name"].replace(" ", "%20")
            url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name}".format(platform=query["platform"].value.lower(), name=name)
            endpoint = "summoners/by-name/name"
        elif "puuid" in query:
            url = url = "https://{platform}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}".format(platform=query["platform"].value.lower(), puuid=query["puuid"])
            endpoint = "summoners/by-puuid/puuid"
        else:
            endpoint = ""

        try:
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return SummonerDto(**data)
