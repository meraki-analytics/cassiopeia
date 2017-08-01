from typing import Type, TypeVar, Mapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.league import LeaguesListDto

T = TypeVar("T")


class LeaguesAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_leagues_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(LeaguesListDto)
    def get_leagues(self, query: Mapping[str, Any], context: PipelineContext = None) -> LeaguesListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_leagues_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/league/v3/leagues/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "leagues/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data = {"leagues": data}
        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return LeaguesListDto(data)

    _validate_get_many_leagues_query = Query. \
        has("summoner.ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(LeaguesListDto)
    def get_leagues(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LeaguesListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_many_leagues_query(query, context)

        def generator():
            for id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v3/leagues/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=id)
                try:
                    data = self._get(url, {}, self._rate_limiter(query["platform"], "leagues/by-summoner/summonerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["summonerId"] = id
                yield LeaguesListDto(data)

        return generator()
