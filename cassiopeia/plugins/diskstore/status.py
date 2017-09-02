from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, DataSink, PipelineContext, Query, NotFoundError

from cassiopeia.data import Platform, Region
from cassiopeia.dto.status import ShardStatusDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class ShardStatusDiskService(SimpleKVDiskService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    ##########
    # Status #
    ##########

    _validate_get_status_query = Query. \
        has("platform").as_(Platform)

    @get.register(ShardStatusDto)
    def get_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ShardStatusDto:
        ShardStatusDiskService._validate_get_status_query(query, context)
        key = "{clsname}.{platform}".format(clsname=ShardStatusDto.__name__, platform=query["platform"].value)
        return ShardStatusDto(self._get(key))

    @put.register(ShardStatusDto)
    def put_status(self, item: ShardStatusDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}".format(clsname=ShardStatusDto.__name__, platform=platform)
        self._put(key, item)
