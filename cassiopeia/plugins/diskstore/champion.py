from typing import Type, TypeVar, MutableMapping, Any, Iterable
import copy

from datapipelines import DataSource, DataSink, PipelineContext, Query, NotFoundError

from cassiopeia.data import Platform, Region
from cassiopeia.dto.champion import ChampionDto, ChampionListDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class ChampionDiskService(SimpleKVDiskService):
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

    #############
    # Champions #
    #############

    _validate_get_champion_status_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(ChampionDto)
    def get_champion_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        ChampionDiskService._validate_get_champion_status_query(query, context)

        champions_query = copy.deepcopy(query)
        if "id" in champions_query:
            champions_query.pop("id")
        if "name" in champions_query:
            champions_query.pop("name")
        champions = context[context.Keys.PIPELINE].get(ChampionListDto, query=champions_query, context=context)

        def find_matching_attribute(list_of_dtos, attrname, attrvalue):
            for dto in list_of_dtos:
                if dto.get(attrname, None) == attrvalue:
                    return dto

        if "id" in query:
            champion = find_matching_attribute(champions["champions"], "id", query["id"])
        elif "name" in query:
            champion = find_matching_attribute(champions["champions"], "name", query["name"])
        else:
            raise ValueError("Impossible!")
        if champion is None:
            raise NotFoundError
        return ChampionDto(champion)

    _validate_get_champion_status_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("freeToPlay").with_default(False)

    @get.register(ChampionListDto)
    def get_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        ChampionDiskService._validate_get_champion_status_list_query(query, context)
        platform = query["platform"].value
        free_to_play = str(query["freeToPlay"])
        key = "{clsname}.{platform}.{free_to_play}".format(clsname="ChampionStatusListDto",
                                                           platform=platform,
                                                           free_to_play=free_to_play)
        return ChampionListDto(self._get(key))

    @put.register(ChampionListDto)
    def put_champion_status_list(self, item: ChampionListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        free_to_play = item["freeToPlay"]
        key = "{clsname}.{platform}.{free_to_play}".format(clsname="ChampionStatusListDto",
                                                           platform=platform,
                                                           free_to_play=free_to_play)
        self._put(key, item)
