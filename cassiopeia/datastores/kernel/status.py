from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import KernelSource, APINotFoundError
from ...data import Platform, Region
from ...dto.staticdata.version import VersionListDto
from ...dto.status import ShardStatusDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


def _get_default_version(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class StatusAPI(KernelSource):
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
    @validate_query(_validate_get_status_query, convert_region_to_platform)
    def get_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatusDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "lol/status/v3/shard-data".format()
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return ShardStatusDto(data)

    _validate_get_many_status_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(ShardStatusDto)
    @validate_query(_validate_get_many_status_query, convert_region_to_platform)
    def get_many_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ShardStatusDto, None, None]:
        def generator():
            parameters = {"platform": query["platform"].value}
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                endpoint = "lol/status/v3/shard-data"
                try:
                    data = self._get(endpoint=endpoint, parameters=parameters)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                yield ShardStatusDto(data)

        return generator()
