import enum
import weakref
import functools

import cassiopeia.type.api.exception


class CassiopeiaObject(object):
    """
    An object storing data from the API, with various helpful utilities and shortcuts
    """

    def __init__(self, data):
        """
        An object storing data from the API, with various helpful utilities and shortcuts
        """
        if data.__class__ is not self.dto_type:
            raise cassiopeia.type.api.exception.CassiopeiaException("Tried to instantiate a core {class_} with a {dto} dto!".format(class_=self.__class__.__name__, dto=data.__class__.__name__))
        self.data = data

    def to_json(self, **kwargs):
        """
        Args:
            data (CassiopeiaDto): the underlying DTO object with the data for this type
        """
        return self.data.to_json(**kwargs)

    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __hash__(self):
        return hash(id(self))


class LazyProperty(object):
    def __init__(self, method):
        """
        Gets a JSON representation of the object

        Returns:
            str: a JSON representation of the object
        """
        self.method = method
        self.values = weakref.WeakKeyDictionary()

    def __set__(self, obj, value):
        raise AttributeError("can't set attribute")

    def __delete__(self, obj):
        raise AttributeError("can't delete attribute")

    def __get__(self, obj, t=None):
        try:
            return self.values[obj]
        except KeyError:
            self.values[obj] = self.method(obj)
            return self.values[obj]


def lazyproperty(method):
    """
    Args:
        method (function): the method to turn into a lazy property
    """
    prop = LazyProperty(method)

    @property
    @functools.wraps(method)
    def lazy(self):
        return prop.__get__(self)

    return lazy


class immutablemethod(object):
    """
    Makes a property load only once and store the result value to be returned to all later calls

    Args:
        method (function): the method to turn into a lazy property

    Returns:
        function: the method as a lazy property
    """
    def __init__(self, method):
        """
        Makes a method un-deletable and un-repleacable
        @decorator
        """
        self.method = method

    def __set__(self, obj, value):
        raise AttributeError("can't set method")

    def __delete__(self, obj):
        raise AttributeError("can't delete method")

    def __get__(self, obj, type=None):
        @functools.wraps(self.method)
        def curried(*args, **kwargs):
            return self.method(obj, *args, **kwargs)
        return curried


def inheritdocs(class_):
    """
    Args:
        method (function): the method to make immutable
    """
    for name, method in vars(class_).items():
        if not method.__doc__:
            for parent in class_.__bases__:
                try:
                    p_method = getattr(parent, name)
                    if p_method and p_method.__doc__:
                        method.__doc__ = p_method.__doc__
                except AttributeError:
                    continue
    return class_


class LookupableMixin(object):
    def __init__(self, fields, args):
        super().__init__(args)
        self.fields = fields

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except (TypeError, IndexError, KeyError, AttributeError):
            return self._lookup(key)


class LookupableList(LookupableMixin, list):
    def _lookup(self, key):
        for field, _type in self.fields:
            if isinstance(key, _type):
                for item in self:
                    # The next 7 lines allow lookup keys such as 'champion.name'
                    attr = item
                    _field = field
                    while '.' in _field:
                        _field, tail = _field.split('.', 1)
                        attr = getattr(attr, _field)
                        _field = tail
                    attr = getattr(attr, _field)
                    if key == attr:
                        return item
        else:
            raise KeyError(key)


class LookupableDict(LookupableMixin, dict):
    def _lookup(self, key):
        for field, _type in self.fields:
            if isinstance(key, _type):
                for item in self:
                    # The next 7 lines allow lookup keys such as 'champion.name'
                    attr = item
                    _field = field
                    while '.' in _field:
                        _field, tail = _field.split('.', 1)
                        attr = getattr(attr, _field)
                        _field = tail
                    attr = getattr(attr, _field)
                    if key == attr:
                        return self[item]
        else:
            raise KeyError(key)


def indexable(fields):
    """
        Args:
            fields (list<tuple<str, type>>): a list of tuples of the form (attribute_name, attribute_type) to perform the lookup on in the objects in the list or dict
    """
    @cassiopeia.type.core.common.inheritdocs
    def _wrapper(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, list):
                result = LookupableList(fields, result)
            if isinstance(result, dict):
                result = LookupableDict(fields, result)
            return result
        return wrapper
    return _wrapper


class LoadPolicy(enum.Enum):
    lazy = "LAZY"
    eager = "EAGER"


class MasteryType(enum.Enum):
    ferocity = "Ferocity"
    resolve = "Resolve"
    cunning = "Cunning"


class Lane(enum.Enum):
    top_lane = "TOP"
    jungle = "JUNGLE"
    mid_lane = "MIDDLE"
    bot_lane = "BOTTOM"

    def for_id(id_):
        try:
            return Lane.by_id[id_]
        except:
            return None

Lane.by_id = {
    1: Lane.top_lane,
    2: Lane.mid_lane,
    3: Lane.jungle,
    4: Lane.bot_lane
}


class Role(enum.Enum):
    none = "NONE"
    solo = "SOLO"
    duo = "DUO"
    carry = "DUO_CARRY"
    support = "DUO_SUPPORT"

    def for_id(id_):
        try:
            return Role.by_id[id_]
        except:
            return None

Role.by_id = {
    1: Role.duo,
    2: Role.support,
    3: Role.carry,
    4: Role.solo
}


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
    ascension = "ASCENSION_5x5"
    hexakill_twisted_treeline = "HEXAKILL"
    butchers_bridge = "BILGEWATER_ARAM_5x5"
    poro_king = "KING_PORO_5x5"
    nemesis_draft = "COUNTER_PICK"
    black_market = "BILGEWATER_5x5"
    dynamic_queue = "TEAM_BUILDER_DRAFT_UNRANKED_5x5"
    ranked_dynamic_queue = "TEAM_BUILDER_DRAFT_RANKED_5x5"

    def for_id(id_):
        try:
            return Queue.by_id[id_]
        except:
            return None

Queue.by_id = {
    0: Queue.custom,
    65: Queue.aram,
    2: Queue.normal_blind_fives,
    4: Queue.ranked_solo,
    6: Queue.ranked_premade_fives,
    7: Queue.bot_fives,
    8: Queue.normal_blind_threes,
    9: Queue.ranked_premade_threes,
    75: Queue.hexakill_summoners_rift,
    76: Queue.urf,
    14: Queue.normal_draft_fives,
    16: Queue.dominion_blind,
    17: Queue.dominion_draft,
    83: Queue.bot_urf,
    25: Queue.bot_dominion,
    91: Queue.doom_bots_1,
    92: Queue.doom_bots_2,
    93: Queue.doom_bots_5,
    31: Queue.bot_intro_fives,
    32: Queue.bot_beginner_fives,
    33: Queue.bot_intermediate_fives,
    98: Queue.hexakill_twisted_treeline,
    100: Queue.butchers_bridge,
    70: Queue.one_for_all,
    41: Queue.ranked_threes,
    42: Queue.ranked_fives,
    300: Queue.poro_king,
    96: Queue.ascension,
    72: Queue.showdown_solo,
    52: Queue.bot_threes,
    310: Queue.nemesis_draft,
    73: Queue.showdown_duo,
    313: Queue.black_market,
    61: Queue.team_builder,
    400: Queue.dynamic_queue,
    410: Queue.ranked_dynamic_queue
}
ranked_queues = {Queue.ranked_solo, Queue.ranked_threes, Queue.ranked_fives, Queue.ranked_dynamic_queue}


class Tier(enum.Enum):
    challenger = "CHALLENGER"
    master = "MASTER"
    diamond = "DIAMOND"
    platinum = "PLATINUM"
    gold = "GOLD"
    silver = "SILVER"
    bronze = "BRONZE"
    unranked = "UNRANKED"


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
    preseason_6 = "PRESEASON2016"
    season_6 = "SEASON2016"

stats_seasons = {Season.season_3, Season.season_4, Season.season_5, Season.season_6}


class Region(enum.Enum):
    brazil = "br"
    europe_north_east = "eune"
    europe_west = "euw"
    japan = "jp"
    korea = "kr"
    latin_america_north = "lan"
    latin_america_south = "las"
    north_america = "na"
    oceania = "oce"
    pbe = "pbe"
    russia = "ru"
    turkey = "tr"


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
    butchers_bridge = 14


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
    black_market = "BILGEWATER"


class StatSummaryType(enum.Enum):
    normal_fives = "Unranked"
    normal_threes = "Unranked3x3"
    dominion = "OdinUnranked"
    aram = "AramUnranked5x5"
    bot_fives = "CoopVsAI"
    bot_threes = "CoopVsAI3x3"
    ranked_solo = "RankedSolo5x5"
    ranked_threes = "RankedTeam3x3"
    ranked_premade_threes = "RankedPremade3x3"
    ranked_fives = "RankedTeam5x5"
    ranked_premade_fives = "RankedPremade5x5"
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
    black_market = "Bilgewater"


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
    rift_herald = "RIFTHERALD"


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
    blue_trinket = "BLUE_TRINKET"
    sight = "SIGHT_WARD"
    vision = "VISION_WARD"
    yellow_trinket = "YELLOW_TRINKET"
    upgraded_yellow_trinket = "YELLOW_TRINKET_UPGRADE"
    mushroom = "TEEMO_MUSHROOM"
    undefined = "UNDEFINED"
