from typing import Type, TypeVar, MutableMapping, Any, Iterable, Generator

from datapipelines import DataSource, PipelineContext, Query, NotFoundError, validate_query
from .common import RiotAPIService, APINotFoundError
from ...data import Platform, Region
from ...dto.thirdpartycode import VerificationStringDto
from ..uniquekeys import convert_region_to_platform

T = TypeVar("T")


def _get_default_locale(query: MutableMapping[str, Any], context: PipelineContext) -> str:
    return query["platform"].default_locale


class ThirdPartyCodeAPI(RiotAPIService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    #######################
    # Verification String #
    #######################

    _validate_get_verification_string_query = Query. \
        has("platform").as_(Platform).also. \
        has("summoner.id").as_(str)

    @get.register(VerificationStringDto)
    @validate_query(_validate_get_verification_string_query, convert_region_to_platform)
    def get_verification_string(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> VerificationStringDto:
        url = "https://{platform}.api.riotgames.com/lol/platform/v4/third-party-code/by-summoner/{summonerId}".format(platform=query["platform"].value.lower(), summonerId=query["summoner.id"])
        try:
            app_limiter, method_limiter = self._get_rate_limiter(query["platform"], "thirdpartycode")
            data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
        except (ValueError, APINotFoundError) as error:
            raise NotFoundError(str(error)) from error

        data = {"string": data}
        data["region"] = query["platform"].region.value
        data["summonerId"] = query["summoner.id"]
        return VerificationStringDto(data)

    _validate_get_many_verification_string_query = Query. \
        has("platforms").as_(Iterable).also. \
        has("summoner.ids").as_(Iterable)

    @get_many.register(VerificationStringDto)
    @validate_query(_validate_get_many_verification_string_query, convert_region_to_platform)
    def get_many_verification_string(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> Generator[VerificationStringDto, None, None]:
        def generator():
            for platform, summoner_id in zip(query["platforms"], query["summoner.ids"]):
                platform = Platform(platform.upper())
                url = "https://{platform}.api.riotgames.com/lol/platform/v4/third-party-code/by-summoner/{summonerId}".format(platform=platform.value.lower(), summonerId=summoner_id)
                try:
                    app_limiter, method_limiter = self._get_rate_limiter(query["platform"], "thirdpartycode")
                    data = self._get(url, {}, app_limiter=app_limiter, method_limiter=method_limiter)
                except APINotFoundError as error:
                    raise NotFoundError(str(error)) from error

                data = {"string": data}
                data["region"] = platform.region.value
                data["summonerId"] = summoner_id
                yield VerificationStringDto(data)

        return generator()
