from typing import Type, TypeVar, MutableMapping, Any, Iterable
import copy
import datetime

from datapipelines import DataSource, DataSink, PipelineContext, Query, NotFoundError

from ...data import Platform, Region
from ...dto.match import MatchDto, MatchListDto, TimelineDto
from .common import SimpleKVDiskService

T = TypeVar("T")


class MatchDiskService(SimpleKVDiskService):
    @DataSource.dispatch
    def get(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: MutableMapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    # Match

    _validate_get_match_query = Query. \
        has("gameId").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(MatchDto)
    def get_match(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchDto:
        MatchDiskService._validate_get_match_query(query, context)
        key = "{clsname}.{platform}.{id}".format(clsname=MatchDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["gameId"])
        return MatchDto(self._get(key))

    @put.register(MatchDto)
    def put_match(self, item: MatchDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=MatchDto.__name__,
                                                 platform=platform,
                                                 id=item["gameId"])
        self._put(key, item)

    # Match list

    # This is cool and useful functionality, but it really only works if we can pull the entire match
    # history in one go. For now, we just won't save the match history to disk at all.
    """
    _validate_get_match_list_query = Query. \
        has("account.id").as_(int).also. \
        has("platform").as_(Platform).also. \
        can_have("beginTime").as_(int).also. \
        can_have("endTime").as_(int).also. \
        can_have("beginIndex").with_default(0).also. \
        can_have("endIndex").with_default(50).also. \
        can_have("seasons").as_(Iterable).also. \
        can_have("champion.ids").as_(Iterable).also. \
        can_have("queues").as_(Iterable).also. \
        can_have("forceRefresh").with_default(False)

    @get.register(MatchListDto)
    def get_match_list(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> MatchListDto:
        MatchDiskService._validate_get_match_list_query(query, context)
        platform = query["platform"].value
        queues = "|".join(sorted({queue.value for queue in query.get("queues", {})}))
        seasons = "|".join(sorted({season.value for season in query.get("seasons", {})}))
        champions = "|".join(sorted({champion.value for champion in query.get("champion.ids", {})}))
        key = "{clsname}.{platform}.{account_id}.{queues}.{seasons}.{champions}".format(clsname=MatchListDto.__name__,
                                                                                        platform=platform,
                                                                                        account_id=query["account.id"],
                                                                                        queues=queues,
                                                                                        seasons=seasons,
                                                                                        champions=champions)
        data = self._get(key)

        # The above line will throw a NotFoundError if the matchlist for this summoner doesn't exist at all.
        # However, if it does exist, let's try to be smart about pulling the remaining data.
        most_recent = data["matches"][0]["timestamp"]
        # Choose 30 minutes to refresh match history
        refresh_from_expiration = datetime.datetime.fromtimestamp(most_recent/1000) < datetime.datetime.now() - datetime.timedelta(minutes=30)
        if query["forceRefresh"] or refresh_from_expiration:
            new_query = copy.deepcopy(query)
            new_query.pop("beginTime", None)
            new_query.pop("endTime", None)
            new_query.pop("beginIndex", None)
            new_query.pop("endIndex", None)
            new_query["beginTime"] = most_recent + 1  # Add 1 ms so we don't get the last game we have.
            new_data = context[context.Keys.PIPELINE].get(MatchListDto, query=new_query, context=context)
            data["matches"].extend(new_data["matches"])
        return MatchListDto(self._get(key))

    @put.register(MatchListDto)
    def put_match_list(self, item: MatchListDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        queues = "|".join(sorted({queue.value for queue in item["queue"]}))
        seasons = "|".join(sorted({season.value for season in item["season"]}))
        champions = "|".join(sorted({champion.value for champion in item["champion"]}))
        key = "{clsname}.{platform}.{account_id}.{queues}.{seasons}.{champions}".format(clsname=MatchListDto.__name__,
                                                                                        platform=platform,
                                                                                        account_id=item["accountId"],
                                                                                        queues=queues,
                                                                                        seasons=seasons,
                                                                                        champions=champions)
        self._put(key, item)
    """

    # Timeline

    _validate_get_timeline_query = Query. \
        has("matchId").as_(int).also. \
        has("platform").as_(Platform)

    @get.register(TimelineDto)
    def get_timeline(self, query: MutableMapping[str, Any], context: PipelineContext = None) -> TimelineDto:
        MatchDiskService._validate_get_timeline_query(query, context)
        key = "{clsname}.{platform}.{id}".format(clsname=TimelineDto.__name__,
                                                 platform=query["platform"].value,
                                                 id=query["matchId"])
        return TimelineDto(self._get(key))

    @put.register(TimelineDto)
    def put_timeline(self, item: TimelineDto, context: PipelineContext = None) -> None:
        platform = Region(item["region"]).platform.value
        key = "{clsname}.{platform}.{id}".format(clsname=TimelineDto.__name__,
                                                 platform=platform,
                                                 id=item["matchId"])
        self._put(key, item)
