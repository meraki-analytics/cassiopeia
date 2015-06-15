import enum
import json

class CassiopeiaObject(object):
    # @param data # CassiopeiaDto # The underlying DTO object with the data for this type
    def __init__(self, data):
        self.data = data

    def to_json(self):
        return json.dumps(self.data, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __hash__(self):
        return hash(id(self))


class lazyproperty(object):
    # @param method # function # The method to make a lazy property out of
    def __init__(self, method):
        self.method = method
        self.values = {}

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")

    def __get__(self, obj, type=None):
        try:
            return self.values[obj]
        except(KeyError):
            self.values[obj] = self.method(obj)
            return self.values[obj]


class immutablemethod(object):
    # @param method # function # The method to make immutable
    def __init__(self, method):
        self.method = method

    def __set__(self, obj, value):
        raise AttributeError("can't set method")

    def __delete__(self, obj):
        raise AttributeError("can't delete method")

    def __get__(self, obj, type=None):
        def curried(*args):
            return self.method(obj, *args)
        return curried


class LoadPolicy(enum.Enum):
    lazy = "LAZY"
    eager = "EAGER"


class Lane(enum.Enum):
    top_lane = "TOP"
    jungle = "JUNGLE"
    mid_lane = "MIDDLE"
    bot_lane = "BOTTOM"


class Role(enum.Enum):
    none = "NONE"
    solo = "SOLO"
    duo = "DUO"
    carry = "DUO_CARRY"
    support = "DUO_SUPPORT"


class Side(enum.Enum):
    blue = 100
    red = 200


class Queue(enum.Enum):
    custom = "CUSTOM"
    normal_blind_fives = "NORMAL_5x5_BLIND"
    bot_fives = "BOT_5x5"
    bot_intro_fives = "BOT_5x5_INTRO"
    bot_beginner_fives = "BOT_5x5_BEGINNER"
    bot_intermediate_fives = "BOT_5x5_INTERMEDIATE"
    normal_blind_threes = "NORMAL_3x3"
    normal_draft_fives = "NORMAL_5x5_DRAFT"
    dominion_blind = "ODIN_5x5_BLIND"
    dominion_draft = "ODIN_5x5_DRAFT"
    bot_dominion = "BOT_ODIN_5x5"
    ranked_solo = "RANKED_SOLO_5x5"
    ranked_premade_threes = "RANKED_PREMADE_3x3"
    ranked_premade_fives = "RANKED_PREMADE_5x5"
    ranked_threes = "RANKED_TEAM_3x3"
    ranked_fives = "RANKED_TEAM_5x5"
    bot_threes = "BOT_TT_3x3"
    team_builder = "GROUP_FINDER_5x5"
    aram = "ARAM_5x5"
    one_for_all = "ONEFORALL_5x5"
    showdown_solo = "FIRSTBLOOD_1x1"
    showdown_duo = "FIRSTBLOOD_2x2"
    hexakill_summoners_rift = "SR_6x6"
    urf = "URF_5x5"
    bot_urf = "BOT_URF_5x5"
    doom_bots_1 = "NIGHTMARE_BOT_5x5_RANK1"
    doom_bots_2 = "NIGHTMARE_BOT_5x5_RANK2"
    doom_bots_5 = "NIGHTMARE_BOT_5x5_RANK5"
    hexakill_twisted_treeline = "HEXAKILL"
    poro_king = "KING_PORO_5x5"
    nemesis_draft = "COUNTER_PICK"

ranked_queues = {Queue.ranked_solo, Queue.ranked_threes, Queue.ranked_fives}


class Tier(enum.Enum):
    challenger = "CHALLENGER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"


class Division(enum.Enum):
    one = "I"
    two = "II"
    three = "III"
    four = "IV"
    five = "V"


class Season(enum.Enum):
    preseason_3 = "PRESEASON3"
    season_3 = "SEASON3"
    preseason_4 = "PRESEASON2014"
    season_4 = "SEASON2014"
    preseason_5 = "PRESEASON2015"
    season_5 = "SEASON2015"

stats_seasons = {Season.season_3, Season.season_4, Season.season_5}


class Region(enum.Enum):
    brazil = "BR"
    europe_north_east = "EUNE"
    europe_west = "EUW"
    korea = "KR"
    latin_america_north = "LAN"
    latin_america_south = "LAS"
    north_america = "NA"
    oceania = "OCE"
    russia = "RU"
    turkey = "TR"


class Platform(enum.Enum):
    brazil = "BR1"
    europe_north_east = "EUN1"
    europe_west = "EUW1"
    korea = "KR"
    latin_america_north = "LA1"
    latin_america_south = "LA2"
    north_america = "NA1"
    oceania = "OC1"
    russia = "RU"
    turkey = "TR1"


class Map(enum.Enum):
    summoners_rift_summer = 1
    summoners_rift_autumn = 2
    the_proving_grounds = 3
    twisted_treeline_original = 4
    the_crystal_scar = 8
    twisted_treeline = 10
    summoners_rift = 11
    howling_abyss = 12


class GameMode(enum.Enum):
    aram = "ARAM"
    ascension = "ASCENSION"
    classic = "CLASSIC"
    showdown = "FIRSTBLOOD"
    poro_king = "KINGPORO"
    dominion = "ODIN"
    one_for_all = "ONEFORALL"
    tutorial = "TUTORIAL"


class GameType(enum.Enum):
    custom = "CUSTOM_GAME"
    tutorial = "TUTORIAL_GAME"
    matched = "MATCHED_GAME"


class SubType(enum.Enum):
    custom = "NONE"
    normal_fives = "NORMAL"
    normal_threes = "NORMAL_3x3"
    dominion = "ODIN_UNRANKED"
    aram = "ARAM_UNRANKED_5x5"
    bot_fives = "BOT"
    bot_threes = "BOT_3x3"
    ranked_solo = "RANKED_SOLO_5x5"
    ranked_threes = "RANKED_TEAM_3x3"
    ranked_fives = "RANKED_TEAM_5x5"
    one_for_all = "ONEFORALL_5x5"
    showdown_solo = "FIRSTBLOOD_1x1"
    showdown_duo = "FIRSTBLOOD_2x2"
    hexakill_summoners_rift = "SR_6x6"
    team_builder = "CAP_5x5"
    urf = "URF"
    bot_urf = "URF_BOT"
    doom_bots = "NIGHTMARE_BOT"
    ascension = "ASCENSION"
    hexakill_twisted_treeline = "HEXAKILL"
    poro_king = "KING_PORO"
    nemesis_draft = "COUNTER_PICK"


class StatSummaryType(enum.Enum):
    normal_fives = "Unranked"
    normal_threes = "Unranked3x3"
    dominion = "OdinUnranked"
    aram = "AramUnranked5x5"
    bot_fives = "CoopVsAI"
    bot_threes = "CoopVsAI3x3"
    ranked_solo = "RankedSolo5x5"
    ranked_threes = "RankedTeam3x3"
    ranked_fives = "RankedTeam5x5"
    one_for_all = "OneForAll5x5"
    showdown_solo = "FirstBlood1x1"
    showdown_duo = "FirstBlood2x2"
    hexakill_summoners_rift = "SummonersRift6x6"
    team_builder = "CAP5x5"
    urf = "URF"
    bot_urf = "URFBots"
    doom_bots = "NightmareBot"
    ascension = "Ascension"
    hexakill_twisted_treeline = "Hexakill"
    poro_king = "KingPoro"
    nemesis_draft = "CounterPick"


class Ascended(enum.Enum):
    player = "CHAMPION_ASCENDED"
    death = "CLEAR_ASCENDED"
    npc = "MINION_ASCENDED"


class Building(enum.Enum):
    inhibitor = "INHIBITOR_BUILDING"
    turret = "TOWER_BUILDING"


class EventType(enum.Enum):
    ascension = "ASCENDED_EVENT"
    building_kill = "BUILDING_KILL"
    point_capture = "CAPTURE_POINT"
    kill = "CHAMPION_KILL"
    elite_monster_kill = "ELITE_MONSTER_KILL"
    item_destruction = "ITEM_DESTROYED"
    item_purchase = "ITEM_PURCHASED"
    item_sale = "ITEM_SOLD"
    item_undo = "ITEM_UNDO"
    summoning = "PORO_KING_SUMMON"
    skill_up = "SKILL_LEVEL_UP"
    ward_kill = "WARD_KILL"
    ward_placement = "WARD_PLACED"


class LaneType(enum.Enum):
    top_lane = "TOP_LANE"
    mid_lane = "MID_LANE"
    bot_lane = "BOT_LANE"


class LevelUp(enum.Enum):
    evolution = "EVOLVE"
    normal = "NORMAL"


class Monster(enum.Enum):
    baron = "BARON_NASHOR"
    dragon = "DRAGON"
    blue = "BLUE_GOLEM"
    red = "RED_LIZARD"
    spider = "VILEMAW"


class Point(enum.Enum):
    windmill = "POINT_C"
    drill = "POINT_D"
    boneyard = "POINT_E"
    quarry = "POINT_A"
    refinery = "POINT_B"


class Turret(enum.Enum):
    outer = "OUTER_TURRET"
    inner = "INNER_TURRET"
    inhibitor = "BASE_TURRET"
    nexus = "NEXUS_TURRET"
    fountain = "FOUNTAIN_TURRET"
    undefined = "UNDEFINED_TURRET"


class Ward(enum.Enum):
    sight = "SIGHT_WARD"
    vision = "VISION_WARD"
    trinket = "YELLOW_TRINKET"
    upgraded_trinket = "YELLOW_TRINKET_UPGRADE"
    mushroom = "TEEMO_MUSHROOM"
    undefined = "UNDEFINED"