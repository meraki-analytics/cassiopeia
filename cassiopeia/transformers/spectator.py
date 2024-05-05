from copy import deepcopy
from typing import Type, TypeVar

from datapipelines import DataTransformer, PipelineContext

from ..core.spectator import (
    CurrentGameInfoData,
    CurrentMatch,
    FeaturedGamesData,
    FeaturedMatches,
)
from ..dto.spectator import CurrentGameInfoDto, FeaturedGamesDto

T = TypeVar("T")
F = TypeVar("F")


class SpectatorTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(
        self, target_type: Type[T], value: F, context: PipelineContext = None
    ) -> T:
        pass

    # Dto to Data

    @transform.register(CurrentGameInfoDto, CurrentGameInfoData)
    def current_game_dto_to_data(
        self, value: CurrentGameInfoDto, context: PipelineContext = None
    ) -> CurrentGameInfoData:
        return CurrentGameInfoData(**value)

    @transform.register(FeaturedGamesDto, FeaturedGamesData)
    def featured_games_dto_to_data(
        self, value: FeaturedGamesDto, context: PipelineContext = None
    ) -> FeaturedGamesData:
        data = deepcopy(value)
        data = data["gameList"]
        return FeaturedGamesData(
            [CurrentGameInfoData(**game) for game in data],
            region=value["region"],
        )

    # Data to Core

    # @transform.register(CurrentGameInfoData, CurrentMatch)
    def current_game_data_to_core(
        self, value: CurrentGameInfoData, context: PipelineContext = None
    ) -> CurrentMatch:
        from ..core.summoner import Summoner

        summoner = Summoner(
            puuid=value.teams[0].participants[0].puuid,
            id=value.teams[0].participants[0].summoner_id,
            region=value.region,
        )
        return CurrentMatch.from_data(value, summoner=summoner)

    # @transform.register(FeaturedGamesData, FeaturedMatches)
    def featured_games_data_to_core(
        self, value: FeaturedGamesData, context: PipelineContext = None
    ) -> FeaturedMatches:
        from ..core.summoner import Summoner

        matches = []
        for match in value:
            # TODO: What do we do here? Do we delete the name field? Do we need a puuid?
            summoner = Summoner(
                name=match.teams[0].participants[0].summoner_name,
                id=match.teams[0].participants[0].summoner_id,
                region=value.region,
            )
            match = CurrentMatch.from_data(match, summoner=summoner)
            matches.append(match)
        return FeaturedMatches.from_data(
            *matches,
            region=value.region,
            client_refresh_interval=value.clientRefreshInterval
        )
