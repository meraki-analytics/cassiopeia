from enum import Enum
from collections import OrderedDict

from .patches import patches as _patches

PATCHES = OrderedDict(((patch.start, patch) for patch in _patches), key=lambda patch: patch.start)


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
    pbe = "PBE"

    @property
    def platform(self) -> "Platform":
        return getattr(Platform, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]


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
    pbe = "PBE1"

    @property
    def region(self) -> "Region":
        return getattr(Region, self.name)

    @property
    def default_locale(self) -> str:
        return DEFAULT_LOCALE[self]


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
    Region.pbe: "en_US",
    Platform.pbe: "en_US"
}


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


class Map(Enum):
    summoners_rift_summer = 1
    summoners_rift_autumn = 2
    the_proving_grounds = 3
    twisted_treeline_original = 4
    the_crystal_scar = 8
    twisted_treeline = 10
    summoners_rift = 11
    howling_abyss = 12
    butchers_bridge = 14
    cosmic_ruins = 16


class GameMode(Enum):
    aram = "ARAM"
    ascension = "ASCENSION"
    classic = "CLASSIC"
    showdown = "FIRSTBLOOD"
    poro_king = "KINGPORO"
    dominion = "ODIN"
    one_for_all = "ONEFORALL"
    tutorial = "TUTORIAL"
    nexus_siege = "SIEGE"
    assassinate = "ASSASSINATE"
    dark_star = "DARKSTAR"
    arsr = "ARSR"
    urf = "URF"
    doom_bots = "DOOMBOTSTEEMO"


class MasteryTree(Enum):
    cunning = "Cunning"
    ferocity = "Ferocity"
    resolve = "Resolve"


class RuneType(Enum):
    mark = "red"
    seal = "yellow"
    glyph = "blue"
    quint = "black"


class Tier(Enum):
    challenger = "CHALLENGER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    unranked = "UNRANKED"


class Division(Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"
    five = "V"


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

    def from_id(id: int):
        return {i: season for season, i in SEASON_IDS.items()}[id]


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
    Season.season_7: 9
}


class GameType(Enum):
    custom = "CUSTOM_GAME"
    tutorial = "TUTORIAL_GAME"
    matched = "MATCHED_GAME"


class Lane(Enum):
    top_lane = "TOP_LANE"
    mid_lane = "MID_LANE"
    bot_lane = "BOT_LANE"


class Queue(Enum):
    custom = "CUSTOM"
    normal_blind_threes = "NORMAL_3x3"
    normal_blind_fives = "NORMAL_5x5_BLIND"
    normal_draft_fives = "NORMAL_5x5_DRAFT"
    ranked_solo = "RANKED_SOLO_5x5"
    ranked_premade_fives = "RANKED_PREMADE_5x5"
    ranked_premade_threes = "RANKED_PREMADE_3x3"
    flex_threes = "RANKED_FLEX_TT"
    ranked_threes = "RANKED_TEAM_3x3"
    ranked_fives = "RANKED_TEAM_5x5"
    dominion_blind = "ODIN_5x5_BLIND"
    dominion_draft = "ODIN_5x5_DRAFT"
    bot_fives = "BOT_5x5"
    bot_dominion = "BOT_ODIN_5x5"
    bot_intro_fives = "BOT_5x5_INTRO"
    bot_beginner_fives = "BOT_5x5_BEGINNER"
    bot_intermediate_fives = "BOT_5x5_INTERMEDIATE"
    bot_threes = "BOT_TT_3x3"
    team_builder = "GROUP_FINDER_5x5"
    aram = "ARAM_5x5"
    one_for_all = "ONEFORALL_5x5"
    showdown_solo = "FIRSTBLOOD_1x1"
    showdown_duo = "FIRSTBLOOD_2x2"
    hexakill_summoners_rift = "SR_6x6"
    urf = "URF_5x5"
    one_for_all_mirror = "ONEFORALL_MIRRORMODE_5x5"
    bot_urf = "BOT_URF_5x5"
    doom_bots_1 = "NIGHTMARE_BOT_5x5_RANK1"
    doom_bots_2 = "NIGHTMARE_BOT_5x5_RANK2"
    doom_bots_5 = "NIGHTMARE_BOT_5x5_RANK5"
    ascension = "ASCENSION_5x5"
    hexakill_twisted_treeline = "HEXAKILL"
    butchers_bridge = "BILGEWATER_ARAM_5x5"
    poro_king = "KING_PORO_5x5"
    nemesis_draft = "COUNTER_PICK"
    black_market = "BILGEWATER_5x5"
    nexus_siege = "SIEGE"
    definitely_not_dominion = "DEFINITELY_NOT_DOMINION_5x5"
    all_random_urf = "ARURF_5X5"
    all_random_summoners_rift = "ARSR_5x5"
    dynamic_queue = "TEAM_BUILDER_DRAFT_UNRANKED_5x5"
    ranked_dynamic_queue = "TEAM_BUILDER_DRAFT_RANKED_5x5"
    ranked_solo_queue = "TEAM_BUILDER_RANKED_SOLO"
    flex = "RANKED_FLEX_SR"
    blood_hunt = "ASSASSINATE_5x5"
    darkstar = "DARKSTAR_3x3"

    def from_id(id: int):
        return {i: season for season, i in QUEUE_IDS.items()}[id]


QUEUE_IDS = {
    Queue.custom: 0,
    Queue.normal_blind_threes: 8,
    Queue.normal_blind_fives: 2,
    Queue.normal_draft_fives: 14,
    Queue.ranked_solo: 4,
    Queue.ranked_premade_fives: 6,
    Queue.ranked_premade_threes: 9,
    Queue.flex_threes: 9,
    Queue.ranked_threes: 41,
    Queue.ranked_fives: 42,
    Queue.dominion_blind: 16,
    Queue.dominion_draft: 17,
    Queue.bot_fives: 7,
    Queue.bot_dominion: 25,
    Queue.bot_intro_fives: 31,
    Queue.bot_beginner_fives: 32,
    Queue.bot_intermediate_fives: 33,
    Queue.bot_threes: 52,
    Queue.team_builder: 61,
    Queue.aram: 65,
    Queue.one_for_all: 70,
    Queue.showdown_solo: 72,
    Queue.showdown_duo: 73,
    Queue.hexakill_summoners_rift: 75,
    Queue.urf: 76,
    Queue.one_for_all_mirror: 78,
    Queue.bot_urf: 83,
    Queue.doom_bots_1: 91,
    Queue.doom_bots_2: 92,
    Queue.doom_bots_5: 93,
    Queue.ascension: 96,
    Queue.hexakill_twisted_treeline: 98,
    Queue.butchers_bridge: 100,
    Queue.poro_king: 300,
    Queue.nemesis_draft: 310,
    Queue.black_market: 313,
    Queue.nexus_siege: 315,
    Queue.definitely_not_dominion: 317,
    Queue.all_random_urf: 318,
    Queue.all_random_summoners_rift: 325,
    Queue.dynamic_queue: 400,
    Queue.ranked_dynamic_queue: 410,
    Queue.ranked_solo_queue: 420,
    Queue.flex: 440,
    Queue.blood_hunt: 600,
    Queue.darkstar: 610
}

RANKED_QUEUES = {
    Queue.flex,
    Queue.flex_threes,
    Queue.ranked_solo
}
