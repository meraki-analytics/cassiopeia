from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Queue, Tier, Division
from ...dto.league import LeagueEntriesDto, LeagueDto, LeagueSummonerEntriesDto, ChallengerLeagueListDto, MasterLeagueListDto, GrandmasterLeagueListDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class LeaguesAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    # League Entries

    _validate_get_league_entries_query = Query. \
        has("queue").as_(Queue).also. \
        has("tier").as_(Tier).also. \
        has("division").as_(Division).also. \
        has("page").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(LeagueEntriesDto)
    @validate_query(_validate_get_league_entries_query, convert_region_to_platform)
    def get_league_entries_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueEntriesDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/entries/{queue}/{tier}/{division}".format(
            platform=query["platform"].value.lower(),
            queue=query["queue"].value,
            tier=query["tier"].value,
            division=query["division"].value
        )
        try:
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], "leagues/paginated-entries")
            data = self._get(url, parameters={"page": query["page"]}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError:
            data = []
        region = query["platform"].region.value
        for entry in data:
            entry["region"] = region
        return LeagueEntriesDto(entries=data, page=query["page"], region=query["region"].value, queue=query["queue"].value, tier=query["tier"].value, division=query["division"].value)


    _validate_get_league_summoner_entries_query = Query. \
        has("summoner.id").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(LeagueSummonerEntriesDto)
    @validate_query(_validate_get_league_summoner_entries_query, convert_region_to_platform)
    def get_league_summoner_entries_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueSummonerEntriesDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/entries/by-summoner/{id}".format(
            platform=query["platform"].value.lower(),
            id=query["summoner.id"]
        )
        try:
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], "leagues/summoner-entries")
            data = self._get(url, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError:
            data = []
        region = query["platform"].region.value
        for entry in data:
            entry["region"] = region
        return LeagueSummonerEntriesDto(entries=data, region=region, summonerId=query["summoner.id"])

    # Leagues

    _validate_get_league_query = Query. \
        has("id").as_(str).also. \
        has("platform").as_(Platform)

    @get.register(LeagueDto)
    @validate_query(_validate_get_league_query, convert_region_to_platform)
    def get_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> LeagueDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/leagues/{leagueId}".format(platform=query["platform"].value.lower(), leagueId=query["id"])
        try:
            endpoint = "leagues/leagueId {}".format(query["platform"].value)
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        for entry in data["entries"]:
            entry["region"] = data["region"]
            entry["tier"] = data["tier"]
        return LeagueDto(data)

    _validate_get_many_league_query = Query. \
        has("ids").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(LeagueDto)
    @validate_query(_validate_get_many_league_query, convert_region_to_platform)
    def get_many_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[LeagueDto, None, None]:
        def generator():
            for id in query["ids"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v4/leagues/{leagueId}".format(platform=query["platform"].value.lower(), leagueId=id)
                try:
                    endpoint = "leagues/leagueId {}".format(query["platform"].value)
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                for league in data["leagues"]:
                    league["region"] = data["region"]
                    for entry in league["entries"]:
                        entry["region"] = data["region"]
                yield LeagueDto(data)

        return generator()

    _validate_get_challenger_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    @get.register(ChallengerLeagueListDto)
    @validate_query(_validate_get_challenger_league_query, convert_region_to_platform)
    def get_challenger_league_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> ChallengerLeagueListDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=query["queue"].value)
        try:
            endpoint = "challengerleagues/by-queue {}".format(query["platform"].value)
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["queue"] = query["queue"].value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return ChallengerLeagueListDto(data)

    _validate_get_many_challenger_league_query = Query. \
        has("queues").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(ChallengerLeagueListDto)
    @validate_query(_validate_get_many_challenger_league_query, convert_region_to_platform)
    def get_many_challenger_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[ChallengerLeagueListDto, None, None]:
        def generator():
            for queue in query["queues"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=queue.value)
                try:
                    endpoint = "challengerleagues/by-queue {}".format(query["platform"].value)
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["queue"] = queue.value
                for entry in data["entries"]:
                    entry["region"] = data["region"]
                yield ChallengerLeagueListDto(data)

        return generator()

    _validate_get_grandmaster_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    @get.register(GrandmasterLeagueListDto)
    @validate_query(_validate_get_grandmaster_league_query, convert_region_to_platform)
    def get_grandmaster_league_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> GrandmasterLeagueListDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=query["queue"].value)
        try:
            endpoint = "grandmasterleagues/by-queue {}".format(query["platform"].value)
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["queue"] = query["queue"].value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return GrandmasterLeagueListDto(data)

    _validate_get_many_grandmaster_league_query = Query. \
        has("queues").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(GrandmasterLeagueListDto)
    @validate_query(_validate_get_many_grandmaster_league_query, convert_region_to_platform)
    def get_many_grandmaster_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[GrandmasterLeagueListDto, None, None]:
        def generator():
            for queue in query["queues"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v4/grandmasterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=queue.value)
                try:
                    endpoint = "grandmasterleagues/by-queue {}".format(query["platform"].value)
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["queue"] = queue.value
                for entry in data["entries"]:
                    entry["region"] = data["region"]
                yield GrandmasterLeagueListDto(data)

        return generator()

    _validate_get_master_league_query = Query. \
        has("queue").as_(Queue).also. \
        has("platform").as_(Platform)

    @get.register(MasterLeagueListDto)
    @validate_query(_validate_get_master_league_query, convert_region_to_platform)
    def get_master_league_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MasterLeagueListDto:
        url = "https://{platform}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=query["queue"].value)
        try:
            endpoint = "masterleagues/by-queue {}".format(query["platform"].value)
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        data["queue"] = query["queue"].value
        for entry in data["entries"]:
            entry["region"] = data["region"]
        return MasterLeagueListDto(data)

    _validate_get_many_master_league_query = Query. \
        has("queues").as_(Iterable).also. \
        has("platform").as_(Platform)

    @get_many.register(MasterLeagueListDto)
    @validate_query(_validate_get_many_master_league_query, convert_region_to_platform)
    def get_many_master_leagues_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[MasterLeagueListDto, None, None]:
        def generator():
            for queue in query["queues"]:
                url = "https://{platform}.api.riotgames.com/lol/league/v4/masterleagues/by-queue/{queueName}".format(platform=query["platform"].value.lower(), queueName=queue.value)
                try:
                    endpoint = "masterleagues/by-queue {}".format(query["platform"].value)
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], endpoint)
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"leagues": data}
                data["region"] = query["platform"].region.value
                data["queue"] = queue.value
                for entry in data["entries"]:
                    entry["region"] = data["region"]
                yield MasterLeagueListDto(data)

        return generator()
