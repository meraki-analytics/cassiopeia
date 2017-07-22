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

    # Data

    @transform.register(MatchDto, MatchData)
    def match_dto_to_data(self, value: MatchDto, context: PipelineContext = None) -> MatchData:
        data = deepcopy(value)
        return MatchData(data)

    @transform.register(MatchReferenceDto, MatchReferenceData)
    def match_reference_dto_to_data(self, value: MatchReferenceDto, context: PipelineContext = None) -> MatchReferenceData:
        data = deepcopy(value)
        return MatchReferenceData(data)

    @transform.register(MatchListDto, MatchListData)
    def matchlist_dto_to_data(self, value: MatchListDto, context: PipelineContext = None) -> MatchListData:
        data = deepcopy(value)
        data = data["matches"]
        return MatchListData([self.match_reference_dto_to_data(match) for match in data])

    @transform.register(TimelineDto, TimelineData)
    def timeline_dto_to_data(self, value: TimelineDto, context: PipelineContext = None) -> TimelineData:
        data = deepcopy(value)
        return TimelineData(data)

    # Core

    @transform.register(MatchData, Match)
    def match_data_to_core(self, value: Match, context: PipelineContext = None) -> Match:
        return Match(value)

    @transform.register(MatchListData, MatchHistory)
    def matchlist_data_to_core(self, value: MatchListData, context: PipelineContext = None) -> MatchHistory:
        return MatchHistory([Match.from_match_reference(ref) for ref in value])

    @transform.register(TimelineData, Timeline)
    def timeline_data_to_core(self, value: TimelineData, context: PipelineContext = None) -> Timeline:
        return Timeline(value)
