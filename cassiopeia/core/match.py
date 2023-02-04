import functools
import arrow
import datetime
import itertools
from collections import Counter
from typing import List, Dict, Union, Generator, Optional

from datapipelines import NotFoundError
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import (
    searchable,
    SearchableList,
    SearchableLazyList,
    SearchableDictionary,
)

from .. import configuration
from .staticdata import Versions
from ..data import (
    Region,
    Platform,
    Continent,
    Tier,
    GameType,
    GameMode,
    MatchType,
    Queue,
    Side,
    Lane,
    Role,
    Key,
    SummonersRiftArea,
    Tower,
)
from .common import (
    CoreData,
    CoreDataList,
    CassiopeiaObject,
    CassiopeiaGhost,
    CassiopeiaLazyList,
    ghost_load_on,
)
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
                old_participant = getattr(
                    self, "_{}__participant".format(self.__class__.__name__)
                )
            else:
                raise RuntimeError("Impossible!")
            for participant in match.participants:
                if participant.summoner.name == old_participant.summoner.name:
                    if isinstance(self, Participant):
                        self._data[ParticipantData] = participant._data[ParticipantData]
                    elif isinstance(self, ParticipantStats):
                        self._data[ParticipantStatsData] = participant.stats._data[
                            ParticipantStatsData
                        ]
                    return method(self, *args, **kwargs)
        return method(self, *args, **kwargs)

    return wrapper


_staticdata_to_version_mapping = {}


def _choose_staticdata_version(match):
    # If we want to pull the data for the correct version, we need to pull the entire match data.
    # However, we can use the creation date (which comes with a matchref) and get the ~ patch and therefore extract the version from the patch.
    if (
        configuration.settings.version_from_match is None
        or configuration.settings.version_from_match == "latest"
    ):
        return None  # Rather than pick the latest version here, let the obj handle it so it knows which endpoint within the realms data to use

    if configuration.settings.version_from_match == "version" or hasattr(
        match._data[MatchData], "version"
    ):
        majorminor = match.patch.major + "." + match.patch.minor
    elif configuration.settings.version_from_match == "patch":
        patch = Patch.from_date(match.creation, region=match.region)
        majorminor = patch.majorminor
    else:
        raise ValueError(
            "Unknown value for setting `version_from_match`:",
            configuration.settings.version_from_match,
        )

    try:
        version = _staticdata_to_version_mapping[majorminor]
    except KeyError:
        if int(match.patch.major) >= 10:
            versions = Versions(region=match.region)
            # use the first major.minor.x matching occurrence from the versions list
            version = next(
                x for x in versions if ".".join(x.split(".")[:2]) == majorminor
            )
        else:
            version = majorminor + ".1"  # use major.minor.1
        _staticdata_to_version_mapping[majorminor] = version
    return version


##############
# Data Types #
##############


class MatchListData(CoreDataList):
    _dto_type = dto.MatchListDto
    _renamed = {}


class PositionData(CoreData):
    _renamed = {}


class EventData(CoreData):
    _renamed = {
        "eventType": "type",
        "teamId": "side",
        "pointCaptured": "capturedPoint",
        "assistingParticipantIds": "assistingParticipants",
        "skillSlot": "skill",
    }

    def __call__(self, **kwargs):
        if "position" in kwargs:
            self.position = PositionData(**kwargs.pop("position"))
        super().__call__(**kwargs)
        return self


class ParticipantFrameData(CoreData):
    _renamed = {
        "totalGold": "goldEarned",
        "minionsKilled": "creepScore",
        "xp": "experience",
        "jungleMinionsKilled": "neutralMinionsKilled",
    }

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
            self.participantFrames = {
                int(key): ParticipantFrameData(**pframe)
                for key, pframe in kwargs.pop("participantFrames").items()
            }
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
        # timeline.setCreepScore(getStatTotals(item.getCreepsPerMinDeltas(), durationInSeconds));
        # timeline.setCreepScoreDifference(getStatTotals(item.getCsDiffPerMinDeltas(), durationInSeconds));
        # timeline.setDamageTaken(getStatTotals(item.getDamageTakenPerMinDeltas(), durationInSeconds));
        # timeline.setDamageTakenDifference(getStatTotals(item.getDamageTakenDiffPerMinDeltas(), durationInSeconds));
        # timeline.setExperience(getStatTotals(item.getXpPerMinDeltas(), durationInSeconds));
        # timeline.setExperienceDifference(getStatTotals(item.getXpDiffPerMinDeltas(), durationInSeconds));
        super().__call__(**kwargs)
        return self


class ParticipantStatsData(CoreData):
    _renamed = {}


class ParticipantData(CoreData):
    _renamed = {
        "summoner1Id": "summonerSpellDId",
        "summoner2Id": "summonerSpellFId",
        "bot": "isBot",
        "profileIcon": "profileIconId",
        "gameEndedInEarlySurrender": "endedInEarlySurrender",
        "gameEndedInSurrender": "endedInSurrender",
    }

    def __call__(self, **kwargs):
        perks = kwargs.pop("perks", {})
        stat_perks = perks.pop("statPerks", {})
        # We're going to drop some info about the perks here because that info is already available from the static data
        styles = perks.pop("styles", [])
        selections = list(itertools.chain(*[s.get("selections", []) for s in styles]))
        self.perks = {
            s["perk"]: [s.pop("var1"), s.pop("var2"), s.pop("var3")] for s in selections
        }
        self.stat_perks = stat_perks
        non_stats = {
            "championId": kwargs.get("championId", None),
            "championName": kwargs.get("championName", None),
            "gameEndedInEarlySurrender": kwargs.get("gameEndedInEarlySurrender", None),
            "gameEndedInSurrender": kwargs.get("gameEndedInSurrender", None),
            "individualPosition": kwargs.get("individualPosition", None),
            "participantId": kwargs.get("participantId", None),
            "profileIcon": kwargs.get("profileIcon", None),
            "puuid": kwargs.get("puuid", None),
            "riotIdName": kwargs.get("riotIdName", None),
            "riotIdTagLine": kwargs.get("riotIdTagline", None),
            "summoner1Id": kwargs.get("summoner1Id", None),
            "summoner2Id": kwargs.get("summoner2Id", None),
            "summonerId": kwargs.get("summonerId", None),
            "summonerLevel": kwargs.pop("summonerLevel", None),
            "summonerName": kwargs.get("summonerName", None),
            "teamEarlySurrendered": kwargs.get("teamEarlySurrendered", None),
            "teamId": kwargs.get("teamId", None),
            "teamPosition": kwargs.get("teamPosition", None),
        }
        stats = {
            "assists": kwargs.pop("assists", None),
            "baronKills": kwargs.pop("baronKills", None),
            "bountyLevel": kwargs.pop("bountyLevel", None),
            "champExperience": kwargs.pop("champExperience", None),
            "champLevel": kwargs.pop("champLevel", None),
            "championTransform": kwargs.pop("championTransform", None),
            "consumablesPurchased": kwargs.pop("consumablesPurchased", None),
            "damageDealtToBuildings": kwargs.pop("damageDealtToBuildings", None),
            "damageDealtToObjectives": kwargs.pop("damageDealtToObjectives", None),
            "damageDealtToTurrets": kwargs.pop("damageDealtToTurrets", None),
            "damageSelfMitigated": kwargs.pop("damageSelfMitigated", None),
            "deaths": kwargs.pop("deaths", None),
            "detectorWardsPlaced": kwargs.pop("detectorWardsPlaced", None),
            "doubleKills": kwargs.pop("doubleKills", None),
            "dragonKills": kwargs.pop("dragonKills", None),
            "firstBloodAssist": kwargs.pop("firstBloodAssist", None),
            "firstBloodKill": kwargs.pop("firstBloodKill", None),
            "firstTowerAssist": kwargs.pop("firstTowerAssist", None),
            "firstTowerKill": kwargs.pop("firstTowerKill", None),
            "goldEarned": kwargs.pop("goldEarned", None),
            "goldSpent": kwargs.pop("goldSpent", None),
            "inhibitorKills": kwargs.pop("inhibitorKills", None),
            "inhibitorTakedowns": kwargs.pop("inhibitorTakedowns", None),
            "inhibitorsLost": kwargs.pop("inhibitorsLost", None),
            "item0": kwargs.pop("item0", None),
            "item1": kwargs.pop("item1", None),
            "item2": kwargs.pop("item2", None),
            "item3": kwargs.pop("item3", None),
            "item4": kwargs.pop("item4", None),
            "item5": kwargs.pop("item5", None),
            "item6": kwargs.pop("item6", None),
            "itemsPurchased": kwargs.pop("itemsPurchased", None),
            "killingSprees": kwargs.pop("killingSprees", None),
            "kills": kwargs.pop("kills", None),
            "lane": kwargs.pop("lane", None),
            "largestCriticalStrike": kwargs.pop("largestCriticalStrike", None),
            "largestKillingSpree": kwargs.pop("largestKillingSpree", None),
            "largestMultiKill": kwargs.pop("largestMultiKill", None),
            "longestTimeSpentLiving": kwargs.pop("longestTimeSpentLiving", None),
            "magicDamageDealt": kwargs.pop("magicDamageDealt", None),
            "magicDamageDealtToChampions": kwargs.pop(
                "magicDamageDealtToChampions", None
            ),
            "magicDamageTaken": kwargs.pop("magicDamageTaken", None),
            "neutralMinionsKilled": kwargs.pop("neutralMinionsKilled", None),
            "nexusKills": kwargs.pop("nexusKills", None),
            "nexusLost": kwargs.pop("nexusLost", None),
            "nexusTakedowns": kwargs.pop("nexusTakedowns", None),
            "objectivesStolen": kwargs.pop("objectivesStolen", None),
            "objectivesStolenAssists": kwargs.pop("objectivesStolenAssists", None),
            "pentaKills": kwargs.pop("pentaKills", None),
            "physicalDamageDealt": kwargs.pop("physicalDamageDealt", None),
            "physicalDamageDealtToChampions": kwargs.pop(
                "physicalDamageDealtToChampions", None
            ),
            "physicalDamageTaken": kwargs.pop("physicalDamageTaken", None),
            "quadraKills": kwargs.pop("quadraKills", None),
            "role": kwargs.pop("role", None),
            "sightWardsBoughtInGame": kwargs.pop("sightWardsBoughtInGame", None),
            "spell1Casts": kwargs.pop("spell1Casts", None),
            "spell2Casts": kwargs.pop("spell2Casts", None),
            "spell3Casts": kwargs.pop("spell3Casts", None),
            "spell4Casts": kwargs.pop("spell4Casts", None),
            "summoner1Casts": kwargs.pop("summoner1Casts", None),
            "summoner2Casts": kwargs.pop("summoner2Casts", None),
            "timeCCingOthers": kwargs.pop("timeCCingOthers", None),
            "timePlayed": kwargs.pop("timePlayed", None),
            "totalDamageDealt": kwargs.pop("totalDamageDealt", None),
            "totalDamageDealtToChampions": kwargs.pop(
                "totalDamageDealtToChampions", None
            ),
            "totalDamageShieldedOnTeammates": kwargs.pop(
                "totalDamageShieldedOnTeammates", None
            ),
            "totalDamageTaken": kwargs.pop("totalDamageTaken", None),
            "totalHeal": kwargs.pop("totalHeal", None),
            "totalHealsOnTeammates": kwargs.pop("totalHealsOnTeammates", None),
            "totalMinionsKilled": kwargs.pop("totalMinionsKilled", None),
            "totalTimeCCDealt": kwargs.pop("totalTimeCCDealt", None),
            "totalTimeSpentDead": kwargs.pop("totalTimeSpentDead", None),
            "totalUnitsHealed": kwargs.pop("totalUnitsHealed", None),
            "tripleKills": kwargs.pop("tripleKills", None),
            "trueDamageDealt": kwargs.pop("trueDamageDealt", None),
            "trueDamageDealtToChampions": kwargs.pop(
                "trueDamageDealtToChampions", None
            ),
            "trueDamageTaken": kwargs.pop("trueDamageTaken", None),
            "turretKills": kwargs.pop("turretKills", None),
            "turretTakedowns": kwargs.pop("turretTakedowns", None),
            "turretsLost": kwargs.pop("turretsLost", None),
            "unrealKills": kwargs.pop("unrealKills", None),
            "visionScore": kwargs.pop("visionScore", None),
            "visionWardsBoughtInGame": kwargs.pop("visionWardsBoughtInGame", None),
            "wardsKilled": kwargs.pop("wardsKilled", None),
            "wardsPlaced": kwargs.pop("wardsPlaced", None),
            "win": kwargs.pop("win", None),
        }
        self.stats = ParticipantStatsData(**stats)

        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))

        super().__call__(**kwargs)
        return self


class BanData(CoreData):
    _renamed = {}


class ObjectiveData(CoreData):
    _renamed = {}


class TeamData(CoreData):
    _renamed = {
        "dominionVictoryScore": "dominionScore",
        "firstBaron": "firstBaronKiller",
        "firstBlood": "firstBloodKiller",
        "firstDragon": "firstDragonKiller",
        "firstInhibitor": "firstInhibitorKiller",
        "firstRiftHerald": "firstRiftHeraldKiller",
        "firstTower": "firstTowerKiller",
    }

    def __call__(self, **kwargs):
        self.bans = [BanData(**ban) for ban in kwargs.pop("bans", [])]
        self.objectives = {
            key: ObjectiveData(**obj)
            for key, obj in kwargs.pop("objectives", {}).items()
        }
        if "win" in kwargs:
            self.isWinner = kwargs.pop("win")
        if "teamId" in kwargs:
            self.side = Side(kwargs.pop("teamId"))
        super().__call__(**kwargs)
        return self


class MatchReferenceData(CoreData):
    _renamed = {"matchId": "id"}


class MatchData(CoreData):
    _dto_type = dto.MatchDto
    _renamed = {
        "gameId": "id",
        "gameVersion": "version",
        "gameMode": "mode",
        "gameType": "type",
        "gameName": "name",
        "queueId": "queue",
        "platformId": "platform",
    }

    def __call__(self, **kwargs):
        if "gameCreation" in kwargs:
            self.creation = arrow.get(kwargs["gameCreation"] / 1000)
        if "gameDuration" in kwargs:
            self.duration = datetime.timedelta(seconds=kwargs["gameDuration"])
        if "gameStartTimestamp" in kwargs:
            self.start = arrow.get(kwargs["gameStartTimestamp"] / 1000)

        participants = kwargs.pop("participants", [])
        puuids = set([p.get("puuid", None) for p in participants])
        self.privateGame = False
        if len(puuids) == 1:
            self.privateGame = True
        self.participants = []
        for participant in participants:
            participant = ParticipantData(
                **participant, platformId=kwargs["platformId"]
            )
            self.participants.append(participant)

        teams = kwargs.pop("teams", [])
        self.teams = []
        for team in teams:
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

    def __init__(
        self,
        *,
        puuid: str,
        continent: Continent = None,
        start_time: arrow.Arrow = None,
        end_time: arrow.Arrow = None,
        queue: Queue = None,
        type: MatchType = None,
        start: int = None,
        count: int = None,
    ):
        if start_time is not None and end_time is not None and start_time > end_time:
            raise ValueError("`end_time` should be greater than `start_time`")
        kwargs = {
            "continent": continent,
            "puuid": puuid,
            "queue": queue,
            "type": type,
            "start": start,
            "count": count,
        }
        if start_time is not None and not isinstance(start_time, (int, float)):
            start_time = start_time.int_timestamp
        kwargs["start_time"] = start_time
        if end_time is not None and not isinstance(end_time, (int, float)):
            end_time = end_time.int_timestamp
        kwargs["end_time"] = end_time
        CassiopeiaObject.__init__(self, **kwargs)

    @classmethod
    def __get_query_from_kwargs__(
        cls,
        *,
        continent: Continent,
        puuid: str,
        start_time: arrow.Arrow = None,
        end_time: arrow.Arrow = None,
        queue: Queue = None,
        type: MatchType = None,
        start: int = None,
        count: int = None,
    ):
        query = {"continent": continent, "puuid": puuid}

        if start is not None:
            query["start"] = start

        if count is not None:
            query["count"] = count

        if start_time is not None:
            if isinstance(start_time, arrow.Arrow):
                start_time = start_time.int_timestamp
            query["startTime"] = start_time

        if end_time is not None:
            if isinstance(end_time, arrow.Arrow):
                end_time = end_time.int_timestamp
            query["endTime"] = end_time

        if queue is not None:
            query["queue"] = queue

        if type is not None:
            query["type"] = type

        return query

    # For type hints
    def __getitem__(self, item: Union[str, int]) -> "Match":
        return super().__getitem__(item)

    @classmethod
    def from_generator(cls, generator: Generator, **kwargs):
        self = cls.__new__(cls)
        CassiopeiaLazyList.__init__(self, generator=generator, **kwargs)
        return self

    def __call__(self, **kwargs) -> "MatchHistory":
        kwargs.setdefault("start", self.start)
        kwargs.setdefault("count", self.count)
        kwargs.setdefault("start_time", self.start_time)
        kwargs.setdefault("end_time", self.end_time)
        kwargs.setdefault("queue", self.queue)
        kwargs.setdefault("type", self.match_type)
        return MatchHistory(**kwargs)

    def continent(self) -> Continent:
        return Continent(self._data[MatchListData].continent)

    def queue(self) -> Queue:
        return Queue(self._data[MatchListData].queue)

    def match_type(self) -> MatchType:
        return MatchType(self._data[MatchData].type)

    @property
    def start(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].start
        except AttributeError:
            return None

    @property
    def count(self) -> Union[int, None]:
        try:
            return self._data[MatchListData].count
        except AttributeError:
            return None

    @property
    def start_time(self) -> arrow.Arrow:
        time = self._data[MatchListData].start_time
        if time is not None:
            return arrow.get(time)

    @property
    def end_time(self) -> arrow.Arrow:
        time = self._data[MatchListData].end_time
        if time is not None:
            return arrow.get(time)


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


@searchable(
    {
        str: [
            "type",
            "tower_type",
            "ascended_type",
            "ward_type",
            "monster_type",
            "type",
            "monster_sub_type",
            "lane_type",
            "building_type",
        ]
    }
)
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
        return datetime.timedelta(seconds=self._data[EventData].timestamp / 1000)

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
        return datetime.timedelta(seconds=self._data[FrameData].timestamp / 1000)

    @property
    def participant_frames(self) -> Dict[int, ParticipantFrame]:
        return SearchableDictionary(
            {
                k: ParticipantFrame.from_data(frame)
                for k, frame in self._data[FrameData].participantFrames.items()
            }
        )

    @property
    def events(self) -> List[Event]:
        return SearchableList(
            [Event.from_data(event) for event in self._data[FrameData].events]
        )


class Timeline(CassiopeiaGhost):
    _data_types = {TimelineData}

    def __init__(
        self,
        *,
        id: int = None,
        region: Union[Region, str] = None,
        platform: Platform = None,
    ):
        if isinstance(region, str):
            region = Region(region)
        if isinstance(platform, str):
            platform = Platform(platform)
        kwargs = {"platform": platform, "id": id}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"platform": self.platform, "id": self.id}

    @property
    def id(self):
        return self._data[TimelineData].id

    @property
    def continent(self) -> Continent:
        return self.platform.continent

    @property
    def region(self) -> Region:
        return self.platform.region

    @property
    def platform(self) -> Platform:
        return Platform(self._data[TimelineData].platform)

    @CassiopeiaGhost.property(TimelineData)
    @ghost_load_on
    def frames(self) -> List[Frame]:
        return SearchableList(
            [Frame.from_data(frame) for frame in self._data[TimelineData].frames]
        )

    @CassiopeiaGhost.property(TimelineData)
    @ghost_load_on
    def frame_interval(self) -> int:
        return self._data[TimelineData].frame_interval

    @property
    def first_tower_fallen(self) -> Event:
        for frame in self.frames:
            for event in frame.events:
                if (
                    event.type == "BUILDING_KILL"
                    and event.building_type == "TOWER_BUILDING"
                ):
                    return event


class ParticipantTimeline(object):
    _data_types = {ParticipantTimelineData}

    @classmethod
    def from_data(cls, match: "Match"):
        self = cls()
        self.__match = match
        return self

    @property
    def frames(self) -> List[ParticipantFrame]:
        timeline: Timeline = self.__match.timeline
        these = []
        for frame in timeline.frames:
            for pid, pframe in frame.participant_frames.items():
                pframe.timestamp = frame.timestamp  # Assign the match's Frame timestamp to the ParticipantFrame
                if pframe.participant_id == self.id:
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
        return self.events.filter(
            lambda event: event.type == "CHAMPION_KILL" and event.killer_id == self.id
        )

    @property
    def champion_deaths(self):
        return self.events.filter(
            lambda event: event.type == "CHAMPION_KILL" and event.victim_id == self.id
        )

    @property
    def champion_assists(self):
        return self.events.filter(
            lambda event: event.type == "CHAMPION_KILL"
            and self.id in event.assisting_participants
        )


class CumulativeTimeline:
    def __init__(self, id: int, participant_timeline: ParticipantTimeline):
        self._id = id
        self._timeline = participant_timeline

    def __getitem__(self, time: Union[datetime.timedelta, str]) -> "ParticipantState":
        if isinstance(time, str):
            time = time.split(":")
            time = datetime.timedelta(minutes=int(time[0]), seconds=int(time[1]))
        state = ParticipantState(
            id=self._id, time=time, participant_timeline=self._timeline
        )
        for event in self._timeline.events:
            if event.timestamp > time:
                break
            state._process_event(event)
        return state


class ParticipantState:
    """The state of a participant at a given point in the timeline."""

    def __init__(
        self,
        id: int,
        time: datetime.timedelta,
        participant_timeline: ParticipantTimeline,
    ):
        self._id = id
        self._time = time
        # self._timeline = participant_timeline
        # Try to get info from the most recent participant timeline object
        latest_frame = None
        for frame in participant_timeline.frames:
            # Round to the nearest second for the frame timestamp because it's off by a few ms
            rounded_frame_timestamp = datetime.timedelta(
                seconds=frame.timestamp.seconds
            )
            if rounded_frame_timestamp > self._time:
                break
            latest_frame = frame
        self._latest_frame: Optional[ParticipantFrame] = latest_frame
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
            # print(f"Did not process event {event.to_dict()}")
            pass
        self._processed_events.append(event)
        self._processed_events.sort(key=lambda event: event.timestamp)

    @property
    def items(self) -> SearchableList:
        return SearchableList(
            [Item(id=id_, region="NA") for id_ in self._item_state._items]
        )

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
        # The latest position is either from the latest event or from the participant timeline frame.
        # Get the most recent frame. This is our baseline.
        latest_frame_ts = self._latest_frame.timestamp
        # Now loop through all events and use the latest event's position if the event was generated later than the frame.
        events = [
            (getattr(event, "timestamp", None), getattr(event, "position", None))
            for event in self._processed_events
        ]
        events_with_ts_and_position = [
            (ts, p)
            for ts, p in events
            if ts is not None and p is not None
        ]
        # If an event exists with both a timestamp and position, and the event was generated later that the frame, return its position.
        if len(events_with_ts_and_position) > 0:
            latest_event_ts, latest_event_position = events_with_ts_and_position[-1]
            if latest_event_ts > latest_frame_ts:
                return latest_event_position
        # If we got this far, then the latest event (if it exists) is not relevant. Return the position from the latest frame.
        return self._latest_frame.position

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
            3850: 3851,
            3851: 3853,  # Spellthief's Edge -> Frostfang -> Shard of True Ice
            3854: 3855,
            3855: 3857,  # Steel Shoulderguards -> Runesteel Spaulders -> Pauldrons of Whiterock
            3858: 3859,
            3859: 3860,  # Relic Shield -> Targon's Buckler -> Bulwark of the Mountain
            3862: 3863,
            3863: 3864,  # Spectral Sickle -> Harrowing Crescent -> Black Mist Scythe
        }
        item_id = getattr(event, "item_id", getattr(event, "before_id", None))
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
            if item in (
                3340,
                3364,
                2319,
                2061,
                2062,
                2056,
                2403,
                2419,
                3400,
                2004,
                2058,
                3200,
                2011,
                2423,
                2055,
                2057,
                2424,
                2059,
                2060,
                2013,
                2421,
                3600,
            ):  # Something weird can happen with trinkets and klepto items
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
    def from_data(
        cls, data: ParticipantStatsData, match: "Match", participant: "Participant"
    ):
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
    def deaths(self) -> int:
        return self._data[ParticipantStatsData].deaths

    @property
    @load_match_on_attributeerror
    def assists(self) -> int:
        return self._data[ParticipantStatsData].assists

    @property
    @load_match_on_attributeerror
    def kills(self) -> int:
        return self._data[ParticipantStatsData].kills

    @property
    @load_match_on_attributeerror
    def baron_kills(self) -> int:
        return self._data[ParticipantStatsData].baronKills

    @property
    @load_match_on_attributeerror
    def bounty_level(self) -> int:
        return self._data[TeamData].bountyLevel

    @property
    @load_match_on_attributeerror
    def champion_experience(self) -> int:
        return self._data[TeamData].championExperience

    @property
    @load_match_on_attributeerror
    def level(self) -> int:
        return self._data[ParticipantStatsData].champLevel

    @load_match_on_attributeerror
    @property
    def champion_transform(self) -> int:
        return self._data[TeamData].championTransform

    @property
    @load_match_on_attributeerror
    def consumables_purchased(self) -> int:
        return self._data[ParticipantStatsData].consumablesPurchased

    @property
    @load_match_on_attributeerror
    def damage_dealt_to_buildings(self) -> int:
        return self._data[ParticipantStatsData].damageDealtToBuildings

    @property
    @load_match_on_attributeerror
    def damage_dealt_to_objectives(self) -> int:
        return self._data[ParticipantStatsData].damageDealtToObjectives

    @property
    @load_match_on_attributeerror
    def damage_dealt_to_turrets(self) -> int:
        return self._data[ParticipantStatsData].damageDealtToTurrets

    @property
    @load_match_on_attributeerror
    def damage_self_mitigated(self) -> int:
        return self._data[ParticipantStatsData].damageSelfMitigated

    @property
    @load_match_on_attributeerror
    def vision_wards_bought(self) -> int:
        return self._data[ParticipantStatsData].visionWardsBoughtInGame

    @property
    @load_match_on_attributeerror
    def vision_wards_placed(self) -> int:
        return self._data[ParticipantStatsData].detectorWardsPlaced

    @property
    @load_match_on_attributeerror
    def double_kills(self) -> int:
        return self._data[ParticipantStatsData].doubleKills

    @property
    @load_match_on_attributeerror
    def dragon_kills(self) -> int:
        return self._data[ParticipantStatsData].dragonKills

    @property
    @load_match_on_attributeerror
    def first_blood_assist(self) -> bool:
        return self._data[ParticipantStatsData].firstBloodAssist

    @property
    @load_match_on_attributeerror
    def first_blood_kill(self) -> bool:
        return self._data[ParticipantStatsData].firstBloodKill

    @property
    @load_match_on_attributeerror
    def first_tower_assist(self) -> bool:
        return self._data[ParticipantStatsData].firstTowerAssist

    @property
    @load_match_on_attributeerror
    def first_tower_kill(self) -> bool:
        return self._data[ParticipantStatsData].firstTowerKill

    @property
    @load_match_on_attributeerror
    def gold_earned(self) -> int:
        return self._data[ParticipantStatsData].goldEarned

    @property
    @load_match_on_attributeerror
    def gold_spent(self) -> int:
        return self._data[ParticipantStatsData].goldSpent

    @property
    @load_match_on_attributeerror
    def inhibitor_kills(self) -> int:
        return self._data[ParticipantStatsData].inhibitorKills

    @property
    @load_match_on_attributeerror
    def inhibitor_takedowns(self) -> int:
        return self._data[ParticipantStatsData].inhibitorTakedowns

    @property
    @load_match_on_attributeerror
    def inhibitors_lost(self) -> int:
        return self._data[ParticipantStatsData].inhibitorsLost

    @lazy_property
    @load_match_on_attributeerror
    def items(self) -> List[Item]:
        ids = [
            self._data[ParticipantStatsData].item0,
            self._data[ParticipantStatsData].item1,
            self._data[ParticipantStatsData].item2,
            self._data[ParticipantStatsData].item3,
            self._data[ParticipantStatsData].item4,
            self._data[ParticipantStatsData].item5,
            self._data[ParticipantStatsData].item6,
        ]
        version = _choose_staticdata_version(self.__match)
        return SearchableList(
            [
                Item(id=id, version=version, region=self.__match.region) if id else None
                for id in ids
            ]
        )

    @property
    @load_match_on_attributeerror
    def items_purchased(self) -> int:
        return self._data[ParticipantStatsData].itemsPurchased

    @property
    @load_match_on_attributeerror
    def killing_sprees(self) -> int:
        return self._data[ParticipantStatsData].killingSprees

    @property
    @load_match_on_attributeerror
    def largest_critical_strike(self) -> int:
        return self._data[ParticipantStatsData].largestCriticalStrike

    @property
    @load_match_on_attributeerror
    def largest_killing_spree(self) -> int:
        return self._data[ParticipantStatsData].largestKillingSpree

    @property
    @load_match_on_attributeerror
    def largest_multi_kill(self) -> int:
        return self._data[ParticipantStatsData].largestMultiKill

    @property
    @load_match_on_attributeerror
    def longest_time_spent_living(self) -> int:
        return self._data[ParticipantStatsData].longestTimeSpentLiving

    @property
    @load_match_on_attributeerror
    def magic_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].magicDamageDealt

    @property
    @load_match_on_attributeerror
    def magic_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].magicDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def magic_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].magicDamageTaken

    @property
    @load_match_on_attributeerror
    def neutral_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].neutralMinionsKilled

    @property
    @load_match_on_attributeerror
    def nexus_kills(self) -> int:
        return self._data[ParticipantStatsData].nexusKills

    @property
    @load_match_on_attributeerror
    def nexus_lost(self) -> int:
        return self._data[ParticipantStatsData].nexusLost

    @property
    @load_match_on_attributeerror
    def nexus_takedowns(self) -> int:
        return self._data[ParticipantStatsData].nexusTakedowns

    @property
    @load_match_on_attributeerror
    def objectives_stolen(self) -> int:
        return self._data[ParticipantStatsData].objectivesStolen

    @property
    @load_match_on_attributeerror
    def objectives_stolen_assists(self) -> int:
        return self._data[ParticipantStatsData].objectivesStolenAssists

    @property
    @load_match_on_attributeerror
    def penta_kills(self) -> int:
        return self._data[ParticipantStatsData].pentaKills

    @property
    @load_match_on_attributeerror
    def physical_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageDealt

    @property
    @load_match_on_attributeerror
    def physical_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def physical_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].physicalDamageTaken

    @property
    @load_match_on_attributeerror
    def quadra_kills(self) -> int:
        return self._data[ParticipantStatsData].quadraKills

    @property
    @load_match_on_attributeerror
    def sight_wards_bought(self) -> int:
        return self._data[ParticipantStatsData].sightWardsBoughtInGame

    @property
    @load_match_on_attributeerror
    def spell_1_casts(self) -> int:
        return self._data[ParticipantStatsData].spell1Casts

    @property
    @load_match_on_attributeerror
    def spell_2_casts(self) -> int:
        return self._data[ParticipantStatsData].spell2Casts

    @property
    @load_match_on_attributeerror
    def spell_3_casts(self) -> int:
        return self._data[ParticipantStatsData].spell3Casts

    @property
    @load_match_on_attributeerror
    def spell_4_casts(self) -> int:
        return self._data[ParticipantStatsData].spell4Casts

    @property
    @load_match_on_attributeerror
    def summoner_spell_1_casts(self) -> int:
        return self._data[ParticipantStatsData].summoner1Casts

    @property
    @load_match_on_attributeerror
    def summoner_spell_2_casts(self) -> int:
        return self._data[ParticipantStatsData].summoner2Casts

    @property
    @load_match_on_attributeerror
    def time_CCing_others(self) -> int:
        return self._data[ParticipantStatsData].timeCCingOthers

    @property
    @load_match_on_attributeerror
    def time_played(self) -> int:
        return self._data[ParticipantStatsData].timePlayed

    @property
    @load_match_on_attributeerror
    def total_damage_dealt(self) -> int:
        return self._data[ParticipantStatsData].totalDamageDealt

    @property
    @load_match_on_attributeerror
    def total_damage_dealt_to_champions(self) -> int:
        return self._data[ParticipantStatsData].totalDamageDealtToChampions

    @property
    @load_match_on_attributeerror
    def total_damage_shielded_on_teammates(self) -> int:
        return self._data[ParticipantStatsData].totalDamageShieldedOnTeammates

    @property
    @load_match_on_attributeerror
    def total_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].totalDamageTaken

    @property
    @load_match_on_attributeerror
    def total_heal(self) -> int:
        return self._data[ParticipantStatsData].totalHeal

    @property
    @load_match_on_attributeerror
    def total_heals_on_teammates(self) -> int:
        return self._data[ParticipantStatsData].totalHealsOnTeammates

    @property
    @load_match_on_attributeerror
    def total_minions_killed(self) -> int:
        return self._data[ParticipantStatsData].totalMinionsKilled

    @property
    @load_match_on_attributeerror
    def total_time_cc_dealt(self) -> int:
        return self._data[ParticipantStatsData].totalTimeCCDealt

    @property
    @load_match_on_attributeerror
    def total_time_spent_dead(self) -> int:
        return self._data[ParticipantStatsData].totalTimeSpentDead

    @property
    @load_match_on_attributeerror
    def total_units_healed(self) -> int:
        return self._data[ParticipantStatsData].totalUnitsHealed

    @property
    @load_match_on_attributeerror
    def triple_kills(self) -> int:
        return self._data[ParticipantStatsData].tripleKills

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
    def true_damage_taken(self) -> int:
        return self._data[ParticipantStatsData].trueDamageTaken

    @property
    @load_match_on_attributeerror
    def turret_kills(self) -> int:
        return self._data[ParticipantStatsData].turretKills

    @property
    @load_match_on_attributeerror
    def turret_takedowns(self) -> int:
        return self._data[ParticipantStatsData].turretTakedowns

    @property
    @load_match_on_attributeerror
    def turrets_lost(self) -> int:
        return self._data[ParticipantStatsData].turretsLost

    @property
    @load_match_on_attributeerror
    def unreal_kills(self) -> int:
        return self._data[ParticipantStatsData].unrealKills

    @property
    @load_match_on_attributeerror
    def vision_score(self) -> int:
        return self._data[ParticipantStatsData].visionScore

    @property
    @load_match_on_attributeerror
    def wards_killed(self) -> int:
        return self._data[ParticipantStatsData].wardsKilled

    @property
    @load_match_on_attributeerror
    def wards_placed(self) -> int:
        return self._data[ParticipantStatsData].wardsPlaced

    @property
    @load_match_on_attributeerror
    def win(self) -> bool:
        return self._data[ParticipantStatsData].win


@searchable(
    {
        str: [
            "summoner",
            "champion",
            "stats",
            "runes",
            "side",
            "summoner_spell_d",
            "summoner_spell_f",
        ],
        Summoner: ["summoner"],
        Champion: ["champion"],
        Side: ["side"],
        Rune: ["runes"],
        SummonerSpell: ["summoner_spell_d", "summoner_spell_f"],
    }
)
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
        version = (
            ".".join(version) + ".1"
        )  # Always use x.x.1 because I don't know how to figure out what the last version number should be.
        return version

    @property
    def individual_position(self) -> Lane:
        return Lane.from_match_naming_scheme(
            self._data[ParticipantData].individualPosition
        )

    @property
    def team_position(self) -> Lane:
        return Lane.from_match_naming_scheme(self._data[ParticipantData].teamPosition)

    @property
    def lane(self) -> Lane:
        return Lane.from_match_naming_scheme(self._data[ParticipantData].individualPosition)

    @property
    def role(self) -> Role:
        return Role.from_match_naming_scheme(self._data[ParticipantData].stats.role)

    @property
    def skill_order(self) -> List[Key]:
        skill_events = self.timeline.events.filter(
            lambda event: event.type == "SKILL_LEVEL_UP"
        )
        skill_events.sort(key=lambda event: event.timestamp)
        skills = [event.skill - 1 for event in skill_events]
        spells = [
            self.champion.spells[Key("Q")],
            self.champion.spells[Key("W")],
            self.champion.spells[Key("E")],
            self.champion.spells[Key("R")],
        ]
        skills = [spells[skill] for skill in skills]
        return skills

    @property
    def ended_in_early_surrender(self) -> bool:
        return self._data[ParticipantData].endedInEarlySurrender

    @lazy_property
    @load_match_on_attributeerror
    def stats(self) -> ParticipantStats:
        return ParticipantStats.from_data(
            self._data[ParticipantData].stats, match=self.__match, participant=self
        )

    @lazy_property
    @load_match_on_attributeerror
    def id(self) -> int:
        if self._data[ParticipantData].participantId is None:
            raise AttributeError
        return self._data[ParticipantData].participantId

    @lazy_property
    @load_match_on_attributeerror
    def is_bot(self) -> bool:
        return self._data[ParticipantData].isBot

    @lazy_property
    @load_match_on_attributeerror
    def runes(self) -> Dict[Rune, int]:
        version = _choose_staticdata_version(self.__match)
        runes = SearchableDictionary(
            {
                Rune(id=rune_id, version=version, region=self.__match.region): perk_vars
                for rune_id, perk_vars in self._data[ParticipantData].perks.items()
            }
        )

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
        runes = SearchableList(
            [
                Rune(id=rune_id, version=version, region=self.__match.region)
                for rune_id in self._data[ParticipantData].stat_perks.values()
            ]
        )
        return runes

    @lazy_property
    @load_match_on_attributeerror
    def timeline(self) -> ParticipantTimeline:
        timeline = ParticipantTimeline.from_data(match=self.__match)
        timeline.id = self.id
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
        return SummonerSpell(
            id=self._data[ParticipantData].summonerSpellDId,
            version=version,
            region=self.__match.region,
        )

    @lazy_property
    @load_match_on_attributeerror
    def summoner_spell_f(self) -> SummonerSpell:
        version = _choose_staticdata_version(self.__match)
        return SummonerSpell(
            id=self._data[ParticipantData].summonerSpellFId,
            version=version,
            region=self.__match.region,
        )

    @lazy_property
    @load_match_on_attributeerror
    def champion(self) -> "Champion":
        # See ParticipantStats for info
        version = _choose_staticdata_version(self.__match)
        return Champion(
            id=self._data[ParticipantData].championId,
            version=version,
            region=self.__match.region,
        )

    # All the summoner data from the match endpoint is passed through to the Summoner class.
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
        kwargs["puuid"] = self._data[ParticipantData].puuid
        kwargs["region"] = Platform(self._data[ParticipantData].platformId).region
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


@searchable(
    {
        str: ["participants"],
        bool: ["win"],
        Champion: ["participants"],
        Summoner: ["participants"],
        SummonerSpell: ["participants"],
    }
)
class Team(CassiopeiaObject):
    _data_types = {TeamData}

    @classmethod
    def from_data(cls, data: CoreData, match: "Match"):
        self = super().from_data(data)
        self.__match = match
        return self

    @property
    def first_dragon(self) -> bool:
        return self._data[TeamData].objectives["dragon"].first

    @property
    def first_inhibitor(self) -> bool:
        return self._data[TeamData].objectives["inhibitor"].first

    @property
    def first_rift_herald(self) -> bool:
        return self._data[TeamData].objectives["riftHerald"].first

    @property
    def first_baron(self) -> bool:
        return self._data[TeamData].objectives["baron"].first

    @property
    def first_tower(self) -> bool:
        return self._data[TeamData].objectives["tower"].first

    @property
    def first_blood(self) -> bool:
        return self._data[TeamData].objectives["champion"].first

    @property
    def bans(self) -> List["Champion"]:
        version = _choose_staticdata_version(self.__match)
        return [
            Champion(id=ban.championId, version=version, region=self.__match.region)
            if ban.championId != -1
            else None
            for ban in self._data[TeamData].bans
        ]

    @property
    def rift_herald_kills(self) -> int:
        return self._data[TeamData].objectives["riftHerald"].kills

    @property
    def baron_kills(self) -> int:
        return self._data[TeamData].objectives["baronKills"].kills

    @property
    def inhibitor_kills(self) -> int:
        return self._data[TeamData].objectives["inhibitor"].kills

    @property
    def tower_kills(self) -> int:
        return self._data[TeamData].objectives["tower"].kills

    @property
    def dragon_kills(self) -> int:
        return self._data[TeamData].objectives["dragonKills"].kills

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
        return SearchableList(
            [
                Participant.from_data(p, match=self.__match)
                for p in self._data[TeamData].participants
            ]
        )


@searchable(
    {
        str: ["participants", "continent", "queue", "mode", "map", "type"],
        Continent: ["continent"],
        Queue: ["queue"],
        MatchType: ["type"],
        GameMode: ["mode"],
        Map: ["map"],
        GameType: ["type"],
        Item: ["participants"],
        Patch: ["patch"],
        Summoner: ["participants"],
        SummonerSpell: ["participants"],
    }
)
class Match(CassiopeiaGhost):
    _data_types = {MatchData}

    def __init__(
        self,
        *,
        id: str = None,
        region: Union[Region, str] = None,
        platform: Union[Platform, str] = None,
    ):
        if isinstance(platform, str):
            platform = Platform(platform)
        if isinstance(region, str):
            region = Region(region)
        if platform is None:
            platform = region.platform
        kwargs = {"platform": platform, "id": id}
        super().__init__(**kwargs)
        self.__participants = []  # For lazy-loading the participants in a special way
        self._timeline = None

    def __get_query__(self):
        return {"platform": self.platform, "id": self.id}

    @classmethod
    def from_match_reference(cls, ref: MatchReferenceData):
        platform, id = ref.id.split("_")
        id = int(id)
        platform = Platform(platform)
        instance = cls(id=id, platform=platform)
        instance._timeline = None
        return instance

    def __eq__(self, other: "Match"):
        if not isinstance(other, Match) or self.continent != other.continent:
            return False
        return self.id == other.id

    def __str__(self):
        return f"Match(id={self.id}, region='{self.continent.value}')"

    __hash__ = CassiopeiaGhost.__hash__

    @lazy_property
    def continent(self) -> Continent:
        """The continent for this match."""
        return self.platform.continent

    @lazy_property
    def region(self) -> Region:
        """The region for this match."""
        return self.platform.region

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def platform(self) -> Platform:
        """The platform for this match."""
        return Platform(self._data[MatchData].platform)

    @property
    def id(self) -> str:
        return self._data[MatchData].id

    @lazy_property
    def timeline(self) -> Timeline:
        if self._timeline is None:
            self._timeline = Timeline(id=self.id, region=self.region)
        return self._timeline

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def queue(self) -> Queue:
        return Queue.from_id(self._data[MatchData].queue)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def type(self) -> MatchType:
        # TODO: this is wrong as type refers to the GameType, we could infer it from the queue
        return MatchType(self._data[MatchData].type)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    def participants(self) -> SearchableList[Participant]:
        if hasattr(self._data[MatchData], "participants"):
            if not self._Ghost__is_loaded(MatchData):
                self.__load__(MatchData)
                self._Ghost__set_loaded(
                    MatchData
                )  # __load__ doesn't trigger __set_loaded.
            # TODO: this is probably not the way to go, but it prevents participants being reappended every time match.participants is called
            if len(self.__participants) == 0:
                for p in self._data[MatchData].participants:
                    participant = Participant.from_data(p, match=self)
                    self.__participants.append(participant)

        else:
            self.__participants = []

        return SearchableList(self.__participants)

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def teams(self) -> List[Team]:
        if not self._Ghost__is_loaded(MatchData):
            self.__load__(MatchData)
            self._Ghost__set_loaded(
                MatchData
            )  # __load__ doesn't trigger __set_loaded.
        return [
            Team.from_data(t, match=self)
            for i, t in enumerate(self._data[MatchData].teams)
        ]

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
    def game_type(self) -> GameType:
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

    @CassiopeiaGhost.property(MatchData)
    @ghost_load_on
    @lazy
    def start(self) -> arrow.Arrow:
        return self._data[MatchData].start

    @property
    def is_remake(self) -> bool:
        for p in self.participants:  # Force a load of the participants
            pass
        # TODO: not sure how this should be handled, it feels like the early surrender state should belong the the match itself, not the participants
        if self.__participants[0] is not None:
            return self.__participants[
                0
            ].ended_in_early_surrender or self.duration < datetime.timedelta(minutes=5)
        else:
            self.duration < datetime.timedelta(minutes=5)

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
            x /= rx1 - rx0
            x *= imx1 - imx0
            y -= ry0
            y /= ry1 - ry0
            y *= imy1 - imy0
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
        plt.axis("off")
        plt.show()
