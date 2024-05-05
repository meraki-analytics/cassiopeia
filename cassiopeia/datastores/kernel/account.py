from typing import Type, TypeVar, MutableMapping, Any, Iterable

from datapipelines import (
    DataSource,
    PipelineContext,
    Query,
    NotFoundError,
    validate_query,
)
from .common import KernelSource, APINotFoundError
from ...data import Platform
from ...dto.account import AccountDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


class AccountAPI(KernelSource):
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
        .also.has("platform")
        .as_(Platform)
    )

    @get.register(AccountDto)
    @validate_query(_validate_get_account_query, convert_region_to_platform)
    def get_account(
        self, query: MutableMapping[str, Any], context: PipelineContext = None
    ) -> AccountDto:
        parameters = {"platform": query["platform"].value}
        if "puuid" in query:
            puuid = query["puuid"]
            endpoint = f"riot/account/v1/accounts/by-puuid/{puuid}"
        elif "name" in query and "tagline" in query:
            game_name = query["name"].replace(" ", "%20")
            tagline = query["tagline"].replace(" ", "%20")
            endpoint = f"riot/account/v1/accounts/by-riot-id/{game_name}/{tagline}"
        else:
            RuntimeError("Impossible")

        try:
            data = self._get(endpoint=endpoint, parameters=parameters)
        except APINotFoundError as error:
            raise NotFoundError(str(error)) from error

        data["region"] = query["platform"].region.value
        return AccountDto(**data)
