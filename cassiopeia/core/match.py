import functools
import arrow
import datetime
from collections import Counter
from typing import List, Dict, Set, Union, Generator

from datapipelines import NotFoundError
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableLazyList, SearchableDictionary

from .. import configuration
from .staticdata import Versions
from ..data import Region, Platform, Tier, GameType, GameMode, Queue, Side, Season, Lane, Role, Key, SummonersRiftArea, Tower
from .common import CoreData, CoreDataList, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, provide_default_region, ghost_load_on
from ..dto import match as dto
from .patch import Patch
from .summoner import Summoner
from .staticdata.champion import Champion
from .staticdata.rune import Rune
from .staticdata.summonerspell import SummonerSpell
from .staticdata.item import Item
from .staticdata.map import Map


def load_match_on_attributeerror(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except AttributeError:  # teamId
            # The match has only partially loaded this participant and it doesn't have all it's data, so load the full match
            match = getattr(self, "_{}__match".format(self.__class__.__name__))
            if not match._Ghost__is_loaded(MatchData):
                match.__load__(MatchData)
                match._Ghost__set_loaded(MatchData)
            if isinstance(self, Participant):
                old_participant = self
            elif isinstance(self, ParticipantStats):
                old_participant = getattr(self, "_{}__participant".format(self.__class__.__name__))
            else:
                raise RuntimeError("Impossible!")
            for participant in match.participants:
                if participant.summoner.name == old_participant.summoner.name:
                    if isinstance(self, Participant):
                        self._data[ParticipantData] = participant._data[ParticipantData]
                    elif isinstance(self, ParticipantStats):
                        self._data[ParticipantStatsData] = participant.stats._data[ParticipantStatsData]
                    return method(self, *args, **kwargs)
        return method(self, *args, **kwargs)
    return wrapper


_staticdata_to_version_mapping = {}
def _choose_staticdata_version(match):
    # If we want to pull the data for the correct version, we need to pull the entire match data.
    # However, we can use the creation date (which comes with a matchref) and get the ~ patch and therefore extract the version from the patch.
    if configuration.settings.version_from_match is None or configuration.settings.version_from_match == "latest":
        return None  # Rather than pick the latest version here, let the obj handle it so it knows which endpoint within the realms data to use

    if configuration.settings.version_from_match == "version" or hasattr(match._data[MatchData], "version"):
        majorminor = match.patch.major + "." + match.patch.minor
    elif configuration.settings.version_from_match == "patch":
        patch = Patch.from_date(match.creation, region=match.region)
        majorminor = patch.majorminor
    else:
        raise ValueError("Unknown value for setting `version_from_match`:", configuration.settings.version_from_match)

    try:
        version = _staticdata_to_version_mapping[majorminor]
    except KeyError:
        if int(match.patch.major) >= 10:
            versions = Versions(region=match.region)
            # use the first major.minor.x matching occurrence from the versions list
            version = next(x for x in versions if ".".join(x.split(".")[:2]) == majorminor)
        else:
            version = majorminor + ".1"  # use major.minor.1
        _staticdata_to_version_mapping[majorminor] = version
    return version

##############
# Data Types #
##############


class MatchListData(CoreDataList):
    _dto_type = dto.MatchListDto
    _renamed = {"champion": "championIds", "queue": "queues", "season": "seasons"}


class PositionData(CoreData):
    _renamed = {}


class EventData(CoreData):
    _renamed = {"eventType": "type", "teamId": "side", "pointCaptured": "capturedPoint", "assistingParticipantIds": "assistingParticipants", "skillSlot": "skill"}

    def __call__(self, **kwargs):
        if "position" in kwargs:
            self.position = PositionData(**kwargs.pop("position"))
        super().__call__(**kwargs)
        return self


class ParticipantFrameData(CoreData):
    _renamed = {"totalGold": "goldEarned", "minionsKilled": "creepScore", "xp": "experience", "jungleMinionsKilled": "neutralMinionsKilled"}

    def __call__(self, **kwargs):
        if "position" in kwargs:
            self.position = PositionData(**kwargs.pop("position"))
        super().__call__(**kwargs)
        return self


class FrameData(CoreData):
    _renamed = {}

    def __call__(self, **kwargs):
        if "events" in kwargs:
            self.events = [EventData(**event) for event in kwargs.pop("events")]
        if "participantFrames" in kwargs:
            self.participantFrames = {int(key): ParticipantFrameData(**pframe) for key, pframe in kwargs.pop("participantFrames").items()}
        super().__call__(**kwargs)
        return self


class TimelineData(CoreData):
    _dto_type = dto.TimelineDto
    _renamed = {"matchId": "id", "frameInterval": "frame_interval"}

    def __call__(self, **kwargs):
        if "frames" in kwargs:
            self.frames = [FrameData(**frame) for frame in kwargs.pop("frames")]
        super().__call__(**kwargs)
        return self


class ParticipantTimelineData(CoreData):
    _renamed = {"participantId": "id"}

    def __call__(self, **kwargs):
        #timeline.setCreepScore(getStatTotals(item.getCreepsPerMinDeltas(), durationInSeconds));
        #timeline.setCreepScoreDifference(getStatTotals(item.getCsDiffPerMinDeltas(), durationInSeconds));
        #timeline.setDamageTaken(getStatTotals(item.getDamageTakenPerMinDeltas(), durationInSeconds));
        #timeline.setDamageTakenDifference(getStatTotals(item.getDamageTakenDiffPerMinDeltas(), durationInSeconds));
        #timeline.setExperience(getStatTotals(item.getXpPerMinDeltas(), durationInSeconds));
        #timeline.setExperienceDifference(getStatTotals(item.getXpDiffPerMinDeltas(), durationInSeconds));
        super().__call__(**kwargs)
        return self


class ParticipantStatsData(CoreData):
    _renamed = {}


class ParticipantData(CoreData):
    _renamed = {"participantId": "id", "spell1Id": "summonerSpellDId", "spell2Id": "summonerSpellFId", "highestAchievedSeasonTier": "rankLastSeason", "bot": "isBot", "profileIcon": "profileIconId"}

    def __call__(self, **kwargs):
        if "stats" in kwargs:
            stats = kwargs.pop("stats")
            if "perk0" in stats:  # Assume all the rest are too
                self.runes = {
                    stats.pop("perk0"): [stats.pop("perk0Var1"), stats.pop("perk0Var2"), stats.pop("perk0Var3")],
                    stats.pop("perk1"): [stats.pop("perk1Var1"), stats.pop("perk1Var2"), stats.pop("perk1Var3")],
                    stats.pop("perk2"): [stats.pop("perk2Var1"), stats.pop("perk2Var2"), stats.pop("perk2Var3")],
                    stats.pop("perk3"): [stats.pop("perk3Var1"), stats.pop("perk3Var2"), stats.pop("perk3Var3")],
                    stats.pop("perk4"): [stats.pop("perk4Var1"), stats.pop("perk4Var2"), stats.pop("perk4Var3")],
                    stats.pop("perk5"): [stats.pop("perk5Var1"), stats.pop("perk5Var2"), stats.pop("perk5Var3")],
                }
                self.stat_runes = [
                    stats.pop("statPerk0", None),
                    stats.pop("statPerk1", None),
                    stats.pop("statPerk2", None),
                ]
                stats.pop("runes", None)
            self.stats = ParticipantStatsData(**stats)
        if "timeline" in kwargs:
            self.timeline = ParticipantTimelineData(**kwargs.pop("timeline"))
        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))

        if "player" in kwargs:
            for key, value in kwargs.pop("player").items():
                kwargs[key] = value
        super().__call__(**kwargs)
        return self


class TeamData(CoreData):
    _renamed = {"dominionVictoryScore": "dominionScore", "firstBaron": "firstBaronKiller", "firstBlood": "firstBloodKiller", "firstDragon": "firstDragonKiller", "firstInhibitor": "firstInhibitorKiller", "firstRiftHerald": "firstRiftHeraldKiller", "firstTower": "firstTowerKiller"}

    def __call__(self, **kwargs):
        if "bans" in kwargs:
            self.bans = [ban["championId"] for ban in kwargs.pop("bans")]
        if "win" in kwargs:
            self.isWinner = kwargs.pop("win") != "Fail"
        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))
        super().__call__(**kwargs)
        return self


class MatchReferenceData(CoreData):
    _renamed = {"account_id": "accountId", "gameId": "id", "champion": "championId", "teamId": "side", "platformId": "platform"}

    def __call__(self, **kwargs):
        if "timestamp" in kwargs:
            self.creation = arrow.get(kwargs.pop("timestamp") / 1000)

            # Set lane and role if they are missing from the data
            if "lane" not in kwargs:
                kwargs["lane"] = None
            if "role" not in kwargs:
                kwargs["role"] = None
        super().__call__(**kwargs)
        return self


class MatchData(CoreData):
    _dto_type = dto.MatchDto
    _renamed = {"gameId": "id", "gameVersion": "version", "gameMode": "mode", "gameType": "type", "queueId": "queue", "seasonId": "season"}

    def __call__(self, **kwargs):
        if "gameCreation" in kwargs:
            self.creation = arrow.get(kwargs["gameCreation"] / 1000)
        if "gameDuration" in kwargs:
            self.duration = datetime.timedelta(seconds=kwargs["gameDuration"])

        if "participants" in kwargs:
            good_participant_ids = []
            for participant in kwargs["participants"]:
                for pid in kwargs["participantIdentities"]:
                    if participant["participantId"] == pid["participantId"] and "player" in pid:
                        good_participant_ids.append(participant["participantId"])
                        participant["player"] =  pid["player"]
                        break
            self.privateGame = False
            if len(good_participant_ids) == 0:
                self.privateGame = True
            # For each participant id we found that has both a participant and an identity, add it to the match data's participants
            self.participants = []
            for participant in kwargs["participants"]:
                if self.privateGame or participant["participantId"] in good_participant_ids:
                    participant = ParticipantData(**participant)
                    self.participants.append(participant)
            assert len(self.participants) == len(kwargs["participants"])
            kwargs.pop("participants")
            kwargs.pop("participantIdentities")

        if "teams" in kwargs:
            self.teams = []
            for team in kwargs.pop("teams"):
                team_side = Side(team["teamId"])
                participants = []
                for participant in self.participants:
                    if participant.side is team_side:
                        participants.append(participant)
                self.teams.append(TeamData(**team, participants=participants))

        super().__call__(**kwargs)
        return self


##############
# Core Types #
##############


class MatchHistory(CassiopeiaLazyList):  # type: List[Match]
    """The match history for a summoner. By default, this will return the entire match history."""
    _data_types = {MatchListData}

    def __init__(self, *, summoner: Summoner, begin_index: int = None, end_index: int = None, begin_time: arrow.Arrow = None, end_time: arrow.Arrow = None, queues: Set[Queue] = None, seasons: Set[Season] = None, champions: Set[Champion] = None):
        assert end_index is None or end_index > begin_index
        if begin_time is not None and end_time is not None and begin_time > end_time:
            raise ValueError("`end_time` should be greater than `begin_time`")
        kwargs = {"region": summoner.region}
        kwargs["queues"] = queues or []
        kwargs["seasons"] = seasons or []
        champions = champions or []
        kwargs["championIds"] = [champion.id if isinstance(champion, Champion) else champion for champion in champions]
        kwargs["begin_index"] = begin_index
        kwargs["end_index"] = end_index
        if begin_time is not None and not isinstance(begin_time, (int, float)):
            begin_time = begin_time.int_timestamp * 1000
        kwargs["begin_time"] = begin_time
        if end_time is not None and not isinstance(end_time, (int, float)):
            end_time = end_time.int_timestamp * 1000
        kwargs["end_time"] = end_time
        assert isinstance(summoner, Summoner)
        self.__account_id_callable = lambda: summoner.account_id
        self.__summoner = summoner
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    def __get_query_from_kwargs__(cls, *, summoner: Summoner, begin_index: int = None, end_index: int = None, begin_time: arrow.Arrow = None, end_time: arrow.Arrow = None, queues: Set[Queue] = None, seasons: Set[Season] = None, champions: Set[Champion] = None):
        assert isinstance(summoner, Summoner)
        query = {"region": summoner.region}
        query["accountId"] = summoner.account_id

        if begin_index is not None:
            query["beginIndex"] = begin_index

        if end_index is not None:
            query["endIndex"] = end_index

        if begin_time is not None:
            if isinstance(begin_time, arrow.Arrow):
                begin_time = begin_time.int_timestamp * 1000
            query["beginTime"] = begin_time

        if end_time is not None:
            if isinstance(end_time, arrow.Arrow):
                end_time = end_time.int_timestamp * 1000
            query["endTime"] = end_time

        if queues is not None:
            query["queues"] = queues

        if seasons is not None:
            query["seasons"] = seasons

        if champions is not None:
            champions = [champion.id if isinstance(champion, Champion) else champion for champion in champions]
            query["champion.ids"] = champions

        return query

    @classmethod
    def from_generator(cls, generator: Generator, summoner: Summoner, **kwargs):
        self = cls.__new__(cls)
        kwargs["summoner"] = summoner
        self.__summoner = summoner
        CassiopeiaLazyList.__init__(self, generator=generator, **kwargs)
        return self

    def __call__(self, **kwargs) -> "MatchHistory":
        # summoner, begin_index, end_index, begin_time, end_time, queues, seasons, champions
        kwargs.setdefault("summoner", self.__summoner)
        kwargs.setdefault("begin_index", self.begin_index)
        kwargs.setdefault("end_index", self.end_index)
        kwargs.setdefault("begin_time", self.begin_time)
        kwargs.setdefault("end_time", self.end_time)
        kwargs.setdefault("queues", self.queues)
        kwargs.setdefault("seasons", self.seasons)
        kwargs.setdefault("champions", self.champions)
        return MatchHistory(**kwargs)

    @property
    def _account_id(self):
        try:
            return self.__account_id
        except AttributeError:
            self.__account_id = self.__account_id_callable()
            del self.__account_id_callable  # This releases the reference to the summoner
            return self.__account_id

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MatchListData].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @lazy_property
    def queues(self) -> Set[Queue]:
        return {Queue(q) for q in self._data[MatchListData].queues}

    @lazy_property
    def seasons(self) -> Set[Season]:
        return {Season(s) for s in self._data[MatchListData].seasons}

    @lazy_property
    def champions(self) -> Set[Champion]:
        return {Champion(id=cid, region=self.region) for cid in self._data[MatchListData].championIds}

    @property
    def begin_index(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].beginIndex
        except AttributeError:
            return None

    @property
    def end_index(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].endIndex
        except AttributeError:
            return None

    @property
    def begin_time(self) -> arrow.Arrow:
        time = self._data[MatchListData].begin_time
        if time is not None:
            return arrow.get(time / 1000)

    @property
    def end_time(self) -> arrow.Arrow:
        time = self._data[MatchListData].end_time
        if time is not None:
            return arrow.get(time / 1000)


class Position(CassiopeiaObject):
    _data_types = {PositionData}

    def __str__(self):
        return "<Position ({}, {})>".format(self.x, self.y)

    @property
    def x(self) -> int:
        return self._data[PositionData].x

    @property
    def y(self) -> int:
        return self._data[PositionData].y

    @property
    def location(self) -> SummonersRiftArea:
        return SummonersRiftArea.from_position(self)


@searchable({str: ["type", "tower_type", "ascended_type", "ward_type", "monster_type", "type", "monster_sub_type", "lane_type", "building_type"]})
class Event(CassiopeiaObject):
    _data_types = {EventData}

    @property
    def tower_type(self) -> Tower:
        return Tower(self._data[EventData].towerType)

    @property
    def side(self) -> Side:
        return Side(self._data[EventData].side)

    @property
    def ascended_type(self) -> str:
        return self._data[EventData].ascendedType

    @property
    def killer_id(self) -> int:
        return self._data[EventData].killerId

    @property
    def level_up_type(self) -> str:
        return self._data[EventData].levelUpType

    @property
    def captured_point(self) -> str:
        return self._data[EventData].capturedPoint

    @property
    def assisting_participants(self) -> List[int]:
        return self._data[EventData].assistingParticipants

    @property
    def ward_type(self) -> str:
        return self._data[EventData].wardType

    @property
    def monster_type(self) -> str:
        return self._data[EventData].monsterType

    @property
    def type(self) -> List[str]:
        """Legal values: CHAMPION_KILL, WARD_PLACED, WARD_KILL, BUILDING_KILL, ELITE_MONSTER_KILL, ITEM_PURCHASED, ITEM_SOLD, ITEM_DESTROYED, ITEM_UNDO, SKILL_LEVEL_UP, ASCENDED_EVENT, CAPTURE_POINT, PORO_KING_SUMMON"""
        return self._data[EventData].type

    @property
    def skill(self) -> int:
        return self._data[EventData].skill

    @property
    def victim_id(self) -> int:
        return self._data[EventData].victimId

    @property
    def timestamp(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self._data[EventData].timestamp/1000)

    @property
    def after_id(self) -> int:
        return self._data[EventData].afterId

    @property
    def monster_sub_type(self) -> str:
        return self._data[EventData].monsterSubType

    @property
    def lane_type(self) -> str:
        return self._data[EventData].laneType

    @property
    def item_id(self) -> int:
        return self._data[EventData].itemId

    @property
    def participant_id(self) -> int:
        return self._data[EventData].participantId

    @property
    def building_type(self) -> str:
        return self._data[EventData].buildingType

    @property
    def creator_id(self) -> int:
        return self._data[EventData].creatorId

    @property
    def position(self) -> Position:
        return Position.from_data(self._data[EventData].position)

    @property
    def before_id(self) -> int:
        return self._data[EventData].beforeId


class ParticipantFrame(CassiopeiaObject):
    _data_types = {ParticipantFrameData}

    @property
    def gold_earned(self) -> int:
        return self._data[ParticipantFrameData].goldEarned

    @property
    def team_score(self) -> int:
        return self._data[ParticipantFrameData].teamScore

    @property
    def participant_id(self) -> int:
        return self._data[ParticipantFrameData].participantId

    @property
    def level(self) -> int:
        return self._data[ParticipantFrameData].level

    @property
    def current_gold(self) -> int:
        return self._data[ParticipantFrameData].currentGold

    @property
    def creep_score(self) -> int:
        return self._data[ParticipantFrameData].creepScore

    @property
    def dominion_score(self) -> int:
        return self._data[ParticipantFrameData].dominionScore

    @property
    def position(self) -> Position:
        return Position.from_data(self._data[ParticipantFrameData].position)

    @property
    def experience(self) -> int:
        return self._data[ParticipantFrameData].experience

    @property
    def neutral_minions_killed(self) -> int:
        return self._data[ParticipantFrameData].neutralMinionsKilled


class Frame(CassiopeiaObject):
    _data_types = {FrameData}

    @property
    def timestamp(self) -> datetime.timedelta:
        return datetime.timedelta(seconds=self._data[FrameData].timestamp/1000)

    @property
    def participant_frames(self) -> Dict[int, ParticipantFrame]:
        return SearchableDictionary({k: ParticipantFrame.from_data(frame) for k, frame in self._data[FrameData].participantFrames.items()})

    @property
    def events(self) -> List[Event]:
        return SearchableList([Event.from_data(event) for event in self._data[FrameData].events])


class Timeline(CassiopeiaGhost):
    _data_types = {TimelineData}

    @provide_default_region
    def __init__(self, *, id: int = None, region: Union[Region, str] = None):
        kwargs = {"region": region, "id": id}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "id": self.id}

    @property
    def id(self):
        return self._data[TimelineData].id

    @property
    def region(self) -> Region:
        return Region(self._data[TimelineData].region)

    @property
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(TimelineData)
    @ghost_load_on
    def frames(self) -> List[Frame]:
        return SearchableList([Frame.from_data(frame) for frame in self._data[TimelineData].frames])

    @CassiopeiaGhost.property(TimelineData)
    @ghost_load_on
    def frame_interval(self) -> int:
        return self._data[TimelineData].frame_interval

    @property
    def first_tower_fallen(self) -> Event:
        for frame in self.frames:
            for event in frame.events:
                if event.type == "BUILDING_KILL" and event.building_type == "TOWER_BUILDING":
                    return event


class ParticipantTimeline(CassiopeiaObject):
    _data_types = {ParticipantTimelineData}

    @classmethod
    def from_data(cls, data: CoreData, match: "Match"):
        self = super().from_data(data)
        self.__match = match
        return self

    @property
    def frames(self):
        these = []
        for frame in self.__match.timeline.frames:
            for pid, pframe in frame.participant_frames.items():
                pframe.timestamp = frame.timestamp
                if pid == self.id:
                    these.append(pframe)
        return these

    @property
    def events(self):
        my_events = []
        timeline = self.__match.timeline
        for frame in timeline.frames:
            for event in frame.events:
                try:
                    if event.participant_id == self.id:
                        my_events.append(event)
                except AttributeError:
                    pass
                try:
                    if event.creator_id == self.id:
                        my_events.append(event)
                except AttributeError:
                    pass
                try:
                    if event.killer_id == self.id:
                        my_events.append(event)
                except AttributeError:
                    pass
                try:
                    if event.victim_id == self.id:
                        my_events.append(event)
                except AttributeError:
                    pass
                try:
                    if self.id in event.assisting_participants:
                        my_events.append(event)
                except AttributeError:
                    pass
        return SearchableList(my_events)

    @property
    def champion_kills(self):
        return self.events.filter(lambda event: event.type == "CHAMPION_KILL" and event.killer_id == self.id)

    @property
    def champion_deaths(self):
        return self.events.filter(lambda event: event.type == "CHAMPION_KILL" and event.victim_id == self.id)

    @property
    def champion_assists(self):
        return self.events.filter(lambda event: event.type == "CHAMPION_KILL" and self.id in event.assisting_participants)

    @property
    def lane(self) -> Lane:
        return Lane.from_match_naming_scheme(self._data[ParticipantTimelineData].lane)

    @property
    def role(self) -> Role:
        return Role.from_match_naming_scheme(self._data[ParticipantTimelineData].role)

    @property
    def id(self) -> int:
        return self._data[ParticipantTimelineData].id

    @property
    def cs_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].csDiffPerMinDeltas

    @property
    def gold_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].goldPerMinDeltas

    @property
    def xp_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xpDiffPerMinDeltas

    @property
    def creeps_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].creepsPerMinDeltas

    @property
    def xp_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xpPerMinDeltas

    @property
    def damage_taken_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damageTakenPerMinDeltas

    @property
    def damage_taken_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damageTakenDiffPerMinDeltas


class CumulativeTimeline:
    def __init__(self, id: int, participant_timeline: ParticipantTimeline):
        self._id = id
        self._timeline = participant_timeline

    def __getitem__(self, time: Union[datetime.timedelta, str]) -> "ParticipantState":
        if isinstance(time, str):
            time = time.split(":")
            time = datetime.timedelta(minutes=int(time[0]), seconds=int(time[1]))
        state = ParticipantState(id=self._id, time=time, participant_timeline=self._timeline)
        for event in self._timeline.events:
            if event.timestamp > time:
                break
            state._process_event(event)
        return state


class ParticipantState:
    """The state of a participant at a given point in the timeline."""
    def __init__(self, id: int, time: datetime.timedelta, participant_timeline: ParticipantTimeline):
        self._id = id
        self._time = time
        #self._timeline = participant_timeline
        # Try to get info from the most recent participant timeline object
        latest_frame = None
        for frame in participant_timeline.frames:
            # Round to the nearest second for the frame timestamp because it's off by a few ms
            rounded_frame_timestamp = datetime.timedelta(seconds=frame.timestamp.seconds)
            if rounded_frame_timestamp > self._time:
                break
            latest_frame = frame
        self._latest_frame = latest_frame
        self._item_state = _ItemState()
        self._skills = Counter()
        self._kills = 0
        self._deaths = 0
        self._assists = 0
        self._objectives = 0
        self._level = 1
        self._processed_events = []

    def _process_event(self, event: Event):
        if "ITEM" in event.type:
            self._item_state.process_event(event)
        elif "CHAMPION_KILL" == event.type:
            if event.killer_id == self._id:
                self._kills += 1
            elif event.victim_id == self._id:
                self._deaths += 1
            else:
                assert self._id in event.assisting_participants
                self._assists += 1
        elif "SKILL_LEVEL_UP" == event.type:
            if event.level_up_type == "NORMAL":
                self._skills[event.skill] += 1
                self._level += 1
        elif event.type in ("WARD_PLACED", "WARD_KILL"):
            return
        elif event.type in ("ELITE_MONSTER_KILL", "BUILDING_KILL"):
            self._objectives += 1
        else:
            #print(f"Did not process event {event.to_dict()}")
            pass
        self._processed_events.append(event)

    @property
    def items(self) -> SearchableList:
        return SearchableList([Item(id=id_, region="NA") for id_ in self._item_state._items])

    @property
    def skills(self) -> Dict[Key, int]:
        skill_keys = {1: Key.Q, 2: Key.W, 3: Key.E, 4: Key.R}
        skills = {skill_keys[skill]: level for skill, level in self._skills.items()}
        return skills

    @property
    def kills(self) -> int:
        return self._kills

    @property
    def deaths(self) -> int:
        return self._deaths

    @property
    def assists(self) -> int:
        return self._assists

    @property
    def kda(self) -> float:
        return (self.kills + self.assists) / (self.deaths or 1)

    @property
    def objectives(self) -> int:
        """Number of objectives assisted in."""
        return self._objectives

    @property
    def level(self) -> int:
        return self._level

    @property
    def gold_earned(self) -> int:
        return self._latest_frame.gold_earned

    @property
    def team_score(self) -> int:
        return self._latest_frame.team_score

    @property
    def current_gold(self) -> int:
        return self._latest_frame.current_gold

    @property
    def creep_score(self) -> int:
        return self._latest_frame.creep_score

    @property
    def dominion_score(self) -> int:
        return self._latest_frame.dominion_score

    @property
    def position(self) -> Position:
        # The latest position is either from the latest event or from the participant timeline frame
        latest_frame_ts = self._latest_frame.timestamp
        latest_event_with_ts = [(getattr(event, 'timestamp', None), getattr(event, 'position', None)) for event in self._processed_events]
        latest_event_with_ts = [(ts, p) for ts, p in latest_event_with_ts if ts is not None and p is not None]
        latest_event_ts = sorted(latest_event_with_ts)[-1]
        if latest_frame_ts > latest_event_ts[0]:
            return self._latest_frame.position
        else:
            return latest_event_ts[1]

    @property
    def experience(self) -> int:
        return self._latest_frame.experience

    @property
    def neutral_minions_killed(self) -> int:
        return self._latest_frame.neutral_minions_killed


class _ItemState:
    def __init__(self, *args):
        self._items = []
        self._events = []

    def __str__(self):
        return str(self._items)

    def process_event(self, event):
        items_to_ignore = (2010, 3599, 3520, 3513, 2422, 2052)
        # 2422 is Slightly Magical Boots... I could figure out how to add those and Biscuits to the inventory based on runes but it would be manual...
        # 2052 is Poro-Snax, which gets added to inventory eventless
        upgradable_items = {
            3850: 3851, 3851: 3853, # Spellthief's Edge -> Frostfang -> Shard of True Ice
            3854: 3855, 3855: 3857, # Steel Shoulderguards -> Runesteel Spaulders -> Pauldrons of Whiterock
            3858: 3859, 3859: 3860, # Relic Shield -> Targon's Buckler -> Bulwark of the Mountain
            3862: 3863, 3863: 3864, # Spectral Sickle -> Harrowing Crescent -> Black Mist Scythe
        }
        item_id = getattr(event, 'item_id', getattr(event, 'before_id', None))
        assert item_id is not None
        if item_id in items_to_ignore:
            return
        if event.type == "ITEM_PURCHASED":
            self.add(event.item_id)
            self._events.append(event)
        elif event.type == "ITEM_DESTROYED":
            self.destroy(event.item_id)
            if event.item_id in upgradable_items:
                # add the upgraded item
                self.add(upgradable_items[event.item_id])
            self._events.append(event)
        elif event.type == "ITEM_SOLD":
            self.destroy(event.item_id)
            self._events.append(event)
        elif event.type == "ITEM_UNDO":
            self.undo(event)
        else:
            raise ValueError(f"Unexpected event type {event.type}")

    def add(self, item: int):
        self._items.append(item)

    def destroy(self, item: int):
        self._items.reverse()
        try:
            self._items.remove(item)
        except ValueError as error:
            if item in (3340, 3364, 2319, 2061, 2062, 2056, 2403, 2419, 3400, 2004, 2058, 3200, 2011, 2423, 2055, 2057, 2424, 2059, 2060, 2013, 2421, 3600):  # Something weird can happen with trinkets and klepto items
                pass
            else:
                raise error
        self._items.reverse()

    def undo(self, event: Event):
        assert event.after_id == 0 or event.before_id == 0
        item_id = event.before_id or event.after_id
        prev = None
        while prev is None or prev.item_id != item_id:
            prev = self._events.pop()
            if prev.type == "ITEM_PURCHASED":
                self.destroy(prev.item_id)
            elif prev.type == "ITEM_DESTROYED":
                self.add(prev.item_id)
            elif prev.type == "ITEM_SOLD":
                self.add(prev.item_id)
            else:
                raise TypeError(f"Unexpected event type {prev.type}")


@searchable({str: ["items"], Item: ["items"]})
class ParticipantStats(CassiopeiaObject):
    _data_types = {ParticipantStatsData}

    @classmethod
    def from_data(cls, data: ParticipantStatsData, match: "Match", participant: "Participant"):
        self = super().from_data(data)
        self.__match = match
        self.__participant = participant
        return self

    @property
    @load_match_on_attributeerror
    def kda(self) -> float:
        return (self.kills + self.assists) / (self.deaths or 1)

    @property
    @load_match_on_attributeerror
    def physical_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageDealt

    @property
    @load_match_on_attributeerror
    def magic_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].magicDamageDealt

    @property
    @load_match_on_attributeerror
    def neutral_minions_killed_team_jungle(self) -> int:
        return self._data[ParticipantStatsData].neutralMinionsKilledTeamJungle

    @property
    @load_match_on_attributeerror
    def total_player_score(self) -> int:
        return self._data[ParticipantStatsData].totalPlayerScore

    @property
    @load_match_on_attributeerror
    def deaths(self) -> int:
        return self._data[ParticipantStatsData].deaths

    @property
    @load_match_on_attributeerror
    def win(self) -> bool:
        return self._data[ParticipantStatsData].win

    @property
    @load_match_on_attributeerror
    def neutral_minions_killed_enemy_jungle(self) -> int:
        return self._data[ParticipantStatsData].neutralMinionsKilledEnemyJungle

    @property
    @load_match_on_attributeerror
    def altars_captured(self) -> int:
        return self._data[ParticipantStatsData].altarsCaptured

    @property
    @load_match_on_attributeerror
    def largest_critical_strike(self) -> int:
        return self._data[ParticipantStatsData].largestCriticalStrike

    @property
    @load_match_on_attributeerror
    def total_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].totalDamageDealt

    @property
    @load_match_on_attributeerror
    def magic_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].magicDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def vision_wards_bought_in_game(self) -> int:
        return self._data[ParticipantStatsData].visionWardsBoughtInGame

    @property
    @load_match_on_attributeerror
    def damage_dealt_to_objectives(self) -> int:
        return self._data[ParticipantStatsData].damageDealtToObjectives

    @property
    @load_match_on_attributeerror
    def largest_killing_spree(self) -> int:
        return self._data[ParticipantStatsData].largestKillingSpree

    @property
    @load_match_on_attributeerror
    def quadra_kills(self) -> int:
        return self._data[ParticipantStatsData].quadraKills

    @property
    @load_match_on_attributeerror
    def team_objective(self) -> int:
        return self._data[ParticipantStatsData].teamObjective

    @property
    @load_match_on_attributeerror
    def total_time_crowd_control_dealt(self) -> int:
        return self._data[ParticipantStatsData].totalTimeCrowdControlDealt

    @property
    @load_match_on_attributeerror
    def longest_time_spent_living(self) -> int:
        return self._data[ParticipantStatsData].longestTimeSpentLiving

    @property
    @load_match_on_attributeerror
    def wards_killed(self) -> int:
        return self._data[ParticipantStatsData].wardsKilled

    @property
    @load_match_on_attributeerror
    def first_tower_assist(self) -> bool:
        return self._data[ParticipantStatsData].firstTowerAssist

    @property
    @load_match_on_attributeerror
    def first_tower_kill(self) -> bool:
        return self._data[ParticipantStatsData].firstTowerKill

    @lazy_property
    @load_match_on_attributeerror
    def items(self) -> List[Item]:
        ids = [self._data[ParticipantStatsData].item0,
               self._data[ParticipantStatsData].item1,
               self._data[ParticipantStatsData].item2,
               self._data[ParticipantStatsData].item3,
               self._data[ParticipantStatsData].item4,
               self._data[ParticipantStatsData].item5,
               self._data[ParticipantStatsData].item6
        ]
        version = _choose_staticdata_version(self.__match)
        return SearchableList([Item(id=id, version=version, region=self.__match.region) if id else None for id in ids])

    @property
    @load_match_on_attributeerror
    def first_blood_assist(self) -> bool:
        return self._data[ParticipantStatsData].firstBloodAssist

    @property
    @load_match_on_attributeerror
    def vision_score(self) -> int:
        return self._data[ParticipantStatsData].visionScore

    @property
    @load_match_on_attributeerror
    def wards_placed(self) -> int:
        return self._data[ParticipantStatsData].wardsPlaced

    @property
    @load_match_on_attributeerror
    def turret_kills(self) -> int:
        return self._data[ParticipantStatsData].turretKills

    @property
    @load_match_on_attributeerror
    def triple_kills(self) -> int:
        return self._data[ParticipantStatsData].tripleKills

    @property
    @load_match_on_attributeerror
    def damage_self_mitigated(self) -> int:
        return self._data[ParticipantStatsData].damageSelfMitigated

    @property
    @load_match_on_attributeerror
    def level(self) -> int:
        return self._data[ParticipantStatsData].champLevel

    @property
    @load_match_on_attributeerror
    def node_neutralize_assist(self) -> int:
        return self._data[ParticipantStatsData].nodeNeutralizeAssist

    @property
    @load_match_on_attributeerror
    def first_inhibitor_kill(self) -> bool:
        return self._data[ParticipantStatsData].firstInhibitorKill

    @property
    @load_match_on_attributeerror
    def gold_earned(self) -> int:
        return self._data[ParticipantStatsData].goldEarned

    @property
    @load_match_on_attributeerror
    def magical_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].magicalDamageTaken

    @property
    @load_match_on_attributeerror
    def kills(self) -> int:
        return self._data[ParticipantStatsData].kills

    @property
    @load_match_on_attributeerror
    def double_kills(self) -> int:
        return self._data[ParticipantStatsData].doubleKills

    @property
    @load_match_on_attributeerror
    def node_capture_assist(self) -> int:
        return self._data[ParticipantStatsData].nodeCaptureAssist

    @property
    @load_match_on_attributeerror
    def true_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].trueDamageTaken

    @property
    @load_match_on_attributeerror
    def node_neutralize(self) -> int:
        return self._data[ParticipantStatsData].nodeNeutralize

    @property
    @load_match_on_attributeerror
    def first_inhibitor_assist(self) -> bool:
        return self._data[ParticipantStatsData].firstInhibitorAssist

    @property
    @load_match_on_attributeerror
    def assists(self) -> int:
        return self._data[ParticipantStatsData].assists

    @property
    @load_match_on_attributeerror
    def unreal_kills(self) -> int:
        return self._data[ParticipantStatsData].unrealKills

    @property
    @load_match_on_attributeerror
    def neutral_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].neutralMinionsKilled

    @property
    @load_match_on_attributeerror
    def objective_player_score(self) -> int:
        return self._data[ParticipantStatsData].objectivePlayerScore

    @property
    @load_match_on_attributeerror
    def combat_player_score(self) -> int:
        return self._data[ParticipantStatsData].combatPlayerScore

    @property
    @load_match_on_attributeerror
    def damage_dealt_to_turrets(self) -> int:
        return self._data[ParticipantStatsData].damageDealtToTurrets

    @property
    @load_match_on_attributeerror
    def altars_neutralized(self) -> int:
        return self._data[ParticipantStatsData].altarsNeutralized

    @property
    @load_match_on_attributeerror
    def physical_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def gold_spent(self) -> int:
        return self._data[ParticipantStatsData].goldSpent

    @property
    @load_match_on_attributeerror
    def true_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].trueDamageDealt

    @property
    @load_match_on_attributeerror
    def true_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].trueDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def id(self) -> int:
        return self._data[ParticipantStatsData].id

    @property
    @load_match_on_attributeerror
    def penta_kills(self) -> int:
        return self._data[ParticipantStatsData].pentaKills

    @property
    @load_match_on_attributeerror
    def total_heal(self) -> int:
        return self._data[ParticipantStatsData].totalHeal

    @property
    @load_match_on_attributeerror
    def total_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].totalMinionsKilled

    @property
    @load_match_on_attributeerror
    def first_blood_kill(self) -> bool:
        return self._data[ParticipantStatsData].firstBloodKill

    @property
    @load_match_on_attributeerror
    def node_capture(self) -> int:
        return self._data[ParticipantStatsData].nodeCapture

    @property
    @load_match_on_attributeerror
    def largest_multi_kill(self) -> int:
        return self._data[ParticipantStatsData].largestMultiKill

    @property
    @load_match_on_attributeerror
    def sight_wards_bought_in_game(self) -> int:
        return self._data[ParticipantStatsData].sightWardsBoughtInGame

    @property
    @load_match_on_attributeerror
    def total_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].totalDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def total_units_healed(self) -> int:
        return self._data[ParticipantStatsData].totalUnitsHealed

    @property
    @load_match_on_attributeerror
    def inhibitor_kills(self) -> int:
        return self._data[ParticipantStatsData].inhibitorKills

    @property
    @load_match_on_attributeerror
    def total_score_rank(self) -> int:
        return self._data[ParticipantStatsData].totalScoreRank

    @property
    @load_match_on_attributeerror
    def total_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].totalDamageTaken

    @property
    @load_match_on_attributeerror
    def killing_sprees(self) -> int:
        return self._data[ParticipantStatsData].killingSprees

    @property
    @load_match_on_attributeerror
    def time_CCing_others(self) -> int:
        return self._data[ParticipantStatsData].timeCCingOthers

    @property
    @load_match_on_attributeerror
    def physical_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageTaken


@searchable({str: ["summoner", "champion", "stats", "runes", "side", "summoner_spell_d", "summoner_spell_f"], Summoner: ["summoner"], Champion: ["champion"], Side: ["side"], Rune: ["runes"], SummonerSpell: ["summoner_spell_d", "summoner_spell_f"]})
class Participant(CassiopeiaObject):
    _data_types = {ParticipantData}

    @classmethod
    def from_data(cls, data: CoreData, match: "Match"):
        self = super().from_data(data)
        self.__match = match
        return self

    @property
    def version(self) -> str:
        version = self.__match.version
        version = version.split(".")[0:2]
        version = ".".join(version) + ".1"  # Always use x.x.1 because I don't know how to figure out what the last version number should be.
        return version

    @property
    def lane(self) -> Lane:
        return Lane.from_match_naming_scheme(self._data[ParticipantData].timeline.lane)

    @property
    def role(self) -> Role:
        return Role.from_match_naming_scheme(self._data[ParticipantData].timeline.role)

    @property
    def skill_order(self) -> List[Key]:
        skill_events = self.timeline.events.filter(lambda event: event.type == "SKILL_LEVEL_UP")
        skill_events.sort(key=lambda event: event.timestamp)
        skills = [event.skill - 1 for event in skill_events]
        spells = [self.champion.spells[Key("Q")], self.champion.spells[Key("W")], self.champion.spells[Key("E")], self.champion.spells[Key("R")]]
        skills = [spells[skill] for skill in skills]
        return skills

    @lazy_property
    @load_match_on_attributeerror
    def stats(self) -> ParticipantStats:
        return ParticipantStats.from_data(self._data[ParticipantData].stats, match=self.__match, participant=self)

    @lazy_property
    @load_match_on_attributeerror
    def id(self) -> int:
        if self._data[ParticipantData].id is None:
            raise AttributeError
        return self._data[ParticipantData].id

    @lazy_property
    @load_match_on_attributeerror
    def is_bot(self) -> bool:
        return self._data[ParticipantData].isBot

    @lazy_property
    @load_match_on_attributeerror
    def runes(self) -> Dict[Rune, int]:
        version = _choose_staticdata_version(self.__match)
        runes = SearchableDictionary({Rune(id=rune_id, version=version, region=self.__match.region): perk_vars
                                      for rune_id, perk_vars in self._data[ParticipantData].runes.items()})

        def keystone(self):
            for rune in self:
                if rune.is_keystone:
                    return rune
        # The bad thing about calling this here is that the runes won't be lazy loaded, so if the user only want the
        #  rune ids then there will be a needless call. That said, it's pretty nice functionality to have and without
        #  making a custom RunePage class, I believe this is the only option.
        runes.keystone = keystone(runes)
        return runes

    @lazy_property
    @load_match_on_attributeerror
    def stat_runes(self) -> List[Rune]:
        version = _choose_staticdata_version(self.__match)
        runes = SearchableList([Rune(id=rune_id, version=version, region=self.__match.region)
                                for rune_id in self._data[ParticipantData].stat_runes])
        return runes

    @lazy_property
    @load_match_on_attributeerror
    def timeline(self) -> ParticipantTimeline:
        timeline = ParticipantTimeline.from_data(self._data[ParticipantData].timeline, match=self.__match)
        timeline(id=self.id)
        return timeline

    @property
    def cumulative_timeline(self) -> CumulativeTimeline:
        return CumulativeTimeline(id=self.id, participant_timeline=self.timeline)

    @lazy_property
    @load_match_on_attributeerror
    def side(self) -> Side:
        return Side(self._data[ParticipantData].side)

    @lazy_property
    @load_match_on_attributeerror
    def summoner_spell_d(self) -> SummonerSpell:
        version = _choose_staticdata_version(self.__match)
        return SummonerSpell(id=self._data[ParticipantData].summonerSpellDId, version=version, region=self.__match.region)

    @lazy_property
    @load_match_on_attributeerror
    def summoner_spell_f(self) -> SummonerSpell:
        version = _choose_staticdata_version(self.__match)
        return SummonerSpell(id=self._data[ParticipantData].summonerSpellFId, version=version, region=self.__match.region)

    @lazy_property
    @load_match_on_attributeerror
    def rank_last_season(self) -> Tier:
        return Tier(self._data[ParticipantData].rankLastSeason)

    @property
    @load_match_on_attributeerror
    def match_history_uri(self) -> str:
        return self._data[ParticipantData].matchHistoryUri

    @lazy_property
    @load_match_on_attributeerror
    def champion(self) -> "Champion":
        # See ParticipantStats for info
        version = _choose_staticdata_version(self.__match)
        return Champion(id=self._data[ParticipantData].championId, version=version, region=self.__match.region)

    # All the Player data from ParticipantIdentities.player is contained in the Summoner class.
    # The non-current accountId and platformId should never be relevant/used, and can be deleted from our type system.
    #   See: https://discussion.developer.riotgames.com/questions/1713/is-there-any-scenario-where-accountid-should-be-us.html
    @lazy_property
    def summoner(self) -> Summoner:
        if self.__match._data[MatchData].privateGame:
            return None
        kwargs = {}
        try:
            kwargs["id"] = self._data[ParticipantData].summonerId
        except AttributeError:
            pass
        try:
            kwargs["name"] = self._data[ParticipantData].summonerName
        except AttributeError:
            pass
        kwargs["account_id"] = self._data[ParticipantData].currentAccountId
        kwargs["region"] = Platform(self._data[ParticipantData].currentPlatformId).region
        summoner = Summoner(**kwargs)
        try:
            summoner(profileIconId=self._data[ParticipantData].profileIconId)
        except AttributeError:
            pass
        return summoner

    @property
    def team(self) -> "Team":
        if self.side == Side.blue:
            return self.__match.blue_team
        else:
            return self.__match.red_team

    @property
    def enemy_team(self) -> "Team":
        if self.side == Side.blue:
            return self.__match.red_team
        else:
            return self.__match.blue_team


@searchable({str: ["participants"], bool: ["win"], Champion: ["participants"], Summoner: ["participants"], SummonerSpell: ["participants"]})
class Team(CassiopeiaObject):
    _data_types = {TeamData}

    @classmethod
    def from_data(cls, data: CoreData, match: "Match"):
        self = super().from_data(data)
        self.__match = match
        return self

    @property
    def first_dragon(self) -> bool:
        return self._data[TeamData].firstDragonKiller

    @property
    def first_inhibitor(self) -> bool:
        return self._data[TeamData].firstInhibitorKiller

    @property
    def first_rift_herald(self) -> bool:
        return self._data[TeamData].firstRiftHeraldKiller

    @property
    def first_baron(self) -> bool:
        return self._data[TeamData].firstBaronKiller

    @property
    def first_tower(self) -> bool:
        return self._data[TeamData].firstTowerKiller

    @property
    def first_blood(self) -> bool:
        return self._data[TeamData].firstBloodKiller

    @property
    def bans(self) -> List["Champion"]:
        version = _choose_staticdata_version(self.__match)
        return [Champion(id=champion_id, version=version, region=self.__match.region) if champion_id != -1 else None for champion_id in self._data[TeamData].bans]

    @property
    def baron_kills(self) -> int:
        return self._data[TeamData].baronKills

    @property
    def rift_herald_kills(self) -> int:
        return self._data[TeamData].riftHeraldKills

    @property
    def vilemaw_kills(self) -> int:
        return self._data[TeamData].vilemawKills

    @property
    def inhibitor_kills(self) -> int:
        return self._data[TeamData].inhibitorKills

    @property
    def tower_kills(self) -> int:
        return self._data[TeamData].towerKills

    @property
    def dragon_kills(self) -> int:
        return self._data[TeamData].dragonKills

    @property
    def side(self) -> Side:
        return self._data[TeamData].side

    @property
    def dominion_score(self) -> int:
        return self._data[TeamData].dominionScore

    @property
    def win(self) -> bool:
        return self._data[TeamData].isWinner

    @lazy_property
    def participants(self) -> List[Participant]:
        return SearchableList([Participant.from_data(p, match=self.__match) for p in self._data[TeamData].participants])


@searchable({str: ["participants", "region", "platform", "season", "queue", "mode", "map", "type"], Region: ["region"], Platform: ["platform"], Season: ["season"], Queue: ["queue"], GameMode: ["mode"], Map: ["map"], GameType: ["type"], Item: ["participants"], Champion: ["participants"], Patch: ["patch"], Summoner: ["participants"], SummonerSpell: ["participants"]})
class Match(CassiopeiaGhost):
    _data_types = {MatchData}

    @provide_default_region
    def __init__(self, *, id: int = None, region: Union[Region, str] = None):
        kwargs = {"region": region, "id": id}
        super().__init__(**kwargs)
        self.__participants = []  # For lazy-loading the participants in a special way
        self._timeline = None

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "id": self.id}

    @classmethod
    def from_match_reference(cls, ref: MatchReferenceData):
        instance = cls(id=ref.id, region=ref.region)
        # The below line is necessary because it's possible to pull this match from the cache (which has Match core objects in it).
        # In that case, the data will already be loaded and we don't want to overwrite anything.
        if not hasattr(instance._data[MatchData], "participants"):
            participant = {"participantId": None, "championId": ref.championId, "timeline": {"lane": ref.lane, "role": ref.role}}
            player = {"participantId": None, "currentAccountId": ref.accountId, "currentPlatformId": ref.platform}
            instance(season=ref.season, queue=ref.queue, creation=ref.creation)
            instance._data[MatchData](participants=[participant],
                                      participantIdentities=[{"participantId": None, "player": player, "bot": False}])
        instance._timeline = None
        return instance

    def __eq__(self, other: "Match"):
        if not isinstance(other, Match) or self.region != other.region:
            return False
        return self.id == other.id

    def __str__(self):
        region = self.region
        id_ = self.id
        return "Match(id={id_}, region='{region}')".format(id_=id_, region=region.value)

    __hash__ = CassiopeiaGhost.__hash__

    @lazy_property
    def region(self) -> Region:
        """The region for this match."""
        return Region(self._data[MatchData].region)

    @property
    def platform(self) -> Platform:
        """The platform for this match."""
        return self.region.platform

    @property
    def id(self) -> int:
        return self._data[MatchData].id

    @lazy_property
    def timeline(self) -> Timeline:
        if self._timeline is None:
            self._timeline = Timeline(id=self.id, region=self.region.value)
        return self._timeline

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def season(self) -> Season:
        return Season.from_id(self._data[MatchData].season)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue.from_id(self._data[MatchData].queue)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    # This method is lazy-loaded in a special way because of its unique behavior
    def participants(self) -> List[Participant]:
        # This is a complicated function because we don't want to load the particpants if the only one the user cares about is the one loaded from a match ref

        def generate_participants(match):
            if not hasattr(match._data[MatchData], "participants"):
                empty_match = True
            else:
                empty_match = False

            # If a participant was provided from a matchref, yield that first
            yielded_one = False
            if not empty_match and len(match._data[MatchData].participants) == 1:
                yielded_one = True
                try:
                    yield match.__participants[0]
                except IndexError:
                    p = match._data[MatchData].participants[0]
                    participant = Participant.from_data(p, match=match)
                    match.__participants.append(participant)
                    yield participant

            # Create all the participants if any haven't been created yet.
            # Note that it's important to overwrite the one from the matchref if it was loaded because we have more data after we load the full match.
            if empty_match or yielded_one or len(match.__participants) < len(match._data[MatchData].participants):
                if not match._Ghost__is_loaded(MatchData):
                    match.__load__(MatchData)
                    match._Ghost__set_loaded(MatchData)  # __load__ doesn't trigger __set_loaded.
                for i, p in enumerate(match._data[MatchData].participants):
                    participant = Participant.from_data(p, match=match)
                    # If we already have this participant in the list, replace it so it stays in the same position
                    for j, pold in enumerate(match.__participants):
                        if hasattr(pold._data[ParticipantData], "currentAccountId") and hasattr(participant._data[ParticipantData], "currentAccountId") and pold._data[ParticipantData].currentAccountId == participant._data[ParticipantData].currentAccountId:
                            match.__participants[j] = participant
                            break
                    else:
                        match.__participants.append(participant)

            # Yield the rest of the participants
            for participant in match.__participants[yielded_one:]:
                yield participant

        return SearchableLazyList(generate_participants(self))

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def teams(self) -> List[Team]:
        return [Team.from_data(t, match=self) for i, t in enumerate(self._data[MatchData].teams)]

    @property
    def red_team(self) -> Team:
        if self.teams[0].side is Side.red:
            return self.teams[0]
        else:
            return self.teams[1]

    @property
    def blue_team(self) -> Team:
        if self.teams[0].side is Side.blue:
            return self.teams[0]
        else:
            return self.teams[1]

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    def version(self) -> str:
        return self._data[MatchData].version

    @property
    def patch(self) -> Patch:
        if hasattr(self._data[MatchData], "version"):
            version = ".".join(self.version.split(".")[:2])
            patch = Patch.from_str(version, region=self.region)
        else:
            date = self.creation
            patch = Patch.from_date(date, region=self.region)
        return patch

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def mode(self) -> GameMode:
        return GameMode(self._data[MatchData].mode)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def map(self) -> Map:
        version = _choose_staticdata_version(self)
        return Map(id=self._data[MatchData].mapId, region=self.region, version=version)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def type(self) -> GameType:
        return GameType(self._data[MatchData].type)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def duration(self) -> datetime.timedelta:
        return self._data[MatchData].duration

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def creation(self) -> arrow.Arrow:
        return self._data[MatchData].creation

    @property
    def is_remake(self) -> bool:
        return self.duration < datetime.timedelta(minutes=5)

    @property
    def exists(self) -> bool:
        try:
            if not self._Ghost__all_loaded:
                self.__load__()
            self.type  # Make sure we can access this attribute
            return True
        except (AttributeError, NotFoundError):
            return False

    def kills_heatmap(self):
        if self.map.name == "Summoner's Rift":
            rx0, ry0, rx1, ry1 = 0, 0, 14820, 14881
        elif self.map.name == "Howling Abyss":
            rx0, ry0, rx1, ry1 = -28, -19, 12849, 12858
        else:
            raise NotImplemented

        imx0, imy0, imx1, imy1 = self.map.image.image.getbbox()

        def position_to_map_image_coords(position):
            x, y = position.x, position.y
            x -= rx0
            x /= (rx1 - rx0)
            x *= (imx1 - imx0)
            y -= ry0
            y /= (ry1 - ry0)
            y *= (imy1 - imy0)
            return x, y

        import matplotlib.pyplot as plt
        size = 8
        plt.figure(figsize=(size, size))
        plt.imshow(self.map.image.image.rotate(-90))
        for p in self.participants:
            for kill in p.timeline.champion_kills:
                x, y = position_to_map_image_coords(kill.position)
                if p.team.side == Side.blue:
                    plt.scatter([x], [y], c="b", s=size * 10)
                else:
                    plt.scatter([x], [y], c="r", s=size * 10)
        plt.axis('off')
        plt.show()
