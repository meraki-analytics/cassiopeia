import copy
from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.champion import ChampionDto, ChampionListDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class ChampionAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_status_query = Query. \
        has("id").as_(int).or_("name").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(ChampionDto)
    @validate_query(_validate_get_champion_status_query, convert_region_to_platform)
    def get_champion_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        if self._request_by_id or "id" not in query:  # Get by champion status list
            champions_query = copy.deepcopy(query)
            champions = context[context.Keys.PIPELINE].get(ChampionListDto, query=champions_query)

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
            return ChampionDto(champion)
        else:
            url = "https://{platform}.api.riotgames.com/lol/platform/v3/champions/{id}".format(platform=query["platform"].value.lower(), id=query["id"])
            try:
                data = self._get(url, {}, self._get_rate_limiter(query["platform"], "champions/id"))
            except APINotFoundError as error:
                raise NotFoundError(str(error)) from error

            data["region"] = query["platform"].region.value
            return ChampionDto(**data)

    _validate_get_many_champion_status_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(ChampionDto)
    @validate_query(_validate_get_many_champion_status_query, convert_region_to_platform)
    def get_many_champion_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionDto, None, None]:
        params = {
            "freeToPlay": False
        }

        url = "https://{platform}.api.riotgames.com/lol/platform/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "champions"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        statuses = {
            status["id"]: status for status in data["champions"]
        }

        def generator():
            for id in query["ids"]:
                try:
                    status = statuses[id]
                except KeyError as error:
                    raise NotFoundError("No champion exists with id \"{id}\"".format(id=id)) from error

                status["region"] = query["platform"].region.value
                yield ChampionDto(**status)

        return generator()

    _validate_get_champion_status_list_query = Query. \
        has("platform").as_(Platform).also. \
        can_have("freeToPlay").with_default(False)

    @get.register(ChampionListDto)
    @validate_query(_validate_get_champion_status_list_query, convert_region_to_platform)
    def get_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        params = {
            "freeToPlay": query["freeToPlay"]
        }

        url = "https://{platform}.api.riotgames.com/lol/platform/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "champions"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for c in data["champions"]:
            c["region"] = data["region"]
        data["freeToPlay"] = query["freeToPlay"]
        return ChampionListDto(data)

    _validate_get_many_champion_status_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("freeToPlay").with_default(False)

    @get_many.register(ChampionListDto)
    @validate_query(_validate_get_many_champion_status_list_query, convert_region_to_platform)
    def get_many_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionListDto, None, None]:
        params = {
            "freeToPlay": query["freeToPlay"]
        }

        def generator():
            for platform in query["platforms"]:
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/platform/v3/champions".format(platform=platform.value.lower())
                try:
                    data = self._get(url, params, self._get_rate_limiter(platform, "champions"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data["region"] = platform.region.value
                data["freeToPlay"] = query["freeToPlay"]
                yield ChampionListDto(data)

        return generator()
