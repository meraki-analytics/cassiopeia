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
    all_random_summoners_rift = "ARSR"
    urf = "URF"
    doom_bots = "DOOMBOTSTEEMO"
    star_guardian = "STARGUARDIAN"
    project = "PROJECT"
    overcharge = "OVERCHARGE"
    all_random_urf_snow = "SNOWURF"


class MasteryTree(Enum):
    cunning = "Cunning"
    ferocity = "Ferocity"
    resolve = "Resolve"


class RunePath(Enum):
    precision = "Precision"
    domination = "Domination"
    sorcery = "Sorcery"
    inspiration = "Inspiration"
    resolve = "Resolve"


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
    preseason_8 = "PRESEASON2018"
    season_8 = "SEASON2018"

    @property
    def id(self):
        return SEASON_IDS[self]

    def from_id(id: int):
        return {i: season for season, i in SEASON_IDS.items()}[id]

    def start(self, region: Region) -> arrow.Arrow:
        from .core import Patch
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
    Season.season_8: 11
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

    def from_match_naming_scheme(string: str):
        return {
            "BOTTOM": Lane.bot_lane,
            "MIDDLE": Lane.mid_lane,
            "TOP": Lane.top_lane,
            "JUNGLE": Lane.jungle
        }[string]


class Role(Enum):
    top = "TOP"
    jungle = "JUNGLE"
    middle = "MIDDLE"
    adc = "DUO_CARRY"
    support = "DUO_SUPPORT"

    def from_match_naming_scheme(string: str):
        return {
            "DUO_CARRY": Role.adc,
            "DUO_SUPPORT": Role.support
        }[string]


# References for Queues:
# https://developer.riotgames.com/game-constants.html
# https://discussion.developer.riotgames.com/articles/3482/multiple-queueids-are-being-updated-with-patch-719.html
# https://github.com/stelar7/L4J8/blob/master/src/main/java/no/stelar7/api/l4j8/basic/constants/types/GameQueueType.java
class Queue(Enum):
    custom = "CUSTOM"  # 0
    depreciated_blind_fives = "NORMAL_5x5_BLIND"  # 2
    depreciated_ranked_solo_fives = "CLASSIC"  # 4
    depreciated_ranked_premade_fives = "RANKED_PREMADE_5x5"  # 6
    depreciated_coop_ai_fives = "BOT_5x5"  # 7
    depreciated_blind_threes = "NORMAL_3x3"  # 8
    depreciated_ranked_premade_threes = "RANKED_PREMADE_3x3"  # 9
    depreciated_ranked_flex_threes = "RANKED_FLEX_TT"  # 9  # There are two different queue names with ID 9... This one was replaced with queue 470. There is therefore no corresponding queue with ID 9 for this Queue, and instead the Queue with ID 470 will be used when this name is requested, even for very old games.
    depreciated_draft_fives = "NORMAL_5x5_DRAFT"  # 14
    depreciated_blind_dominion = "ODIN_5x5_BLIND"  # 16
    depreciated_draft_dominion = "ODIN_5x5_DRAFT"  # 17
    depreciated_coop_ai_dominion = "BOT_ODIN_5x5"  # 25
    depreciated_coop_ai_intro_fives = "BOT_5x5_INTRO"  # 31
    depreciated_coop_ai_beginner_fives = "BOT_5x5_BEGINNER"  # 32
    depreciated_coop_ai_intermediate_fives = "BOT_5x5_INTERMEDIATE"  # 33
    depreciated_ranked_team_threes = "RANKED_TEAM_3x3"  # 41
    depreciated_ranked_team_fives = "RANKED_TEAM_5x5"  # 42
    depreciated_coop_ai_threes = "BOT_TT_3x3"  # 52
    depreciated_team_builder_fives = "GROUP_FINDER_5x5"  # 61
    depreciated_aram = "ARAM_5x5"  # 65
    one_for_all = "ONEFORALL_5x5"  # 70
    showdown_1v1 = "FIRSTBLOOD_1x1"  # 72
    showdown_2v2 = "FIRSTBLOOD_2x2"  # 73
    hexakill_summoners_rift = "SR_6x6"  # 75
    urf = "URF_5x5"  # 76
    mirror_mode_fives = "ONEFORALL_MIRRORMODE_5x5"  # 78
    urf_coop_ai = "BOT_URF_5x5"  # 83
    depreciated_doom_bots_rank_1 = "NIGHTMARE_BOT_5x5_RANK1"  # 91
    depreciated_doom_bots_rank_2 = "NIGHTMARE_BOT_5x5_RANK2"  # 92
    depreciated_doom_bots_rank_5 = "NIGHTMARE_BOT_5x5_RANK5"  # 93
    ascension = "ASCENSION_5x5"  # 96
    hexakill_twisted_treeline = "HEXAKILL"  # 98
    aram_butchers_bridge = "BILGEWATER_ARAM_5x5"  # 100
    depreciated_poro_king = "KING_PORO_5x5"  # 300
    nemesis_draft = "COUNTER_PICK"  # 310
    black_market_brawlers = "BILGEWATER_5x5"  # 313
    depreciated_nexus_siege = "SIEGE"  # 315
    definitely_not_dominion = "DEFINITELY_NOT_DOMINION_5x5"  # 317
    all_random_urf = "ARURF_5X5"  # 318
    all_random_summoners_rift = "ARSR_5x5"  # 325
    normal_draft_fives = "TEAM_BUILDER_DRAFT_UNRANKED_5x5"  # 400
    depreciated_ranked_fives = "TEAM_BUILDER_DRAFT_RANKED_5x5"  # 410

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
    coop_ai_intermediate_threes = "BOT_3X3_INTERMEDIATE"  # 800
    coop_ai_intro_threes = "BOT_3X3_INTRO"  # 810
    coop_ai_beginner_threes = "BOT_3X3_BEGINNER"  # 820
    coop_ai_intro_fives = "BOT_5X5_INTRO"  # 830
    coop_ai_beginner_fives = "BOT_5X5_BEGINNER"  # 840
    coop_ai_intermediate_fives = "BOT_5X5_INTERMEDIATE"  # 850
    project = "PROJECT"  # 910
    poro_king = "KINGPORO"  # 920
    nexus_siege = "NEXUS_SIEGE"  # 940
    doom_bots_difficult = "NIGHTMARE_BOT_5X5_VOTE"  # 950
    doom_bots = "NIGHTMARE_BOT_5X5"  # 960
    guardian_invasion_normal = "INVASION_NORMAL"  # 980
    guardian_invasion_onslaught = "INVASION_ONSLAUGHT"  # 990
    overcharge = "OVERCHARGE"  # 1000
    all_random_urf_snow = "SNOWURF"  # 1010

    def from_id(id: int):
        return {i: season for season, i in QUEUE_IDS.items()}[id]

    @property
    def id(self):
        return QUEUE_IDS[self]


QUEUE_IDS = {
    Queue.custom: 0,  # Custom games
    Queue.depreciated_blind_fives: 2,  # Summoner's Rift    5v5 Blind Pick games    Deprecated in patch 7.19 in favor of queueId 430
    Queue.depreciated_ranked_solo_fives: 4,  # Summoner's Rift    5v5 Ranked Solo games    Deprecated in favor of queueId 420
    Queue.depreciated_ranked_premade_fives: 6,  # Summoner's Rift    5v5 Ranked Premade games    Game mode deprecated
    Queue.depreciated_coop_ai_fives: 7,  # Summoner's Rift    Co-op vs AI games    Deprecated in favor of queueId 32 and 33
    Queue.depreciated_blind_threes: 8,  # Twisted Treeline    3v3 Normal games    Deprecated in patch 7.19 in favor of queueId 460
    Queue.depreciated_ranked_premade_threes: 9,  # Twisted Treeline    3v3 Ranked Flex games    Deprecated in patch 7.19 in favor of queueId 470
    Queue.depreciated_draft_fives: 14,  # Summoner's Rift    5v5 Draft Pick games    Deprecated in favor of queueId 400
    Queue.depreciated_blind_dominion: 16,  # Crystal Scar    5v5 Dominion Blind Pick games    Game mode deprecated
    Queue.depreciated_draft_dominion: 17,  # Crystal Scar    5v5 Dominion Draft Pick games    Game mode deprecated
    Queue.depreciated_coop_ai_dominion: 25,  # Crystal Scar    Dominion Co-op vs AI games    Game mode deprecated
    Queue.depreciated_coop_ai_intro_fives: 31,  # Summoner's Rift    Co-op vs AI Intro Bot games    Deprecated in patch 7.19 in favor of queueId 830
    Queue.depreciated_coop_ai_beginner_fives: 32,  # Summoner's Rift    Co-op vs AI Beginner Bot games    Deprecated in patch 7.19 in favor of queueId 840
    Queue.depreciated_coop_ai_intermediate_fives: 33,  # Summoner's Rift    Co-op vs AI Intermediate Bot games    Deprecated in patch 7.19 in favor of queueId 850
    Queue.depreciated_ranked_team_threes: 41,  # Twisted Treeline    3v3 Ranked Team games    Game mode deprecated
    Queue.depreciated_ranked_team_fives: 42,  # Summoner's Rift    5v5 Ranked Team games    Game mode deprecated
    Queue.depreciated_coop_ai_threes: 52,  # Twisted Treeline    Co-op vs AI games    Deprecated in patch 7.19 in favor of queueId 800
    Queue.depreciated_team_builder_fives: 61,  # Summoner's Rift    5v5 Team Builder games    Game mode deprecated
    Queue.depreciated_aram: 65,  # Howling Abyss    5v5 ARAM games    Deprecated in patch 7.19 in favor of queueId 450
    Queue.one_for_all: 70,  # Summoner's Rift    One for All games
    Queue.showdown_1v1: 72,  # Howling Abyss    1v1 Snowdown Showdown games
    Queue.showdown_2v2: 73,  # Howling Abyss    2v2 Snowdown Showdown games
    Queue.hexakill_summoners_rift: 75,  # Summoner's Rift    6v6 Hexakill games
    Queue.urf: 76,  # Summoner's Rift    Ultra Rapid Fire games
    Queue.mirror_mode_fives: 78,  # Summoner's Rift    Mirrored One for All
    Queue.urf_coop_ai: 83,  # Summoner's Rift    Co-op vs AI Ultra Rapid Fire games
    Queue.depreciated_doom_bots_rank_1: 91,  # Summoner's Rift    Doom Bots Rank 1 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.depreciated_doom_bots_rank_2: 92,  # Summoner's Rift    Doom Bots Rank 2 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.depreciated_doom_bots_rank_5: 93,  # Summoner's Rift    Doom Bots Rank 5 games    Deprecated in patch 7.21 in favor of queueId 950
    Queue.ascension: 96,  # Crystal Scar    Ascension games
    Queue.hexakill_twisted_treeline: 98,  # Twisted Treeline    6v6 Hexakill games
    Queue.aram_butchers_bridge: 100,  # Butcher's Bridge    5v5 ARAM games
    Queue.depreciated_poro_king: 300,  # Howling Abyss    King Poro games    Deprecated in patch 7.19 in favor of queueId 920
    Queue.nemesis_draft: 310,  # Summoner's Rift    Nemesis games
    Queue.black_market_brawlers: 313,  # Summoner's Rift    Black Market Brawlers games
    Queue.depreciated_nexus_siege: 315,  # Summoner's Rift    Nexus Siege games    Deprecated in patch 7.19 in favor of queueId 940
    Queue.definitely_not_dominion: 317,  # Crystal Scar    Definitely Not Dominion games
    Queue.all_random_urf: 318,  # Summoner's Rift    All Random URF games
    Queue.all_random_summoners_rift: 325,  # Summoner's Rift    All Random games
    Queue.normal_draft_fives: 400,  # Summoner's Rift    5v5 Draft Pick games
    Queue.depreciated_ranked_fives: 410,  # Summoner's Rift    5v5 Ranked Dynamic games    Game mode deprecated in patch 6.22
    Queue.ranked_solo_fives: 420,  # Summoner's Rift    5v5 Ranked Solo games
    Queue.blind_fives: 430,  # Summoner's Rift    5v5 Blind Pick games
    Queue.ranked_flex_fives: 440,  # Summoner's Rift    5v5 Ranked Flex games
    Queue.aram: 450,  # Howling Abyss    5v5 ARAM games
    Queue.blind_threes: 460,  # Twisted Treeline    3v3 Blind Pick games
    Queue.ranked_flex_threes: 470,  # Twisted Treeline    3v3 Ranked Flex games
    Queue.blood_hunt_assassin: 600,  # Summoner's Rift    Blood Hunt Assassin games
    Queue.dark_star: 610,  # Cosmic Ruins    Dark Star games
    Queue.coop_ai_intermediate_threes: 800,  # Twisted Treeline    Co-op vs. AI Intermediate Bot games
    Queue.coop_ai_intro_threes: 810,  # Twisted Treeline    Co-op vs. AI Intro Bot games
    Queue.coop_ai_beginner_threes: 820,  # Twisted Treeline    Co-op vs. AI Beginner Bot games
    Queue.coop_ai_intro_fives: 830,  # Summoner's Rift    Co-op vs. AI Intro Bot games
    Queue.coop_ai_beginner_fives: 840,  # Summoner's Rift    Co-op vs. AI Beginner Bot games
    Queue.coop_ai_intermediate_fives: 850,  # Summoner's Rift    Co-op vs. AI Intermediate Bot games
    Queue.project: 910,
    Queue.poro_king: 920,  # Howling Abyss    Legend of the Poro King
    Queue.nexus_siege: 940,  # Summoner's Rift    Nexus Siege games
    Queue.doom_bots_difficult: 950,  # Summoner's Rift    Doom Bots games /w difficulty voting
    Queue.doom_bots: 960,  # Summoner's Rift    Doom Bots games
    Queue.guardian_invasion_normal: 980,  # Valoran City Park    Star Guardian Invasion: Normal games
    Queue.guardian_invasion_onslaught: 990,  # Valoran City Park    Star Guardian Invasion: Onslaught games
    Queue.overcharge: 1000,  # Overcharge, PROJECT: Hunters games
    Queue.all_random_urf_snow: 1010,  # Summoner's Rift, Snow ARURF games
}

RANKED_QUEUES = {
    Queue.depreciated_ranked_solo_fives,  # Summoner's Rift    5v5 Ranked Solo games    Deprecated in favor of queueId 420
    Queue.depreciated_ranked_premade_fives,  # Summoner's Rift    5v5 Ranked Premade games    Game mode deprecated
    Queue.depreciated_ranked_premade_threes,  # Twisted Treeline    3v3 Ranked Flex games    Deprecated in patch 7.19 in favor of queueId 470
    Queue.depreciated_ranked_team_threes,  # Twisted Treeline    3v3 Ranked Team games    Game mode deprecated
    Queue.depreciated_ranked_team_fives,  # Summoner's Rift    5v5 Ranked Team games    Game mode deprecated
    Queue.depreciated_ranked_fives,  # Summoner's Rift    5v5 Ranked Dynamic games    Game mode deprecated in patch 6.22
    Queue.ranked_solo_fives,  # Summoner's Rift    5v5 Ranked Solo games
    Queue.ranked_flex_fives,  # Summoner's Rift    5v5 Ranked Flex games
    Queue.ranked_flex_threes,  # Twisted Treeline    3v3 Ranked Flex games
}
