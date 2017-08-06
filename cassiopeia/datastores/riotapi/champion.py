from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.champion import ChampionDto, ChampionListDto

T = TypeVar("T")


class ChampionAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_status_query = Query. \
        has("id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(ChampionDto)
    def get_champion_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionDto:
        ChampionAPI._validate_get_champion_status_query(query, context)

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
    def get_many_champion_status(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionDto, None, None]:
        ChampionAPI._validate_get_many_champion_status_query(query, context)

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
    def get_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionListDto:
        ChampionAPI._validate_get_champion_status_list_query(query, context)

        params = {
            "freeToPlay": query["freeToPlay"]
        }

        url = "https://{platform}.api.riotgames.com/lol/platform/v3/champions".format(platform=query["platform"].value.lower())
        try:
            data = self._get(url, params, self._get_rate_limiter(query["platform"], "champions"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["freeToPlay"] = query["freeToPlay"]
        return ChampionListDto(data)

    _validate_get_many_champion_status_list_query = Query. \
        has("platforms").as_(Iterable).also. \
        can_have("freeToPlay").with_default(False)

    @get_many.register(ChampionListDto)
    def get_many_champion_status_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionListDto, None, None]:
        ChampionAPI._validate_get_many_champion_status_list_query(query, context)

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
