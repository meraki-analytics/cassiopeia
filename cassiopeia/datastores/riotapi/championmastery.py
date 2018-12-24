from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto, ChampionMasteryScoreDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class ChampionMasteryAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str).also. \
        has("champion.id").as_(int)

    @get.register(ChampionMasteryDto)
    @validate_query(_validate_get_champion_mastery_query, convert_region_to_platform)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryDto:
        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"], championId=query["champion.id"])
        try:
            endpoint = "champion-masteries/by-summoner/summonerId/by-champion/championId"
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return ChampionMasteryDto(data)

    _validate_get_many_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summonerId").as_(str).also. \
        has("championIds").as_(Iterable)

    @get_many.register(ChampionMasteryDto)
    @validate_query(_validate_get_many_champion_mastery_query, convert_region_to_platform)
    def get_many_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryDto, None, None]:
        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summonerId"])
        try:
            endpoint = "champion-masteries/by-summoner/summonerId"
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        masteries = {
            mastery["championId"]: mastery for mastery in data
        }

        def generator():
            for id in query["championIds"]:
                try:
                    mastery = masteries[id]
                except KeyError as error:
                    raise NotFoundError("Summoner has no mastery on champion with id \"{id}\"".format(id=id)) from error

                mastery["summonerId"] = query["summonerId"]
                mastery["region"] = query["platform"].region.value
                yield ChampionMasteryDto(mastery)

        return generator()

    _validate_get_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str)

    @get.register(ChampionMasteryListDto)
    @validate_query(_validate_get_champion_mastery_list_query, convert_region_to_platform)
    def get_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryListDto:
        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            endpoint = "champion-masteries/by-summoner/summonerId"
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        for cm in data:
            cm["region"] = query["region"]
        return ChampionMasteryListDto({
            "masteries": data,
            "summonerId": query["summoner.id"],
            "region": query["platform"].region.value
        })

    _validate_get_many_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.ids").as_(Iterable)

    @get_many.register(ChampionMasteryListDto)
    @validate_query(_validate_get_many_champion_mastery_list_query, convert_region_to_platform)
    def get_many_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryListDto, None, None]:
        def generator():
            for summoner_id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=summoner_id)
                try:
                    endpoint = "champion-masteries/by-summoner/summonerId"
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield ChampionMasteryListDto({
                    "masteries": data,
                    "summonerId": summoner_id,
                    "region": query["platform"].region.value
                })

        return generator()

    _validate_get_champion_mastery_score_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str)

    @get.register(ChampionMasteryScoreDto)
    @validate_query(_validate_get_champion_mastery_score_query, convert_region_to_platform)
    def get_champion_mastery_score(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryScoreDto:
        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            endpoint = "scores/by-summoner/summonerId"
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return ChampionMasteryScoreDto({
            "region": query["platform"].region.value,
            "summonerId": query["summoner.id"],
            "score": data
        })

    _validate_get_many_champion_mastery_score_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.ids").as_(Iterable)

    @get_many.register(ChampionMasteryScoreDto)
    @validate_query(_validate_get_many_champion_mastery_score_query, convert_region_to_platform)
    def get_many_champion_mastery_score(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryScoreDto, None, None]:
        def generator():
            for summoner_id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v4/scores/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=summoner_id)
                try:
                    endpoint = "scores/by-summoner/summonerId"
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield ChampionMasteryScoreDto({
                    "region": query["platform"].region.value,
                    "summonerId": summoner_id,
                    "score": data
                })

        return generator()
