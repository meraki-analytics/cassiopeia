from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region, Queue
from ...dto.league import LeaguesListDto, ChallengerLeagueListDto, MasterLeagueListDto

T = TypeVar("T")


class LeaguesAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    _validate_get_leagues_query = Query. \
        has("summoner.id").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(LeaguesListDto)
    def get_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeaguesListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_leagues_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/league/v3/leagues/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "leagues/by-summoner/summonerId"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data = {"leagues": data}
        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return LeaguesListDto(data)

    _validate_get_many_leagues_query = Query. \
        has("summoner.ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(LeaguesListDto)
    def get_leagues(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[LeaguesListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_many_leagues_query(query, context)

        def generator():
            for id in query["summoner.ids"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v3/leagues/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=id)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "leagues/by-summoner/summonerId"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["summonerId"] = id
                yield LeaguesListDto(data)

        return generator()


    _validate_get_challenger_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    @get.register(ChallengerLeagueListDto)
    def get_challenger_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeagueListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_challenger_league_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=query["queue"].value)
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "challengerleagues/by-queue"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["queue"] = query["queue"].value
        return ChallengerLeagueListDto(data)

    _validate_get_many_challenger_league_query = Query. \
        has("queues").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(ChallengerLeagueListDto)
    def get_challenger_leagues(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChallengerLeagueListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_many_master_league_query(query, context)

        def generator():
            for queue in query["queues"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v3/challengerleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=queue.value)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "challengerleagues/by-queue"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["queue"] = queue.value
                yield ChallengerLeagueListDto(data)

        return generator()


    _validate_get_master_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    @get.register(MasterLeagueListDto)
    def get_master_league(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeagueListDto:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_master_league_query(query, context)

        url = "https://{platform}.api.riotgames.com/lol/league/v3/masterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=query["queue"].value)
        try:
            data = self._get(url, {}, self._get_rate_limiter(query["platform"], "masterleagues/by-queue"))
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["queue"] = query["queue"].value
        return MasterLeagueListDto(data)

    _validate_get_many_master_league_query = Query. \
        has("queues").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(MasterLeagueListDto)
    def get_master_leagues(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MasterLeagueListDto, None, None]:
        if "region" in query and "platform" not in query:
            query["platform"] = Region(query["region"]).platform.value
        LeaguesAPI._validate_get_many_master_league_query(query, context)

        def generator():
            for queue in query["queues"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v3/masterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=queue.value)
                try:
                    data = self._get(url, {}, self._get_rate_limiter(query["platform"], "masterleagues/by-queue"))
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["queue"] = queue.value
                yield MasterLeagueListDto(data)

        return generator()
