import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import KernelSource, APINotFoundError
from ...data import Platform
from ...dto.champion import ChampionRotationDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class ChampionAPI(KernelSource):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_rotation_query = Query. \
        has("platform").as_(Platform)

    @get.register(ChampionRotationDto)
    @validate_query(_validate_get_champion_rotation_query, convert_region_to_platform)
    def get_champion_rotation(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionRotationDto:
        parameters = {"platform": query["platform"].value}
        endpoint = "lol/platform/v3/champion-rotations"
        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["platform"] = query["platform"].value
        data["region"] = query["platform"].region.value
        return ChampionRotationDto(**data)

    _validate_get_many_champion_rotation_query = Query. \
        has("platforms").as_(Iterable)

    @get_many.register(ChampionRotationDto)
    @validate_query(_validate_get_many_champion_rotation_query, convert_region_to_platform)
    def get_many_champion_rotations(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionRotationDto, None, None]:
        def generator():
            for platform in query["platforms"]:
                new_query = copy.deepcopy(query)
                new_query.pop("platforms")
                new_query["platform"] = platform
                yield self.get_champion_rotation(query=new_query)

        return generator()
