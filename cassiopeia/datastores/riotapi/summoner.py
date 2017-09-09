from typing import Type, TypeVar, MutableMapping, Any, Iterable

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
        has("id").as_(int). \
        or_("account.id").as_(int). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(SummonerDto)
    @validate_query(_validate_get_summoner_query, convert_region_to_platform)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerDto:
        if "id" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v3/summoners/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["id"])
            endpoint = "summoners/summonerId"
        elif "account.id" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v3/summoners/by-account/{accountId}".format(platform=query["platform"].value.lower(), accountId=query["account.id"])
            endpoint = "summoners/by-account/accountId"
        elif "name" in query:
            url = "https://{platform}.api.riotgames.com/lol/summoner/v3/summoners/by-name/{name}".format(platform=query["platform"].value.lower(), name=query["name"].replace(" ", "")).encode("utf-8")
            endpoint = "summoners/by-name/name"
        else:
            endpoint = ""

        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], endpoint))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return SummonerDto(**data)
