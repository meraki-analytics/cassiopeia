from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.staticdata.version import VersionListDto
from ...dto.status import ShardStatusDto

T = TypeVar("T")


def _get_default_version(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class StatusAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    ##########
    # Status #
    ##########

    _validate_get_status_query = Query. \
        has("platform").as_(Platform)

    @get.register(ShardStatusDto)
    def get_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatusDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StatusAPI._validate_get_status_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/status/v3/shard-data".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "status"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return ShardStatusDto(data)

    _validate_get_many_status_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(ShardStatusDto)
    def get_many_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ShardStatusDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        StatusAPI._validate_get_many_status_query(query, context)

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/status/v3/shard-data".format(platform=platform.value.lower())
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "status"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["locale"] = query["locale"] if "locale" in query else platform.default_locale
                data["includedData"] = query["includedData"]
                yield ShardStatusDto(data)

        return generator()
