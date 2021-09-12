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
        return MatchData(**value)

    @transform.register(MatchReferenceDto, MatchReferenceData)
    def match_reference_dto_to_data(self, value: MatchReferenceDto, context: PipelineContext = None) -> MatchReferenceData:
        return MatchReferenceData(**value)

    @transform.register(MatchListDto, MatchListData)
    def matchlist_dto_to_data(self, value: MatchListDto, context: PipelineContext = None) -> MatchListData:
        kwargs = {
            "continent": value["continent"],
            "puuid": value["puuid"],
            "type": value["type"],
            "queue": value["queue"],
        }
        if "beginIndex" in value:
            kwargs["beginIndex"] = value["beginIndex"]
            kwargs["endIndex"] = value["endIndex"]
            kwargs["maxNumberOfMatches"] = value.get("maxNumberOfMatches", None),
        if "beginTime" in value:
            kwargs["beginTime"] = value["beginTime"]
            kwargs["endTime"] = value["endTime"]
        return MatchListData([self.match_reference_dto_to_data({"id": id, "continent": value["continent"]}) for id in value["match_ids"]], **kwargs)

    @transform.register(TimelineDto, TimelineData)
    def timeline_dto_to_data(self, value: TimelineDto, context: PipelineContext = None) -> TimelineData:
        return TimelineData(**value)

    # Data to Core

    #@transform.register(MatchData, Match)
    def match_data_to_core(self, value: MatchData, context: PipelineContext = None) -> Match:
        return Match.from_data(value)

    #@transform.register(MatchReferenceData, Match)
    def match_reference_data_to_core(self, value: MatchReferenceData, context: PipelineContext = None) -> Match:
        return Match.from_match_reference(value)

    #@transform.register(TimelineData, Timeline)
    def timeline_data_to_core(self, value: TimelineData, context: PipelineContext = None) -> Timeline:
        return Timeline.from_data(value)
