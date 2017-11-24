import functools
import datetime
from typing import List, Dict, Set, Union, Generator

from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList, SearchableLazyList, SearchableDictionary

from .. import configuration
from ..data import Region, Platform, Tier, GameType, GameMode, Queue, Side, Season, Patch, Lane, Role
from .common import CoreData, CoreDataList, DataObjectGenerator, CassiopeiaObject, CassiopeiaGhost, CassiopeiaLazyList, provide_default_region, ghost_load_on
from ..dto import match as dto
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


def _choose_staticdata_version(match):
    # If we want to pull the data for the correct version, we need to pull the entire match data.
    # However, we can use the creation date (which comes with a matchref) and get the ~ patch and therefore extract the version from the patch.
    if configuration.settings.version_from_match == "latest":
        version = None  # Rather than pick the latest version here, let the obj handle it so it knows which endpoint within the realms data to use
    elif configuration.settings.version_from_match == "version" or hasattr(match._data[MatchData], "version"):
        version = match.version
        version = ".".join(version.split(".")[:2]) + ".1"
    elif configuration.settings.version_from_match == "patch":
        patch = Patch.from_date(match.creation, region=match.region)
        version = patch.majorminor + ".1"  # Just always use x.x.1
    else:
        raise ValueError("Unknown value for setting `version_from_match`:", configuration.settings.version_from_match)
    return version


##############
# Data Types #
##############


class MatchListData(CoreDataList):
    _dto_type = dto.MatchListDto
    _renamed = {"champion": "championIds", "queue": "queues", "season": "seasons"}


class MatchListGenerator(DataObjectGenerator):
    _dto_type = dto.MatchListDtoGenerator
    _renamed = {"champion": "championIds", "queue": "queues", "season": "seasons"}


class PositionData(CoreData):
    _renamed = {}


class EventData(CoreData):
    _renamed = {"eventType": "type", "teamId": "side", "pointCaptured": "capturedPoint", "assistingParticipantIds": "assistingParticipants", "skillSlot": "skill"}


class ParticipantFrameData(CoreData):
    _renamed = {"totalGold": "goldEarned", "participantId": "participant_id", "currentGold": "gold", "minionsKilled": "creepScore", "Xp": "experience", "jungleMinionsKilled": "NeutralMinionsKilled"}

    def __call__(self, **kwargs):
        if "position" in kwargs:
            self.position = PositionData(**kwargs.pop("position"))
        super().__call__(**kwargs)
        return self


class FrameData(CoreData):
    _renamed = {"participantFrames": "_participant_frames", "events": "_events"}

    def __call__(self, **kwargs):
        if "events" in kwargs:
            self.events = [EventData(**event) for event in kwargs.pop("events")]
        # TODO Implement participant frames here
        #if "participantFrames" in kwargs:
        super().__call__(**kwargs)
        return self

    #@property
    #def participant_frames(self) -> Dict[int, ParticipantFrameData]:
    #    return {k: ParticipantFrameData(**v) for k, v in self._participant_frames.items()}


class TimelineData(CoreData):
    _dto_type = dto.TimelineDto
    _renamed = {"matchId": "id", "frameInterval": "frame_interval"}

    def __call__(self, **kwargs):
        if "frames" in kwargs:
            self.frames = [FrameData(**frame) for frame in kwargs.pop("frames")]
        super().__call__(**kwargs)
        return self


class ParticipantTimelineData(CoreData):
    _renamed = {"participantId": "id", "csDiffPerMinDeltas": "cs_diff_per_min_deltas", "goldPerMinDeltas": "gold_per_min_deltas", "xpDiffPerMinDeltas": "xp_pdiff_per_min_deltas", "creepsPerMinDeltas": "creeps_per_min_deltas", "damageTakenDiffPerMinDeltas": "damage_taken_diff_per_min_deltas", "damageTakenPerMinDeltas": "damage_taken_per_min_deltas"}

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
                    stats.pop("perk5"): [stats.pop("perk5Var1"), stats.pop("perk5Var2"), stats.pop("perk5Var3")]
                }
                stats.pop("runes", None)
            self.stats = ParticipantStatsData(**stats)
        if "timeline" in kwargs:
            self.timeline = ParticipantTimelineData(**kwargs.pop("timeline"))
        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))

        if "player" in kwargs:
            for key, value in kwargs.pop("player").items():
                kwargs[key] = value
        if "platformId" in kwargs:
            if kwargs["platformId"] == "NA":
                kwargs["platformId"] = "NA1"
            self.platform = Platform(kwargs.pop("platformId"))
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
    _renamed = {"account_id": "accountId", "gameId": "id", "champion": "championId"}

    def __call__(self, **kwargs):
        if "season" in kwargs:
            self.season = Season.from_id(kwargs.pop("season"))
        if "queue" in kwargs:
            self.queue = Queue.from_id(kwargs.pop("queue"))
        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))
        if "timestamp" in kwargs:
            self.creation = datetime.datetime.fromtimestamp(kwargs.pop("timestamp") / 1000)
        if "platformId" in kwargs:
            self.platform = Platform(kwargs.pop("platformId"))
        super().__call__(**kwargs)
        return self


class MatchData(CoreData):
    _dto_type = dto.MatchDto
    _renamed = {"gameId": "id", "gameVersion": "version", "gameMode": "mode", "gameType": "type"}

    def __call__(self, **kwargs):
        if "gameCreation" in kwargs:
            self.creation = datetime.datetime.fromtimestamp(kwargs["gameCreation"] / 1000)
        if "gameDuration" in kwargs:
            self.duration = datetime.timedelta(seconds=kwargs["gameDuration"])

        if "participants" in kwargs:
            for participant in kwargs["participants"]:
                for pid in kwargs["participantIdentities"]:
                    if participant["participantId"] == pid["participantId"]:
                        participant["player"] =  pid["player"]
                        break
            self.participants = []
            for i in range(len(kwargs["participants"])):
                for participant in kwargs["participants"]:
                    if i == participant["participantId"] - 1:
                        participant = ParticipantData(**participant)
                        self.participants.append(participant)
                        break
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


class MatchHistory(CassiopeiaLazyList):
    """The match history for a summoner. By default, this will return the entire match history."""
    _data_types = {MatchListGenerator}

    @provide_default_region
    def __init__(self, *, summoner: Union[Summoner, str, int] = None, account_id: int = None, region: Union[Region, str] = None, begin_index: int = None, end_index: int = None, begin_time: datetime.datetime = None, end_time: datetime.datetime = None, queues: Set[Queue] = None, seasons: Set[Season] = None, champions: Set[Champion] = None):
        assert end_index is None or end_index > begin_index
        if begin_time is not None and end_time is None:
            raise ValueError("Both `begin_time` and `end_time` must be specified, or neither.")
        if begin_time is not None and end_time is not None and begin_time > end_time:
            raise ValueError("`end_time` should be greater than `begin_time`")
        #if begin_time is not None and end_index is not None:
        #    raise ValueError("Only one of `*_time` or `*_index` can be specified. If you wish to use a truncated match history within a specific timeframe, specify the timeframe then only use the number of matches you need.")
        kwargs = {"region": region}
        kwargs["queues"] = queues or []
        kwargs["seasons"] = seasons or []
        champions = champions or []
        kwargs["championIds"] = [champion.id if isinstance(champion, Champion) else champion for champion in champions]
        kwargs["begin_index"] = begin_index
        kwargs["end_index"] = end_index
        if begin_time is not None and not isinstance(begin_time, (int, float)):
            begin_time = begin_time.timestamp() * 1000
        kwargs["begin_time"] = begin_time
        if end_time is not None and not isinstance(end_time, (int, float)):
            end_time = end_time.timestamp() * 1000
        kwargs["end_time"] = end_time
        if account_id is not None and summoner is None:
            summoner = Summoner(account=account_id, region=region)
        elif isinstance(summoner, int):
            summoner = Summoner(id=summoner, region=region)
        elif isinstance(summoner, str):
            summoner = Summoner(name=summoner, region=region)
        assert isinstance(summoner, Summoner)
        self.__class__.summoner.fget._lazy_set(self, summoner)
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    @provide_default_region
    def __get_query_from_kwargs__(cls, *, summoner: Union[Summoner, str, int] = None, account_id: int = None, region: Union[Region, str] = None, begin_index: int = None, end_index: int = None, begin_time: datetime.datetime = None, end_time: datetime.datetime = None, queues: Set[Queue] = None, seasons: Set[Season] = None, champions: Set[Champion] = None):
        query = {"region": region}
        if account_id is not None:
            query["account.id"] = account_id
        else:
            if isinstance(summoner, Summoner):
                query["account.id"] = summoner.account.id
                query["summoner"] = summoner  # Tack the summoner on to the generator... See notes in transformers/match.py
            elif isinstance(summoner, str):
                summoner = Summoner(name=summoner, region=region)
                query["account.id"] = summoner.account.id
                query["summoner"] = summoner  # Tack the summoner on to the generator... See notes in transformers/match.py
            else:  # int
                summoner = Summoner(id=summoner, region=region)
                query["account.id"] = summoner.account.id
                query["summoner"] = summoner  # Tack the summoner on to the generator... See notes in transformers/match.py

        if begin_index is not None:
            query["beginIndex"] = begin_index

        if end_index is not None:
            query["endIndex"] = end_index

        if begin_time is not None:
            if isinstance(begin_time, datetime.datetime):
                begin_time = int(begin_time.timestamp() * 1000)
            query["beginTime"] = begin_time

        if end_time is not None:
            if isinstance(end_time, datetime.datetime):
                end_time = int(end_time.timestamp() * 1000)
            query["endTime"] = end_time

        if queues is not None:
            query["queues"] = queues

        if seasons is not None:
            query["seasons"] = seasons

        if champions is not None:
            champions = [champion.id if isinstance(champion, Champion) else champion for champion in champions]
            query["champion.ids"] = champions

        return query

    def __get_query__(self):
        query = {"platform": self.platform, "account.id": self.summoner.account.id}
        if self.queues is not None:
            query["queues"] = self.queues
        if self.seasons is not None:
            query["seasons"] = self.seasons
        if self.champions is not None:
            query["champions"] = self.champions
        if self.begin_time is not None:
            query["beginTime"] = int(self.begin_time.timestamp() * 1000)
        if self.end_time is not None:
            query["endTime"] = int(self.end_time.timestamp() * 1000)
        if self.begin_index is not None:
            query["beginIndex"] = self.begin_index
        if self.end_index is not None:
            query["endIndex"] = self.end_index
        return query

    @classmethod
    def from_generator(cls, generator: Generator, **kwargs):
        self = cls.__new__(cls)
        CassiopeiaLazyList.__init__(self, generator=generator, **kwargs)
        return self

    @lazy_property
    def summoner(self) -> Summoner:
        return Summoner(account=self._data[MatchListGenerator].accountId, region=self.region)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[MatchListGenerator].region)

    @lazy_property
    def platform(self) -> Platform:
        return self.region.platform

    @lazy_property
    def queues(self) -> Set[Queue]:
        return {Queue(q) for q in self._data[MatchListGenerator].queues}

    @lazy_property
    def seasons(self) -> Set[Season]:
        return {Season(s) for s in self._data[MatchListGenerator].seasons}

    @lazy_property
    def champions(self) -> Set[Champion]:
        return {Champion(id=cid, region=self.region) for cid in self._data[MatchListGenerator].championIds}

    @property
    def begin_index(self) -> Union[int, None]:
        try:
            return self._data[MatchListGenerator].beginIndex
        except AttributeError:
            return None

    @property
    def end_index(self) -> Union[int, None]:
        try:
            return self._data[MatchListGenerator].endIndex
        except AttributeError:
            return None

    @property
    def begin_time(self) -> datetime.datetime:
        time = self._data[MatchListGenerator].begin_time
        if time is not None:
            return datetime.datetime.fromtimestamp(time / 1000)

    @property
    def end_time(self) -> datetime.datetime:
        time = self._data[MatchListGenerator].end_time
        if time is not None:
            return datetime.datetime.fromtimestamp(time / 1000)


class Position(CassiopeiaObject):
    _data_types = {PositionData}

    @property
    def x(self) -> int:
        return self._data[PositionData].x

    @property
    def y(self) -> int:
        return self._data[PositionData].y


@searchable({str: ["type", "tower_type", "ascended_type", "ward_type", "monster_type", "type", "monster_sub_type", "lane_type", "building_type"]})
class Event(CassiopeiaObject):
    _data_types = {EventData}

    @property
    def type(self) -> str:
        return self._data[EventData].type

    @property
    def tower_type(self) -> str:
        return self._data[EventData].tower_type

    @property
    def team_id(self) -> int:
        return self._data[EventData].team_id

    @property
    def ascended_type(self) -> str:
        return self._data[EventData].ascended_type

    @property
    def killer_id(self) -> int:
        return self._data[EventData].killer_id

    @property
    def level_up_type(self) -> str:
        return self._data[EventData].level_up_type

    @property
    def captured_point(self) -> str:
        return self._data[EventData].capturedPoint

    @property
    def assisting_participants(self) -> List[int]:
        return self._data[EventData].assistingParticipants

    @property
    def ward_type(self) -> str:
        return self._data[EventData].ward_type

    @property
    def monster_type(self) -> str:
        return self._data[EventData].monster_type

    @property
    def type(self) -> List[str]:
        """Legal values: CHAMPION_KILL, WARD_PLACED, WARD_KILL, BUILDING_KILL, ELITE_MONSTER_KILL, ITEM_PURCHASED, ITEM_SOLD, ITEM_DESTROYED, ITEM_UNDO, SKILL_LEVEL_UP, ASCENDED_EVENT, CAPTURE_POINT, PORO_KING_SUMMON"""
        return self._data[EventData].type

    @property
    def skill(self) -> int:
        return self._data[EventData].skill

    @property
    def victim_id(self) -> int:
        return self._data[EventData].victim_id

    @property
    def timestamp(self) -> int:
        return self._data[EventData].timestamp

    @property
    def after_id(self) -> int:
        return self._data[EventData].after_id

    @property
    def monster_sub_type(self) -> str:
        return self._data[EventData].monster_sub_type

    @property
    def lane_type(self) -> str:
        return self._data[EventData].lane_type

    @property
    def item_id(self) -> int:
        return self._data[EventData].item_id

    @property
    def participant_id(self) -> int:
        return self._data[EventData].participant_id

    @property
    def building_type(self) -> str:
        return self._data[EventData].building_type

    @property
    def creator_id(self) -> int:
        return self._data[EventData].creator_id

    @property
    def position(self) -> Position:
        return Position.from_data(self._data[EventData].position)

    @property
    def before_id(self) -> int:
        return self._data[EventData].before_id


class ParticipantFrame(CassiopeiaObject):
    _data_types = {ParticipantFrameData}

    @property
    def total_gold(self) -> int:
        return self._data[ParticipantFrameData].total_gold

    @property
    def team_score(self) -> int:
        return self._data[ParticipantFrameData].team_score

    @property
    def participant_id(self) -> int:
        return self._data[ParticipantFrameData].participant_id

    @property
    def level(self) -> int:
        return self._data[ParticipantFrameData].level

    @property
    def current_gold(self) -> int:
        return self._data[ParticipantFrameData].current_gold

    @property
    def minions_killed(self) -> int:
        return self._data[ParticipantFrameData].minions_killed

    @property
    def dominion_score(self) -> int:
        return self._data[ParticipantFrameData].dominion_score

    @property
    def position(self) -> Position:
        return Position.from_data(self._data[ParticipantFrameData].position)

    @property
    def xp(self) -> int:
        return self._data[ParticipantFrameData].xp

    @property
    def jungle_minions_killed(self) -> int:
        return self._data[ParticipantFrameData].jungle_minions_killed


class Frame(CassiopeiaObject):
    _data_types = {FrameData}

    @property
    def timestamp(self) -> int:
        return self._data[FrameData].timestamp

    @property
    def participant_frames(self) -> Dict[int, ParticipantFrame]:
        return SearchableDictionary({k: ParticipantFrame.from_data(frame) for k, frame in self._data[FrameData].participant_frames.items()})

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


class ParticipantTimeline(CassiopeiaObject):
    _data_types = {ParticipantTimelineData}

    # TODO Add lane and role enums and make things searchable by them
    @property
    def lane(self) -> str:
        return Lane.from_match_naming_scheme(self._data[ParticipantTimelineData].lane)

    @property
    def role(self) -> Union[str, Role]:
        role = self._data[ParticipantTimelineData].role
        if role == "NONE":
            role = None
        elif role == "SOLO":
            role = "SOLO"
        elif role == "DUO":
            role = "DUO"
        else:
            role = Role.from_match_naming_scheme(role)
        return role

    @property
    def id(self) -> int:
        return self._data[ParticipantTimelineData].id

    @property
    def cs_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].cs_diff_per_min_deltas

    @property
    def gold_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].gold_per_min_deltas

    @property
    def xp_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xp_diff_per_min_deltas

    @property
    def creeps_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].creeps_per_min_deltas

    @property
    def xp_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].xp_per_min_deltas

    @property
    def damage_taken_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damage_taken_per_min_deltas

    @property
    def damage_taken_diff_per_min_deltas(self) -> Dict[str, float]:
        return self._data[ParticipantTimelineData].damage_taken_diff_per_min_deltas


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
        try:
            return (self.kills + self.assists) / self.deaths
        except ZeroDivisionError:
            return self.kills + self.assists

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
        return SearchableList([Item(id=id, version=version, region=self.__match.region) for id in ids if id])

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
    def champion_level(self) -> int:
        return self._data[ParticipantStatsData].championLevel

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
        return self._data[ParticipantStatsData].time_CCingOthers

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

    @lazy_property
    @load_match_on_attributeerror
    def stats(self) -> ParticipantStats:
        return ParticipantStats.from_data(self._data[ParticipantData].stats, match=self.__match, participant=self)

    @property
    def id(self) -> int:
        return self._data[ParticipantData].id

    @lazy_property
    @load_match_on_attributeerror
    def is_bot(self) -> bool:
        return self._data[ParticipantData].isBot

    @lazy_property
    @load_match_on_attributeerror
    def runes(self) -> Dict["Rune", int]:
        version = _choose_staticdata_version(self.__match)
        return SearchableDictionary({Rune(id=rune_id, version=version, region=self.__match.region): perk_vars
            for rune_id, perk_vars in self._data[ParticipantData].runes.items()})

    @lazy_property
    @load_match_on_attributeerror
    def timeline(self) -> ParticipantTimeline:
        return ParticipantTimeline.from_data(self._data[ParticipantData].timeline)

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
    def summoner(self) -> "Summoner":
        kwargs = {}
        try:
            kwargs["id"] = self._data[ParticipantData].summonerId
        except AttributeError:
            pass
        try:
            kwargs["name"] = self._data[ParticipantData].summonerName
        except AttributeError:
            pass
        from .summoner import Summoner
        kwargs["account"] = self._data[ParticipantData].accountId
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


@searchable({str: ["participants"], bool: ["win"]})
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
        return [Champion(id=champion_id, version=self.__match.version, region=self.__match.region) if champion_id != -1 else None for champion_id in self._data[TeamData].bans]

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


@searchable({str: ["participants", "region", "platform", "season", "queue", "mode", "map", "type"], Region: ["region"], Platform: ["platform"], Season: ["season"], Queue: ["queue"], GameMode: ["mode"], Map: ["map"], GameType: ["type"], Item: ["participants"], Champion: ["participants"]})
class Match(CassiopeiaGhost):
    _data_types = {MatchData}

    @provide_default_region
    def __init__(self, *, id: int = None, region: Union[Region, str] = None):
        kwargs = {"region": region, "id": id}
        super().__init__(**kwargs)
        self.__participants = []  # For lazy-loading the participants in a special way

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform, "id": self.id}

    @classmethod
    def from_match_reference(cls, ref: MatchReferenceData):
        instance = cls(id=ref.id, region=ref.region)
        # The below line is necessary because it's possible to pull this match from the cache (which has Match core objects in it).
        # In that case, the data will already be loaded and we don't want to overwrite anything.
        if not hasattr(instance._data[MatchData], "participants"):
            participant = {"participantId": 1, "championId": ref.championId, "stats": {"lane": ref.lane, "role": ref.role}}
            player = {"participantId": 1, "accountId": ref.accountId, "currentPlatformId": ref.platform}
            instance(season=ref.season, queue=ref.queue, creation=ref.creation)
            instance._data[MatchData](participants=[participant],
                                      participantIdentities=[{"participantId": 1, "player": player, "bot": False}])
        return instance

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
        return Timeline(id=self.id, region=self.region.value)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def season(self) -> Season:
        return Season.from_id(self._data[MatchData].seasonId)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue.from_id(self._data[MatchData].queueId)

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
                    participant = Participant.from_data(p, match=self)
                    match.__participants.append(participant)
                    yield participant

            # Create all the participants if any haven't been created yet.
            # Note that it's important to overwrite the one from the matchref if it was loaded because we have more data after we load the full match.
            if empty_match or yielded_one or len(match.__participants) < len(match._data[MatchData].participants):
                if not match._Ghost__is_loaded(MatchData):
                    match.__load__(MatchData)
                    match._Ghost__set_loaded(MatchData)  # __load__ doesn't trigger __set_loaded. is this a "bug"?
                for i, p in enumerate(match._data[MatchData].participants):
                    participant = Participant.from_data(p, match=self)
                    # If we already have this participant in the list, replace it so it stays in the same position
                    for j, pold in enumerate(self.__participants):
                        if pold._data[ParticipantData].accountId == participant._data[ParticipantData].accountId:
                            self.__participants[j] = participant
                            break
                    else:
                        self.__participants.append(participant)

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
        version = ".".join(self.version.split(".")[:2])
        patch = Patch.from_str(version, region=self.region)
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
    def creation(self) -> datetime.datetime:
        return self._data[MatchData].creation
