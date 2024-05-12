from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import (
    DataSource,
    PipelineContext,
    Query,
    NotFoundError,
    validate_query,
)
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Continent
from ...dto.account import AccountDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class AccountAPI(RiotAPIService):
    @DataSource.dispatch
    def get(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> T:
        pass

    @DataSource.dispatch
    def get_many(
        self,
        type: Type[T],
        query: MutableMapping[str, Any],
        context: PipelineContext = None,
    ) -> Iterable[T]:
        pass

    _validate_get_account_query = (
        Query.has("puuid")
        .as_(str)
        .or_("name")
        .as_(str)
        .or_("tagline")
        .as_(str)
        .or_("name")
        .as_(str)
        .also.has("platform")
        .as_(Platform)
    )

    @get.register(AccountDto)
    @validate_query(_validate_get_account_query, convert_region_to_platform)
    def get_account(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> AccountDto:
        platform: Platform = query["platform"]
        continent = platform.continent
        # For some reason, Riot routes the SEA region/continent to ASIA for this endpoint.
        if continent == Continent.sea:
            continent = Continent.asia
        if "puuid" in query:
            puuid = query["puuid"]
            url = "https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}".format(
                continent=continent.value.lower(), puuid=puuid
            )
            endpoint = "accounts/puuid"
        elif "name" in query and "tagline" in query:
            game_name = query["name"].replace(" ", "%20")
            tagline = query["tagline"].replace(" ", "%20")
            url = "https://{continent}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}".format(
                continent=continent.value.lower(),
                game_name=game_name,
                tagline=tagline,
            )
            endpoint = "accounts/name"
        else:
            endpoint = ""

        try:
            app_limiter, method_limiter = self._get_rate_limiter(
                query["platform"], endpoint
            )
            data = self._get(
                url, {}, app_limiter=app_limiter, method_limiter=method_limiter
            )
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return AccountDto(**data)
