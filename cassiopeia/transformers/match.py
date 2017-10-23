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

    @transform.register(TimelineData, Timeline)
    def timeline_data_to_core(self, value: TimelineData, context: PipelineContext = None) -> Timeline:
        return Timeline.from_data(value)
