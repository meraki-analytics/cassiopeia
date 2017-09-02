from typing import Type, TypeVar, MutableMapping, Any, Iterable
import copy

from datapipelines import DataSource, DataSink, PipelineContext, Query, NotFoundError

from ...data import Platform, Region
from ...dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class ChampionMasteryDiskService(SimpleKVDiskService):
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

    ######################
    # Champion Masteries #
    ######################

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").also. \
        has("champion.id").as_(int)

    @get.register(ChampionMasteryDto)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryDto:
        ChampionMasteryDiskService._validate_get_champion_mastery_query(query, context)

        champions_query = copy.deepcopy(query)
        champions_query.pop("champion.id")
        try:
            # Normally we'd call context[context.Keys.PIPELINE].get(...), which says "Get this data, I don't care where it comes from",
            # but in this case we only want to try to get it from this KV store because we only store champion masteries by summoner, not by summoner+champion.
            champions = self.get_champion_mastery_list(query=champions_query, context=context)
        except NotFoundError:
            raise NotFoundError

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        champion = find_matching_attribute(champions["masteries"], "championId", query["champion.id"])
        if champion is None:
            raise NotFoundError
        return ChampionMasteryDto(champion)

    _validate_get_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(int)

    @get.register(ChampionMasteryListDto)
    def get_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryListDto:
        ChampionMasteryDiskService._validate_get_champion_mastery_list_query(query, context)
        platform = query["platform"].value
        summoner_id = query["summoner.id"]
        key = "{clsname}.{platform}.{summoner_id}".format(clsname=ChampionMasteryListDto.__name__,
                                                           platform=platform,
                                                           summoner_id=summoner_id)
        return ChampionMasteryListDto(self._get(key))

    @put.register(ChampionMasteryListDto)
    def put_champion_mastery_list(self, item: ChampionMasteryListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        summoner_id = item["summonerId"]
        key = "{clsname}.{platform}.{summoner_id}".format(clsname=ChampionMasteryListDto.__name__,
                                                           platform=platform,
                                                           summoner_id=summoner_id)
        self._put(key, item)
