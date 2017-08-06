from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform
from ...dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto, ChampionMasteryScoreDto
from ...dto.summoner import SummonerDto
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
        has("summoner.id").as_(int).or_("summoner.account.id").as_(int).or_("summoner.name").as_(str).also. \
        has("champion.id").as_(int).or_("champion.name").as_(str)

    @get.register(ChampionMasteryDto)
    @validate_query(_validate_get_champion_mastery_query, convert_region_to_platform)
    def get_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryDto:
        # TODO Is this still what we want to do?
        if "summoner.id" not in query:
            for k in ["summoner.account.id", "summoner.account_id", "summoner.accountId"]:
                if k in query:
                    summoner_query = {"platform": query["platform"], "account.id": query[k]}
                    break
            for k in ["summoner.name", "summoner_name", "summonerName"]:
                if k in query:
                    summoner_query = {"platform": query["platform"], "name": query[k]}
                    break
            summoner_dto = context[PipelineContext.Keys.PIPELINE].get(SummonerDto, query=summoner_query)
            query["summoner.id"] = summoner_dto["id"]

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"], championId=query["champion.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId/by-champion/championId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return ChampionMasteryDto(data)

    _validate_get_many_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("summonerId").as_(int).also. \
        has("championIds").as_(Iterable)

    @get_many.register(ChampionMasteryDto)
    def get_many_champion_mastery(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryDto, None, None]:
        ChampionMasteryAPI._validate_get_many_champion_mastery_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summonerId"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
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
        has("summoner.id").as_(int)

    @get.register(ChampionMasteryListDto)
    def get_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryListDto:
        ChampionMasteryAPI._validate_get_champion_mastery_list_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return ChampionMasteryListDto({
            "masteries": data,
            "summonerId": query["summoner.id"],
            "region": query["platform"].region.value
        })

    _validate_get_many_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.ids").as_(Iterable)

    @get_many.register(ChampionMasteryListDto)
    def get_many_champion_mastery_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryListDto, None, None]:
        ChampionMasteryAPI._validate_get_many_champion_mastery_list_query(query, context)

        def generator():
            for summoner_id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=summoner_id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
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
        has("summoner.id").as_(int)

    @get.register(ChampionMasteryScoreDto)
    def get_champion_mastery_score(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChampionMasteryScoreDto:
        ChampionMasteryAPI._validate_get_champion_mastery_score_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "scores/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return ChampionMasteryScoreDto({
            "region": query["platform"].region.value,
            "summonerId": query["summoner.id"],
            "score": data
        })

    _validate_get_many_champion_mastery_score = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.ids").as_(Iterable)

    @get_many.register(ChampionMasteryScoreDto)
    def get_many_champion_mastery_score(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryScoreDto, None, None]:
        ChampionMasteryAPI._validate_get_many_champion_mastery_score(query, context)

        def generator():
            for summoner_id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=summoner_id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "scores/by-summoner/summonerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield ChampionMasteryScoreDto({
                    "region": query["platform"].region.value,
                    "summonerId": summoner_id,
                    "score": data
                })

        return generator()
