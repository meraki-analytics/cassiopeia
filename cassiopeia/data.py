from enum import Enum
import arrow


class Region(Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    japan = "JP"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    turkey = "TR"
    russia = "RU"

    @property
    def platform(self) -> "Platform":
        return getattr(Platform, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]

    @staticmethod
    def from_platform(platform):
        try:
            return platform.region
        except AttributeError:
            return Platform(platform).region

    @property
    def timezone(self) -> str:
        tzs = {
            'NA': 'GMT-8',
            'LAN': 'GMT-7',
            'LAS': 'GMT-5',
            'BR': 'GMT-4',
            'EUW': 'GMT-2',
            'TR': 'GMT-0',
            'EUNE': 'GMT+1',
            'RU': 'GMT+3',
            'KR': 'GMT+6',
            'JP': 'GMT+7',
            'OCE': 'GMT+8',
        }
        return tzs[self.value]

    @property
    def continent(self) -> "Continent":
        if self is Region.brazil:
            return Continent.americas
        if self is Region.europe_north_east:
            return Continent.europe
        if self is Region.europe_west:
            return Continent.europe
        if self is Region.japan:
            return Continent.asia
        if self is Region.korea:
            return Continent.asia
        if self is Region.latin_america_north:
            return Continent.americas
        if self is Region.latin_america_south:
            return Continent.americas
        if self is Region.north_america:
            return Continent.americas
        if self is Region.oceania:
            return Continent.asia  # TODO: Correct?
        if self is Region.turkey:
            return Continent.europe
        if self is Region.russia:
            return Continent.europe


class Platform(Enum):
    brazil = "BR1"
    europe_north_east = "EUN1"
    europe_west = "EUW1"
    japan = "JP1"
    korea = "KR"
    latin_america_north = "LA1"
    latin_america_south = "LA2"
    north_america = "NA1"
    oceania = "OC1"
    turkey = "TR1"
    russia = "RU"

    @property
    def region(self) -> "Region":
        return getattr(Region, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]

    @staticmethod
    def from_region(region):
        try:
            return region.platform
        except AttributeError:
            return Region(region).platform

    @property
    def continent(self):
        return self.region.continent


DEFAULT_LOCALE = {
    Region.brazil: "pt_BR",
    Platform.brazil: "pt_BR",
    Region.europe_north_east: "en_GB",
    Platform.europe_north_east: "en_GB",
    Region.europe_west: "en_GB",
    Platform.europe_west: "en_GB",
    Region.japan: "ja_JP",
    Platform.japan: "ja_JP",
    Region.korea: "ko_KR",
    Platform.korea: "ko_KR",
    Region.latin_america_north: "es_MX",
    Platform.latin_america_north: "es_MX",
    Region.latin_america_south: "es_AR",
    Platform.latin_america_south: "es_AR",
    Region.north_america: "en_US",
    Platform.north_america: "en_US",
    Region.oceania: "en_AU",
    Platform.oceania: "en_AU",
    Region.turkey: "tr_TR",
    Platform.turkey: "tr_TR",
    Region.russia: "ru_RU",
    Platform.russia: "ru_RU",
}


class Continent(Enum):
    americas = "AMERICAS"
    asia = "ASIA"
    europe = "EUROPE"


class Key(Enum):
    Q = "Q"
    W = "W"
    E = "E"
    R = "R"


class Resource(Enum):
    mana = "Mana"
    courage = "Courage"
    energy = "Energy"
    fury = "Fury"
    rage = "Rage"
    flow = "Flow"
    ferocity = "Ferocity"
    heat = "Heat"
    shield = "Shield"
    blood_well = "Blood Well"
    crimson_rush = "Crimson Rush"
    none = "None"
    no_cost = "No Cost"


class Side(Enum):
    blue = 100
    red = 200


class MatchType(Enum):  # TODO: Can we combine with GameType somehow?
    ranked = "ranked"
    normal = "normal"
    tourney = "tourney"
    tutorial = "tutorial"


class GameMode(Enum):
    aram = "ARAM"
    ascension = "ASCENSION"
    classic = "CLASSIC"
    showdown = "FIRSTBLOOD"
    poro_king = "KINGPORO"
    dominion = "ODIN"
    one_for_all = "ONEFORALL"
    tutorial = "TUTORIAL"
    tutorial_1 = "TUTORIAL_MODULE_1"
    tutorial_2 = "TUTORIAL_MODULE_2"
    tutorial_3 = "TUTORIAL_MODULE_3"
    nexus_siege = "SIEGE"
    assassinate = "ASSASSINATE"
    dark_star = "DARKSTAR"
    all_random_summoners_rift = "ARSR"
    urf = "URF"
    doom_bots = "DOOMBOTSTEEMO"
    star_guardian = "STARGUARDIAN"
    project = "PROJECT"
    overcharge = "OVERCHARGE"
    all_random_urf_snow = "SNOWURF"
    practice_tool = "PRACTICETOOL"
    nexus_blitz = "NEXUSBLITZ"
    odyssey = "ODYSSEY"
    utlbook = "ULTBOOK"


class MasteryTree(Enum):
    cunning = "Cunning"
    ferocity = "Ferocity"
    resolve = "Resolve"


class Tier(Enum):
    challenger = "CHALLENGER"
    grandmaster = "GRANDMASTER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    iron = "IRON"
    unranked = "UNRANKED"

    def __str__(self):
        return self.name.title()

    @staticmethod
    def _order():
        return {Tier.challenger: 9, Tier.grandmaster: 8, Tier.master: 7,
                Tier.diamond: 6, Tier.platinum: 5, Tier.gold: 4,
                Tier.silver: 3, Tier.bronze: 2, Tier.iron: 1}

    def __lt__(self, other):
        return self._order()[self] < other._order()[other]

    def __gt__(self, other):
        return self._order()[self] > other._order()[other]

    def __le__(self, other):
        return self._order()[self] <= other._order()[other]

    def __ge__(self, other):
        return self._order()[self] >= other._order()[other]


class Division(Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"

    def __str__(self):
        return self.value

    @staticmethod
    def _order():
        return {Division.one: 4, Division.two: 3, Division.three: 2, Division.four: 1}

    def __lt__(self, other):
        return self._order()[self] < other._order()[other]

    def __gt__(self, other):
        return self._order()[self] > other._order()[other]

    def __le__(self, other):
        return self._order()[self] <= other._order()[other]

    def __ge__(self, other):
        return self._order()[self] >= other._order()[other]


class Rank:
    def __init__(self, tier: Tier, division: Division):
        self.tuple = (tier, division)
        self.tier = tier
        self.division = division

    def __str__(self):
        return "<{} {}>".format(self.tuple[0], self.tuple[1])

    def __eq__(self, other):
        return self.tuple == other.tuple

    def __ne__(self, other):
        return self.tuple != other.tuple

    def __lt__(self, other):
        return self.tuple < other.tuple

    def __gt__(self, other):
        return self.tuple > other.tuple

    def __le__(self, other):
        return self.tuple <= other.tuple

    def __ge__(self, other):
        return self.tuple >= other.tuple


class Season(Enum):
    preseason_3 = "PRESEASON3"
    season_3 = "SEASON3"
    preseason_4 = "PRESEASON2014"
    season_4 = "SEASON2014"
    preseason_5 = "PRESEASON2015"
    season_5 = "SEASON2015"
    preseason_6 = "PRESEASON2016"
    season_6 = "SEASON2016"
    preseason_7 = "PRESEASON2017"
    season_7 = "SEASON2017"
    preseason_8 = "PRESEASON2018"
    season_8 = "SEASON2018"
    preseason_9 = "PRESEASON2019"
    season_9 = "SEASON2019"

    @property
    def id(self):
        return SEASON_IDS[self]

    def from_id(id: int):
        return {i: season for season, i in SEASON_IDS.items()}[id]

    def start(self, region: Region) -> arrow.Arrow:
        from .core import Patch
        if Patch._Patch__patches is None:
            Patch.__load__()
        for patch in Patch._Patch__patches[region]:
            if patch.season == self:
                return patch.start

    def end(self, region: Region) -> arrow.Arrow:
        from .core import Patch
        for patch in reversed(Patch._Patch__patches[region]):
            if patch.season == self:
                return patch.end


SEASON_IDS = {
    Season.preseason_3: 0,
    Season.season_3: 1,
    Season.preseason_4: 2,
    Season.season_4: 3,
    Season.preseason_5: 4,
    Season.season_5: 5,
    Season.preseason_6: 6,
    Season.season_6: 7,
    Season.preseason_7: 8,
    Season.season_7: 9,
    Season.preseason_8: 10,
    Season.season_8: 11,
    Season.preseason_9: 12,
    Season.season_9: 13
}


class GameType(Enum):
    custom = "CUSTOM_GAME"
    tutorial = "TUTORIAL_GAME"
    matched = "MATCHED_GAME"


class Lane(Enum):
    top_lane = "TOP_LANE"
    mid_lane = "MID_LANE"
    bot_lane = "BOT_LANE"
    jungle = "JUNGLE"
    utility = "UTILITY"

    def from_match_naming_scheme(string: str):
        return {
            "BOTTOM": Lane.bot_lane,
            "MIDDLE": Lane.mid_lane,
            "MID": Lane.mid_lane,
            "TOP": Lane.top_lane,
            "JUNGLE": Lane.jungle,
            "UTILITY": Lane.utility,
            "NONE": None
        }[string]


class Role(Enum):
    duo = "DUO"
    duo_carry = "DUO_CARRY"
    duo_support = "DUO_SUPPORT"
    none = "NONE"
    solo = "SOLO"

    def from_match_naming_scheme(string: str):
        return {
            "DUO": Role.duo,
            "DUO_CARRY": Role.duo_carry,
            "DUO_SUPPORT": Role.duo_support,
            "NONE": Role.none,
            "SOLO": Role.solo
        }[string]


class Position(Enum):
    top = "TOP"
    middle = "MIDDLE"
    jungle = "JUNGLE"
    bottom = "BOTTOM"
    utility = "UTILITY"
    apex = "APEX"
    none = "NONE"

    def from_league_naming_scheme(string: str):
        return {
            "TOP": Position.top,
            "MIDDLE": Position.middle,
            "JUNGLE": Position.jungle,
            "BOTTOM": Position.bottom,
            "UTILITY": Position.support,
            "NONE": Position.none
        }


class SummonersRiftArea(Enum):
    none = "NONE"
    nexus_blue = "NEXUS_BLUE"
    nexus_red = "NEXUS_RED"
    top_lane_blue = "TOP_LANE_BLUE"
    top_lane_purple = "TOP_LANE_PURPLE"
    top_lane_red = "TOP_LANE_RED"
    mid_lane_blue = "MID_LANE_BLUE"
    mid_lane_purple = "MID_LANE_PURPLE"
    mid_lane_red = "MID_LANE_RED"
    bot_lane_blue = "BOT_LANE_BLUE"
    bot_lane_purple = "BOT_LANE_PURPLE"
    bot_lane_red = "BOT_LANE_RED"
    jungle_top_blue = "JUNGLE_TOP_BLUE"
    jungle_top_red = "JUNGLE_TOP_RED"
    jungle_bot_blue = "JUNGLE_BOT_BLUE"
    jungle_bot_red = "JUNGLE_BOT_RED"
    river_top = "RIVER_TOP"
    river_bot = "RIVER_BOT"

    def get_side(self) -> Side:
        if "BLUE" in self.value:
            return Side.blue
        elif "RED" in self.value:
            return Side.red
        else:
            return None

    def get_lane(self) -> Lane:
        if "TOP" in self.value:
            return Lane.top_lane
        elif "MID" in self.value:
            return Lane.mid_lane
        elif "BOT" in self.value:
            return Lane.bot_lane
        elif "JUNGLE" in self.value:
            return Lane.jungle
        else:
            return None

    @staticmethod
    def from_position(position: "Position") -> "SummonersRiftArea":
        from .core.match import Position
        x, y = position.x, position.y

        # Load the map if it isn't already loaded
        try:
            map = SummonersRiftArea.__map
        except AttributeError:
            import os
            from PIL import Image
            script_dir = os.path.dirname(__file__)
            rel_path = './resources/summonersRiftAreas.png'
            map = Image.open(os.path.join(script_dir, rel_path))
            SummonersRiftArea.__map_size = map.size
            map = map.load()
            SummonersRiftArea.__map = map
        image_width, image_height = SummonersRiftArea.__map_size

        min_x = -120
        min_y = -120
        max_x = 14870
        max_y = 14980
        width = max_x - min_x
        height = max_y - min_y
        x = round((x - min_x) / width * (image_width - 1))
        y = round(abs(y - min_y - height) / height * (image_height - 1))
        rgb = map[x, y][0]

        color_mapping = {
            0: SummonersRiftArea.none,
            10: SummonersRiftArea.nexus_blue,
            20: SummonersRiftArea.nexus_red,
            30: SummonersRiftArea.top_lane_blue,
            40: SummonersRiftArea.top_lane_purple,
            50: SummonersRiftArea.top_lane_red,
            60: SummonersRiftArea.mid_lane_blue,
            70: SummonersRiftArea.mid_lane_purple,
            80: SummonersRiftArea.mid_lane_red,
            90: SummonersRiftArea.bot_lane_blue,
            100: SummonersRiftArea.bot_lane_purple,
            110: SummonersRiftArea.bot_lane_red,
            120: SummonersRiftArea.jungle_top_blue,
            130: SummonersRiftArea.jungle_top_red,
            140: SummonersRiftArea.jungle_bot_blue,
            150: SummonersRiftArea.jungle_bot_red,
            160: SummonersRiftArea.river_top,
            170: SummonersRiftArea.river_bot
        }
        return color_mapping.get(rgb, SummonersRiftArea.none)


class Tower(Enum):
    OUTER = "OUTER_TURRET"
    INNER = "INNER_TURRET"
    BASE  = "BASE_TURRET"
    NEXUS = "NEXUS_TURRET"
    UNDEFINED = "UNDEFINED_TURRET"


# References for Queues:
# https://developer.riotgames.com/game-constants.html
# https://discussion.developer.riotgames.com/articles/3482/multiple-queueids-are-being-updated-with-patch-719.html
# https://github.com/stelar7/L4J8/blob/master/src/main/java/no/stelar7/api/l4j8/basic/constants/types/GameQueueType.java
class Queue(Enum):
    custom = "CUSTOM"  # 0
    deprecated_blind_fives = "NORMAL_5x5_BLIND"  # 2
    deprecated_ranked_solo_fives = "CLASSIC"  # 4
    deprecated_ranked_premade_fives = "RANKED_PREMADE_5x5"  # 6
    deprecated_coop_ai_fives = "BOT_5x5"  # 7
    deprecated_blind_threes = "NORMAL_3x3"  # 8
    deprecated_ranked_premade_threes = "RANKED_PREMADE_3x3"  # 9
    deprecated_ranked_flex_threes = "RANKED_FLEX_TT_DEPRECATED"  # 9  # There are two different queue names with ID 9... This one was replaced with queue 470. There is therefore no corresponding queue with ID 9 for this Queue, and instead the Queue with ID 470 will be used when this name is requested, even for very old games. In addition, there are two queues with the name "RANKED_FLEX_TT"; in order to avoid a name conflict, we renamed this one.
    deprecated_draft_fives = "NORMAL_5x5_DRAFT"  # 14
    deprecated_blind_dominion = "ODIN_5x5_BLIND"  # 16
    deprecated_draft_dominion = "ODIN_5x5_DRAFT"  # 17
    deprecated_coop_ai_dominion = "BOT_ODIN_5x5"  # 25
    deprecated_coop_ai_intro_fives = "BOT_5x5_INTRO_DEPRECATED"  # 31  # There are two queues with the name "BOT_5x5_INTRO" so this one has been renamed in order to avoid a conflict.
    deprecated_coop_ai_beginner_fives = "BOT_5x5_BEGINNER_DEPRECATED"  # 32  # There are two queues with the name "BOT_5x5_BEGINNER" so this one has been renamed in order to avoid a conflict.
    deprecated_coop_ai_intermediate_fives = "BOT_5x5_INTERMEDIATE_DEPRECATED"  # 33  # There are two queues with the name "BOT_5x5_INTERMEDIATE" so this one has been renamed in order to avoid a conflict.
    deprecated_ranked_team_threes = "RANKED_TEAM_3x3"  # 41
    deprecated_ranked_team_fives = "RANKED_TEAM_5x5"  # 42
    deprecated_coop_ai_threes = "BOT_TT_3x3"  # 52
    deprecated_team_builder_fives = "GROUP_FINDER_5x5"  # 61
    deprecated_aram = "ARAM_5x5"  # 65
    one_for_all = "ONEFORALL_5x5"  # 70
    showdown_1v1 = "FIRSTBLOOD_1x1"  # 72
    showdown_2v2 = "FIRSTBLOOD_2x2"  # 73
    hexakill_summoners_rift = "SR_6x6"  # 75
    urf = "URF_5x5"  # 76
    mirror_mode_fives = "ONEFORALL_MIRRORMODE_5x5"  # 78
    urf_coop_ai = "BOT_URF_5x5"  # 83
    deprecated_doom_bots_rank_1 = "NIGHTMARE_BOT_5x5_RANK1"  # 91
    deprecated_doom_bots_rank_2 = "NIGHTMARE_BOT_5x5_RANK2"  # 92
    deprecated_doom_bots_rank_5 = "NIGHTMARE_BOT_5x5_RANK5"  # 93
    ascension = "ASCENSION_5x5"  # 96
    hexakill_twisted_treeline = "HEXAKILL"  # 98
    aram_butchers_bridge = "BILGEWATER_ARAM_5x5"  # 100
    deprecated_poro_king = "KING_PORO_5x5"  # 300
    nemesis_draft = "COUNTER_PICK"  # 310
    black_market_brawlers = "BILGEWATER_5x5"  # 313
    deprecated_nexus_siege = "SIEGE"  # 315
    definitely_not_dominion = "DEFINITELY_NOT_DOMINION_5x5"  # 317
    deprecated_all_random_urf = "ARURF_5X5"  # 318
    all_random_summoners_rift = "ARSR_5x5"  # 325
    normal_draft_fives = "TEAM_BUILDER_DRAFT_UNRANKED_5x5"  # 400
    deprecated_ranked_fives = "TEAM_BUILDER_DRAFT_RANKED_5x5"  # 410

    # TODO Evidently we originally had 420 as the commented out queue name below, but it may have changed?
    # TODO But the queue name sent to the Leagues endpoint needs to be RANKED_SOLO_5x5 for ranked solo games.
    ranked_solo_fives = "RANKED_SOLO_5x5"  # 420

    blind_fives = "NORMAL_5V5_BLIND_PICK"  # 430
    ranked_flex_fives = "RANKED_FLEX_SR"  # 440
    aram = "ARAM"  # 450
    blind_threes = "NORMAL_3X3_BLIND_PICK"  # 460
    blood_hunt_assassin = "ASSASSINATE_5x5"  # 600
    dark_star = "DARKSTAR_3x3"  # 610
    ranked_flex_threes = "RANKED_FLEX_TT"  # 470
    clash = "CLASH"  # 700
    coop_ai_intermediate_threes = "BOT_3X3_INTERMEDIATE"  # 800
    coop_ai_intro_threes = "BOT_3X3_INTRO"  # 810
    coop_ai_beginner_threes = "BOT_3X3_BEGINNER"  # 820
    coop_ai_intro_fives = "BOT_5X5_INTRO"  # 830
    coop_ai_beginner_fives = "BOT_5X5_BEGINNER"  # 840
    coop_ai_intermediate_fives = "BOT_5X5_INTERMEDIATE"  # 850
    all_random_urf = "ARURF_5X5"  # 900
    project = "PROJECT"  # 910
    poro_king = "KINGPORO"  # 920
    nexus_siege = "NEXUS_SIEGE"  # 940
    doom_bots_difficult = "NIGHTMARE_BOT_5X5_VOTE"  # 950
    doom_bots = "NIGHTMARE_BOT_5X5"  # 960
    guardian_invasion_normal = "INVASION_NORMAL"  # 980
    guardian_invasion_onslaught = "INVASION_ONSLAUGHT"  # 990
    overcharge = "OVERCHARGE"  # 1000
    all_random_urf_snow = "SNOWURF"  # 1010
    one_for_all_rapid = "ONEFORALL_RAPID_5x5" # 1020
    odyssey_intro = "ODYSSEY_INTRO"  # 1030
    odyssey_cadet = "ODYSSEY_CADET"  # 1040
    odyssey_crewmember = "ODYSSEY_CREWMEMBER"  # 1050
    odyssey_captain = "ODYSSEY_CAPTAIN"  # 1060
    odyssey_onslaught = "ODYSSEY_ONSLAUGHT"  # 1070
    ranked_tft = "RANKED_TFT" # 1100
    normal_tft = "NORMAL_TFT" # 1090
    deprecated_nexus_blitz = "NEXUS_BLITZ"  # 1200
    nexus_blitz = "NEXUS_BLITZ"  # 1300
    ultimate_spellbook = "ULTIMATE_SPELLBOOK"  # 1400
    tutorial1 = "TUTORIAL_1"  # Summoner's Rift  Tutorial 1
    tutorial2 = "TUTORIAL_2"  # Summoner's Rift  Tutorial 2
    tutorial3 = "TUTORIAL_3"  # Summoner's Rift  Tutorial 3

    def from_id(id: int):
        return {i: season for season, i in QUEUE_IDS.items()}[id]

    @property
    def id(self):
        return QUEUE_IDS[self]


QUEUE_IDS = {
    Queue.custom: 0,  # Custom games
    Queue.deprecated_blind_fives: 2,  # Summoner's Rift    5v5 Blind Pick games    Deprecated in patch 7.19 in favor of queueId 430
    Queue.deprecated_ranked_solo_fives: 4,  # Summoner's Rift    5v5 Ranked Solo games    Deprecated in favor of queueId 420
    Queue.deprecated_ranked_premade_fives: 6,  # Summoner's Rift    5v5 Ranked Premade games    Game mode deprecated
    Queue.deprecated_coop_ai_fives: 7,  # Summoner's Rift    Co-op vs AI games    Deprecated in favor of queueId 32 and 33
    Queue.deprecated_blind_threes: 8,  # Twisted Treeline    3v3 Normal games    Deprecated in patch 7.19 in favor of queueId 460
    Queue.deprecated_ranked_premade_threes: 9,  # Twisted Treeline    3v3 Ranked Flex games    Deprecated in patch 7.19 in favor of queueId 470
    Queue.deprecated_draft_fives: 14,  # Summoner's Rift    5v5 Draft Pick games    Deprecated in favor of queueId 400
    Queue.deprecated_blind_dominion: 16,  # Crystal Scar    5v5 Dominion Blind Pick games    Game mode deprecated
    Queue.deprecated_draft_dominion: 17,  # Crystal Scar    5v5 Dominion Draft Pick games    Game mode deprecated
    Queue.deprecated_coop_ai_dominion: 25,  # Crystal Scar    Dominion Co-op vs AI games    Game mode deprecated
    Queue.deprecated_coop_ai_intro_fives: 31,  # Summoner's Rift    Co-op vs AI Intro Bot games    Deprecated in patch 7.19 in favor of queueId 830
    Queue.deprecated_coop_ai_beginner_fives: 32,  # Summoner's Rift    Co-op vs AI Beginner Bot games    Deprecated in patch 7.19 in favor of queueId 840
    Queue.deprecated_coop_ai_intermediate_fives: 33,  # Summoner's Rift    Co-op vs AI Intermediate Bot games    Deprecated in patch 7.19 in favor of queueId 850
    Queue.deprecated_ranked_team_threes: 41,  # Twisted Treeline    3v3 Ranked Team games    Game mode deprecated
    Queue.deprecated_ranked_team_fives: 42,  # Summoner's Rift    5v5 Ranked Team games    Game mode deprecated
    Queue.deprecated_coop_ai_threes: 52,  # Twisted Treeline    Co-op vs AI games    Deprecated in patch 7.19 in favor of queueId 800
    Queue.deprecated_team_builder_fives: 61,  # Summoner's Rift    5v5 Team Builder games    Game mode deprecated
    Queue.deprecated_aram: 65,  # Howling Abyss    5v5 ARAM games    Deprecated in patch 7.19 in favor of queueId 450
    Queue.one_for_all: 70,  # Summoner's Rift    One for All games
    Queue.showdown_1v1: 72,  # Howling Abyss    1v1 Snowdown Showdown games
    Queue.showdown_2v2: 73,  # Howling Abyss    2v2 Snowdown Showdown games
    Queue.hexakill_summoners_rift: 75,  # Summoner's Rift    6v6 Hexakill games
    Queue.urf: 76,  # Summoner's Rift    Ultra Rapid Fire games
    Queue.mirror_mode_fives: 78,  # Summoner's Rift    Mirrored One for All
    Queue.urf_coop_ai: 83,  # Summoner's Rift    Co-op vs AI Ultra Rapid Fire games
    Queue.deprecated_doom_bots_rank_1: 91,  # Summoner's Rift    Doom Bots Rank 1 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.deprecated_doom_bots_rank_2: 92,  # Summoner's Rift    Doom Bots Rank 2 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.deprecated_doom_bots_rank_5: 93,  # Summoner's Rift    Doom Bots Rank 5 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.ascension: 96,  # Crystal Scar    Ascension games
    Queue.hexakill_twisted_treeline: 98,  # Twisted Treeline    6v6 Hexakill games
    Queue.aram_butchers_bridge: 100,  # Butcher's Bridge    5v5 ARAM games
    Queue.deprecated_poro_king: 300,  # Howling Abyss    King Poro games    Deprecated in patch 7.19 in favor of queueId 920
    Queue.nemesis_draft: 310,  # Summoner's Rift    Nemesis games
    Queue.black_market_brawlers: 313,  # Summoner's Rift    Black Market Brawlers games
    Queue.deprecated_nexus_siege: 315,  # Summoner's Rift    Nexus Siege games    Deprecated in patch 7.19 in favor of queueId 940
    Queue.definitely_not_dominion: 317,  # Crystal Scar    Definitely Not Dominion games
    Queue.deprecated_all_random_urf: 318,  # Summoner's Rift    All Random URF games      Game mode deprecated in patch 8.10 in favor is queueId 900
    Queue.all_random_summoners_rift: 325,  # Summoner's Rift    All Random games
    Queue.normal_draft_fives: 400,  # Summoner's Rift    5v5 Draft Pick games
    Queue.deprecated_ranked_fives: 410,  # Summoner's Rift    5v5 Ranked Dynamic games    Game mode deprecated in patch 6.22
    Queue.ranked_solo_fives: 420,  # Summoner's Rift    5v5 Ranked Solo games
    Queue.blind_fives: 430,  # Summoner's Rift    5v5 Blind Pick games
    Queue.ranked_flex_fives: 440,  # Summoner's Rift    5v5 Ranked Flex games
    Queue.aram: 450,  # Howling Abyss    5v5 ARAM games
    Queue.blind_threes: 460,  # Twisted Treeline    3v3 Blind Pick games
    Queue.ranked_flex_threes: 470,  # Twisted Treeline    3v3 Ranked Flex games
    Queue.blood_hunt_assassin: 600,  # Summoner's Rift    Blood Hunt Assassin games
    Queue.dark_star: 610,  # Cosmic Ruins    Dark Star games
    Queue.clash: 700,  # Summoner's Rift    Clash games
    Queue.coop_ai_intermediate_threes: 800,  # Twisted Treeline    Co-op vs. AI Intermediate Bot games
    Queue.coop_ai_intro_threes: 810,  # Twisted Treeline    Co-op vs. AI Intro Bot games
    Queue.coop_ai_beginner_threes: 820,  # Twisted Treeline    Co-op vs. AI Beginner Bot games
    Queue.coop_ai_intro_fives: 830,  # Summoner's Rift    Co-op vs. AI Intro Bot games
    Queue.coop_ai_beginner_fives: 840,  # Summoner's Rift    Co-op vs. AI Beginner Bot games
    Queue.coop_ai_intermediate_fives: 850,  # Summoner's Rift    Co-op vs. AI Intermediate Bot games
    Queue.all_random_urf: 900,  # Summoner's Rift    All Random URF games
    Queue.project: 910,
    Queue.poro_king: 920,  # Howling Abyss    Legend of the Poro King
    Queue.nexus_siege: 940,  # Summoner's Rift    Nexus Siege games
    Queue.doom_bots_difficult: 950,  # Summoner's Rift    Doom Bots games /w difficulty voting
    Queue.doom_bots: 960,  # Summoner's Rift    Doom Bots games
    Queue.guardian_invasion_normal: 980,  # Valoran City Park    Star Guardian Invasion: Normal games
    Queue.guardian_invasion_onslaught: 990,  # Valoran City Park    Star Guardian Invasion: Onslaught games
    Queue.overcharge: 1000,  # Overcharge, PROJECT: Hunters games
    Queue.all_random_urf_snow: 1010,  # Summoner's Rift, Snow ARURF games
    Queue.one_for_all_rapid: 1020, # Summoner's Rift  One for All games (increased gold and exp gain)
    Queue.odyssey_intro: 1030,  # Odyssey: Extraction
    Queue.odyssey_cadet: 1040,  # Odyssey: Extraction
    Queue.odyssey_crewmember: 1050,  # Odyssey: Extraction
    Queue.odyssey_captain: 1060,  # Odyssey: Extraction
    Queue.odyssey_onslaught: 1070,  # Odyssey: Extraction
    Queue.ranked_tft: 1100, #  Convergence, Ranked Teamfight Tactics games
    Queue.normal_tft: 1090, #  Convergence, Normal Teamfight Tactics games
    Queue.deprecated_nexus_blitz: 1200,  # Nexus Blitz map    Nexus Blitz Deprecated in patch 9.2 in favor of queueId 1300
    Queue.nexus_blitz: 1300,  # Nexus Blitz map    Nexus Blitz
    Queue.ultimate_spellbook: 1400,  # Summoner's Rift   Ultimate Spellbook
    Queue.tutorial1: 2000,  # Summoner's Rift  Tutorial 1
    Queue.tutorial2: 2010,  # Summoner's Rift  Tutorial 2
    Queue.tutorial3: 2020,  # Summoner's Rift  Tutorial 3
}

RANKED_QUEUES = {
    Queue.deprecated_ranked_solo_fives,  # Summoner's Rift    5v5 Ranked Solo games    Deprecated in favor of queueId 420
    Queue.deprecated_ranked_premade_fives,  # Summoner's Rift    5v5 Ranked Premade games    Game mode deprecated
    Queue.deprecated_ranked_premade_threes,  # Twisted Treeline    3v3 Ranked Flex games    Deprecated in patch 7.19 in favor of queueId 470
    Queue.deprecated_ranked_team_threes,  # Twisted Treeline    3v3 Ranked Team games    Game mode deprecated
    Queue.deprecated_ranked_team_fives,  # Summoner's Rift    5v5 Ranked Team games    Game mode deprecated
    Queue.deprecated_ranked_fives,  # Summoner's Rift    5v5 Ranked Dynamic games    Game mode deprecated in patch 6.22
    Queue.ranked_solo_fives,  # Summoner's Rift    5v5 Ranked Solo games
    Queue.ranked_flex_fives,  # Summoner's Rift    5v5 Ranked Flex games
    Queue.ranked_flex_threes,  # Twisted Treeline    3v3 Ranked Flex games
    Queue.ranked_tft, # Convergence  Ranked Teamfight Tactics games
}
