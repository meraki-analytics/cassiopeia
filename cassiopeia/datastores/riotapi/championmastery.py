from typing import Type, TypeVar, Mapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Region, Platform
from ...dto.championmastery import ChampionMasteryDto, ChampionMasteryListDto, ChampionMasteryScoreDto

T = TypeVar("T")


class ChampionMasteryAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("playerId").as_(int).also. \
        has("championId").as_(int)

    @get.register(ChampionMasteryDto)
    def get_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMasteryDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_champion_mastery_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}/by-champion/{championId}".format(platform=query["platform"].value.lower(), summonerId=query["playerId"], championId=query["championId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId/by-champion/championId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["playerId"] = query["playerId"]
        return ChampionMasteryDto(data)

    _validate_get_many_champion_mastery_query = Query. \
        has("platform").as_(Platform).also. \
        has("playerId").as_(int).also. \
        has("championIds").as_(Iterable)

    @get_many.register(ChampionMasteryDto)
    def get_many_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_many_champion_mastery_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["playerId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
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

                mastery["playerId"] = query["playerId"]
                mastery["region"] = query["platform"].region.value
                yield ChampionMasteryDto(mastery)

        return generator()

    _validate_get_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("playerId").as_(int)

    @get.register(ChampionMasteryListDto)
    def get_champion_mastery_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMasteryListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_champion_mastery_list_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["playerId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return ChampionMasteryListDto({
            "masteries": data,
            "playerId": query["playerId"],
            "region": query["platform"].region.value
        })

    _validate_get_many_champion_mastery_list_query = Query. \
        has("platform").as_(Platform).also. \
        has("playerIds").as_(Iterable)

    @get_many.register(ChampionMasteryListDto)
    def get_many_champion_mastery_list(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_many_champion_mastery_list_query(query, context)

        def generator():
            for summoner_id in query["playerIds"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/champion-masteries/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=summoner_id)
                try:
                    data = self._get(url, {}, self._rate_limiter(query["platform"], "champion-masteries/by-summoner/summonerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield ChampionMasteryListDto({
                    "masteries": data,
                    "playerId": summoner_id,
                    "region": query["platform"].region.value
                })

        return generator()

    _validate_get_champion_mastery_score_query = Query. \
        has("platform").as_(Platform).also. \
        has("playerId").as_(int)

    @get.register(ChampionMasteryScoreDto)
    def get_champion_mastery_score(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMasteryScoreDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_champion_mastery_score_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/{playerId}".format(platform=query["platform"].value.lower(), playerId=query["playerId"])
        try:
            data = self._get(url, {}, self._rate_limiter(query["platform"], "scores/by-summoner/playerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        return ChampionMasteryScoreDto({
            "region": query["platform"].region.value,
            "playerId": query["playerId"],
            "score": data
        })

    _validate_get_many_champion_mastery_score = Query. \
        has("platform").as_(Platform).also. \
        has("playerIds").as_(Iterable)

    @get_many.register(ChampionMasteryScoreDto)
    def get_many_champion_mastery_score(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteryScoreDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        ChampionMasteryAPI._validate_get_many_champion_mastery_score(query, context)

        def generator():
            for player_id in query["playerIds"]:
                url = "https://{platform}.api.riotgames.com/lol/champion-mastery/v3/scores/by-summoner/{playerId}".format(platform=query["platform"].value.lower(), playerId=player_id)
                try:
                    data = self._get(url, {}, self._rate_limiter(query["platform"], "scores/by-summoner/playerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                yield ChampionMasteryScoreDto({
                    "region": query["platform"].region.value,
                    "playerId": player_id,
                    "score": data
                })

        return generator()
