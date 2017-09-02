from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import DataSource, DataSink, PipelineContext, Query, NotFoundError

from ...data import Platform, Region
from ...dto.summoner import SummonerDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class SummonerDiskService(SimpleKVDiskService):
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

    ############
    # Summoner #
    ############

    _validate_get_summoner_query = Query. \
        has("id").as_(int). \
        or_("account.id").as_(int). \
        or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(SummonerDto)
    def get_summoner(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> SummonerDto:
        SummonerDiskService._validate_get_summoner_query(query, context)
        platform_str  = query["platform"].value
        for key in self._store:
            if key.startswith("SummonerDto."):
                _, platform, id_, account_id, name = key.split(".")
                if platform == platform_str and any([
                    id_ == str(query.get("id", None)),
                    account_id == str(query.get("account.id", None)),
                    name == query.get("name", None)
                ]):
                    return SummonerDto(self._get(key))
        else:
            raise NotFoundError

    @put.register(SummonerDto)
    def put_summoner(self, item: SummonerDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}.{account_id}.{name}".format(clsname=SummonerDto.__name__,
                                                                     platform=platform,
                                                                     id=item["id"],
                                                                     account_id=item["accountId"],
                                                                     name=item["name"])
        self._put(key, item)
