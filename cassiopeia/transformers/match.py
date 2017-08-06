from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.match import MatchData, MatchListData, MatchReferenceData, TimelineData, Match, MatchHistory, Timeline
from ..dto.match import MatchDto, MatchListDto, MatchReferenceDto, TimelineDto

T = TypeVar("T")
F = TypeVar("F")


class MatchTransformer(DataTransformer):
    @DataTransformer.dispatch
    def transform(self, target_type: Type[T], value: F, context: PipelineContext = None) -> T:
        pass

    # TODO Integrate `forAccountId` into these transformers.
    # TODO Add all the optional fields to matchlist transformers.

    # Dto to Data

    @transform.register(MatchDto, MatchData)
    def match_dto_to_data(self, value: MatchDto, context: PipelineContext = None) -> MatchData:
        data = deepcopy(value)
        return MatchData.from_dto(data)

    @transform.register(MatchReferenceDto, MatchReferenceData)
    def match_reference_dto_to_data(self, value: MatchReferenceDto, context: PipelineContext = None) -> MatchReferenceData:
        data = deepcopy(value)
        return MatchReferenceData.from_dto(data)

    @transform.register(MatchListDto, MatchListData)
    def matchlist_dto_to_data(self, value: MatchListDto, context: PipelineContext = None) -> MatchListData:
        data = deepcopy(value)
        data = data["matches"]
        return MatchListData([self.match_reference_dto_to_data(match) for match in data], region=value["region"])

    @transform.register(TimelineDto, TimelineData)
    def timeline_dto_to_data(self, value: TimelineDto, context: PipelineContext = None) -> TimelineData:
        data = deepcopy(value)
        return TimelineData.from_dto(data)

    # Data to Core

    @transform.register(MatchData, Match)
    def match_data_to_core(self, value: MatchData, context: PipelineContext = None) -> Match:
        return Match.from_data(value)

    @transform.register(MatchReferenceData, Match)
    def match_reference_data_to_core(self, value: MatchReferenceData, context: PipelineContext = None) -> Match:
        return Match.from_match_reference(value)

    @transform.register(MatchListData, MatchHistory)
    def matchlist_data_to_core(self, value: MatchListData, context: PipelineContext = None) -> MatchHistory:
        return MatchHistory([Match.from_match_reference(ref) for ref in value], region=value.region)

    @transform.register(TimelineData, Timeline)
    def timeline_data_to_core(self, value: TimelineData, context: PipelineContext = None) -> Timeline:
        return Timeline.from_data(value)

    # Core to Dto

    @transform.register(Match, MatchDto)
    def match_core_to_dto(self, value: Match, context: PipelineContext = None) -> MatchDto:
        return value._data[MatchData]._dto

    @transform.register(MatchHistory, MatchListDto)
    def matchlist_core_to_dto(self, value: MatchHistory, context: PipelineContext = None) -> MatchListDto:
        return MatchListDto([self.match_core_to_dto(ref) for ref in value])  # It is very unlikely that this will work. Not going to debug it right now and just hope it isn't necessary / used.

    @transform.register(Timeline, TimelineDto)
    def timeline_core_to_dto(self, value: Timeline, context: PipelineContext = None) -> TimelineDto:
        return value._data[TimelineData]._dto
