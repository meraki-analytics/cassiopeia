from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator
import json

from datapipelines import (
    DataSource,
    PipelineContext,
    Query,
    NotFoundError,
    validate_query,
)
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.staticdata.version import VersionListDto
from ...dto.status import ShardStatusDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


def _get_default_version(
    query: MutableMapping[str, Any], context: PipelineContext
) -> str:
    pipeline = context[PipelineContext.Keys.PIPELINE]
    versions = pipeline.get(VersionListDto, {"platform": query["platform"]})
    return versions["versions"][0]


def _get_default_locale(
    query: MutableMapping[str, Any], context: PipelineContext
) -> str:
    return query["platform"].default_locale


class StatusAPI(RiotAPIService):
    @DataSource.dispatch
    def get(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> T:
        pass

    @DataSource.dispatch
    def get_many(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> Iterable[T]:
        pass

    ##########
    # Status #
    ##########

    _validate_get_status_query = Query.has("platform").as_(Platform)

    @get.register(ShardStatusDto)
    @validate_query(_validate_get_status_query, convert_region_to_platform)
    def get_status(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> ShardStatusDto:
        url = "https://{platform}.api.riotgames.com/lol/status/v4/platform-data".format(
            platform=query["platform"].value.lower()
        )
        try:
            app_limiter, method_limiter = self._get_rate_limiter(
                query["platform"], "status"
            )
            data = self._get(
                url, {}, app_limiter=app_limiter, method_limiter=method_limiter
            )
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return ShardStatusDto(data)

    _validate_get_many_status_query = Query.has("platforms").as_(Iterable)

    @get_many.register(ShardStatusDto)
    @validate_query(_validate_get_many_status_query, convert_region_to_platform)
    def get_many_status(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> Generator[ShardStatusDto, None, None]:
        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/status/v4/platform-data".format(
                    platform=platform.value.lower()
                )
                try:
                    app_limiter, method_limiter = self._get_rate_limiter(
                        query["platform"], "status"
                    )
                    data = json.loads(
                        self._get(
                            url,
                            {},
                            app_limiter=app_limiter,
                            method_limiter=method_limiter,
                        )
                    )
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                yield ShardStatusDto(data)

        return generator()
