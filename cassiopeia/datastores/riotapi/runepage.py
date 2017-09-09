from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.runepage import RunePagesDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class RunePageAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_rune_pages_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(RunePagesDto)
    @validate_query(_validate_get_rune_pages_query, convert_region_to_platform)
    def get_runes_pages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> RunePagesDto:
        url = "https://{platform}.api.riotgames.com/lol/platform/v3/runes/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "runes/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return RunePagesDto(data)

    _validate_get_many_rune_pages_query = Query. \
        has("summoner.ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(RunePagesDto)
    @validate_query(_validate_get_many_rune_pages_query, convert_region_to_platform)
    def get_rune_pages(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[RunePagesDto, None, None]:
        def generator():
            for id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/platform/v3/runes/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "runes/by-summoner/summonerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = query["platform"].region.value
                data["summonerId"] = id
                yield RunePagesDto(data)

        return generator()
