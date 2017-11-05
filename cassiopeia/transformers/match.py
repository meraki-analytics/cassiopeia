from typing import Type, TypeVar
from copy import deepcopy

from datapipelines import DataTransformer, PipelineContext

from ..core.match import MatchData, MatchListData, MatchListGenerator, MatchReferenceData, TimelineData, Match, MatchHistory, Timeline
from ..dto.match import MatchDto, MatchListDto, MatchListDtoGenerator, MatchReferenceDto, TimelineDto

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

    @transform.register(MatchListDtoGenerator, MatchListGenerator)
    def matchlist_generator_dto_to_data(self, value: MatchListDtoGenerator, context: PipelineContext = None) -> MatchListGenerator:
        def match_dto_to_data_generator(generator):
            for matchrefdto in generator:
                yield self.match_reference_dto_to_data(matchrefdto)
        generator = match_dto_to_data_generator(value.pop("generator"))
        generator = MatchListGenerator(generator=generator, **value)
        generator._summoner = value._summoner  # Tack the summoner on to the generator... See notes in data -> core transformer
        return generator

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

    @transform.register(MatchListGenerator, MatchHistory)
    def matchlist_generator_to_matchhistory(self, value: MatchListGenerator, context: PipelineContext = None) -> MatchHistory:
        kwargs = {}
        try:
            kwargs["account_id"] = value.account_id
        except KeyError:
            pass
        try:
            kwargs["region"] = value.region
        except KeyError:
            pass
        try:
            kwargs["end_time"] = value.end_time
        except KeyError:
            pass
        try:
            kwargs["begin_time"] = value.begin_time
        except KeyError:
            pass
        try:
            kwargs["end_index"] = value.end_index
        except KeyError:
            pass
        try:
            kwargs["begin_index"] = value.begin_index
        except KeyError:
            pass
        try:
            kwargs["seasons"] = value.seasons
        except KeyError:
            pass
        try:
            kwargs["queues"] = value.queues
        except KeyError:
            pass
        try:
            kwargs["champions"] = value.champion_ids
        except KeyError:
            pass

        def match_generator(gen, summoner):
            for matchrefdata in gen:
                match = Match.from_match_reference(matchrefdata)
                # We have a summoner object (probably) already created, and if one was passed in then this is pretty crucial to:
                # Put the summoner object that this match history was instantiated with into the participant[0] so that searchable
                # list syntax on e.g. the name will work without loading the summoner.
                # For example:
                #    summoner = Summoner(name=name, account=account, id=id, region=region)
                #    match = summoner.match_history[0]
                #    p = match.participants[name]  # This will work without loading the summoner because the name was provided
                if summoner is not None:
                    match.participants[0].__class__.summoner.fget._lazy_set(match.participants[0], summoner)
                yield match
        generator = match_generator(value._generator, summoner=value._summoner)
        return MatchHistory.from_generator(generator=generator, **kwargs)
