import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common
import cassiopeia.type.core.common

######################
# Champion Endpoints #
######################

@cassiopeia.type.core.common.inheritdocs
class BlockItem(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    count    int    item count
    id       int    item ID
    """
    def __init__(self, dictionary):
        # int # Item count
        self.count = dictionary.get("count", 0)

        # int # Item ID
        self.id = dictionary.get("id", 0)


@cassiopeia.type.core.common.inheritdocs
class Block(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    items      list<BlockItem>    the items
    recMath    bool               rec math
    type       str                type
    """
    def __init__(self, dictionary):
        # list<BlockItem> # The items
        self.items = [(BlockItem(item) if not isinstance(item, BlockItem) else item) for item in dictionary.get("items", []) if item]

        # bool # RecMath
        self.recMath = dictionary.get("recMath", False)

        # str # Type
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class SpellVars(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    coeff        list<float>    coefficients
    dyn          str            dyn
    key          str            key
    link         str            link
    ranksWith    str            ranks with
    """
    def __init__(self, dictionary):
        # list<float> # Coefficients
        self.coeff = dictionary.get("coeff", [])

        # str # Dyn
        self.dyn = dictionary.get("dyn", "")

        # str # Key
        self.key = dictionary.get("key", "")

        # str # Link
        self.link = dictionary.get("link", "")

        # str # Ranks with
        self.ranksWith = dictionary.get("ranksWith", "")


@cassiopeia.type.core.common.inheritdocs
class LevelTip(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    effect    list<str>    effects
    label     list<str>    labels
    """
    def __init__(self, dictionary):
        # list<str> # effects
        self.effect = dictionary.get("effect", [])

        # list<str> # labels
        self.label = dictionary.get("label", [])


@cassiopeia.type.core.common.inheritdocs
class Stats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    armor                   float    armor
    armorperlevel           float    armor per level 
    attackdamage            float    attack damage
    attackdamageperlevel    float    attack damage per level
    attackrange             float    attack range
    attackspeedoffset       float    attack speed offset
    attackspeedperlevel     float    attack speed per level
    crit                    float    crit chance
    critperlevel            float    crit change per level
    hp                      float    health
    hpperlevel              float    health per level
    hpregen                 float    health regen
    hpregenperlevel         float    health regen per level
    movespeed               float    movespeed
    mp                      float    mana
    mpperlevel              float    mana per level
    mpregen                 float    mana regen
    mpregenperlevel         float    mana regen per level
    spellblock              float    magic resist
    spellblockperlevel      float    magic resist per level
    """
    def __init__(self, dictionary):
        # float # Armor
        self.armor = dictionary.get("armor", 0.0)

        # float # Armor per level 
        self.armorperlevel = dictionary.get("armorperlevel", 0.0)

        # float # Attack damage
        self.attackdamage = dictionary.get("attackdamage", 0.0)

        # float # Attack damage per level
        self.attackdamageperlevel = dictionary.get("attackdamageperlevel", 0.0)

        # float # Attack range
        self.attackrange = dictionary.get("attackrange", 0.0)

        # float # Attack speed offset
        self.attackspeedoffset = dictionary.get("attackspeedoffset", 0.0)

        # float # Attack speed per level
        self.attackspeedperlevel = dictionary.get("attackspeedperlevel", 0.0)

        # float # Crit chance
        self.crit = dictionary.get("crit", 0.0)

        # float # Crit change per level
        self.critperlevel = dictionary.get("critperlevel", 0.0)

        # float # Health
        self.hp = dictionary.get("hp", 0.0)

        # float # Health per level
        self.hpperlevel = dictionary.get("hpperlevel", 0.0)

        # float # Health regen
        self.hpregen = dictionary.get("hpregen", 0.0)

        # float # Health regen per level
        self.hpregenperlevel = dictionary.get("hpregenperlevel", 0.0)

        # float # Movespeed
        self.movespeed = dictionary.get("movespeed", 0.0)

        # float # Mana
        self.mp = dictionary.get("mp", 0.0)

        # float # Mana per level
        self.mpperlevel = dictionary.get("mpperlevel", 0.0)

        # float # Mana regen
        self.mpregen = dictionary.get("mpregen", 0.0)

        # float # Mana regen per level
        self.mpregenperlevel = dictionary.get("mpregenperlevel", 0.0)

        # float # Magic resist
        self.spellblock = dictionary.get("spellblock", 0.0)

        # float # Magic resist per level
        self.spellblockperlevel = dictionary.get("spellblockperlevel", 0.0)


@cassiopeia.type.core.common.inheritdocs
class Skin(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    id      int    ID
    name    str    name
    num     int    number
    """
    def __init__(self, dictionary):
        # int # ID
        self.id = dictionary.get("id", 0)

        # str # Name
        self.name = dictionary.get("name", "")

        # int # Number
        self.num = dictionary.get("num", 0)


@cassiopeia.type.core.common.inheritdocs
class Recommended(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    blocks      list<Block>    blocks
    champion    str            champion
    map         str            map
    mode        str            mode
    priority    bool           priority
    title       str            title
    type        str            type
    """
    def __init__(self, dictionary):
        # list<Block> # Blocks
        self.blocks = [(Block(block) if not isinstance(block, Block) else block) for block in dictionary.get("blocks", []) if block]

        # str # Champion
        self.champion = dictionary.get("champion", "")

        # str # Map
        self.map = dictionary.get("map", "")

        # str # Mode
        self.mode = dictionary.get("mode", "")

        # bool # Priority
        self.priority = dictionary.get("priority", False)

        # str # Title
        self.title = dictionary.get("title", "")

        # str # Type
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class Image(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    full      str    full link
    group     str    group
    h         int    h
    sprite    str    sprite
    w         int    w
    x         int    x
    y         int    y
    """
    def __init__(self, dictionary, is_alt=False):
        # str # Full link
        self.full = dictionary.get("full", "")

        # str # Group
        self.group = dictionary.get("group", "")

        # int # H
        self.h = dictionary.get("h", 0)

        # str # Sprite
        self.sprite = dictionary.get("sprite", "")

        # int # W
        self.w = dictionary.get("w", 0)

        # int # X
        self.x = dictionary.get("x", 0)

        # int # Y
        self.y = dictionary.get("y", 0)

        self._is_alt = is_alt


@cassiopeia.type.core.common.inheritdocs
class Passive(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    description             str      description
    image                   Image    image
    name                    str      name
    sanitizedDescription    str      sanitized description
    """
    def __init__(self, dictionary):
        # str # Description
        self.description = dictionary.get("description", "")

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")


@cassiopeia.type.core.common.inheritdocs
class Info(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    attack        int    attack rating
    defense       int    defense rating
    difficulty    int    difficulty rating
    magic         int    magic rating
    """
    def __init__(self, dictionary):
        # int # Attack rating
        self.attack = dictionary.get("attack", 0)

        # int # Defense rating
        self.defense = dictionary.get("defense", 0)

        # int # Difficulty rating
        self.difficulty = dictionary.get("difficulty", 0)

        # int # Magic rating
        self.magic = dictionary.get("magic", 0)


@cassiopeia.type.core.common.inheritdocs
class ChampionSpell(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    altimages               list<Image>            alternate images
    cooldown                list<float>            cooldown
    cooldownBurn            str                    cooldown burn
    cost                    list<int>              cost
    costBurn                str                    cost burn
    costType                str                    cost type
    description             str                    description
    effect                  list<list<float>>      effects
    effectBurn              list<str>              effect burn
    image                   Image                  image
    key                     str                    key
    leveltip                LevelTip               level tip
    maxrank                 int                    max rank
    name                    str                    name
    range                   list<int> or "self"    range
    rangeBurn               str                    range burn
    resource                str                    resource
    sanitizedDescription    str                    sanitized description
    sanitizedTooltip        str                    sanitized tooltip
    tooltip                 str                    tooltip
    vars                    list<SpellVars>        vars
    """
    def __init__(self, dictionary):
        # list<Image> # Alternate images
        self.altimages = [(Image(img, True) if not isinstance(img, Image) else img) for img in dictionary.get("altimages", []) if img]

        # list<float> # Cooldown
        self.cooldown = dictionary.get("cooldown", [])

        # str # Cooldown burn
        self.cooldownBurn = dictionary.get("cooldownBurn", "")

        # list<int> # Cost
        self.cost = dictionary.get("cost", [])

        # str # Cost burn
        self.costBurn = dictionary.get("costBurn", "")

        # str # Cost type
        self.costType = dictionary.get("costType", "")

        # str # Description
        self.description = dictionary.get("description", "")

        # list<list<float>> # Effects
        self.effect = dictionary.get("effect", [])

        # list<str> # Effect burn
        self.effectBurn = dictionary.get("effectBurn", [])

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # str # Key
        self.key = dictionary.get("key", "")

        # LevelTip # Level tip
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val

        # int # Max rank
        self.maxrank = dictionary.get("maxrank", 0)

        # str # Name
        self.name = dictionary.get("name", "")

        # list<int> or "self" # Range
        self.range = dictionary.get("range", "self")

        # str # Range burn
        self.rangeBurn = dictionary.get("rangeBurn", "")

        # str # Resource
        self.resource = dictionary.get("resource", "")

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")

        # str # Sanitized tooltip
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip", "")

        # str # Tooltip
        self.tooltip = dictionary.get("tooltip", "")

        # list<SpellVars> # Vars
        self.vars = [(SpellVars(svars) if not isinstance(svars, SpellVars) else svars) for svars in dictionary.get("vars", []) if svars]


@cassiopeia.type.core.common.inheritdocs
class Champion(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    allytips       list<str>              ally tips
    blurb          str                    blurb
    enemytips      list<str>              enemy tips
    id             int                    ID
    image          Image                  image
    info           Info                   info
    key            str                    key
    lore           str                    lore
    name           str                    name
    partype        str                    partype
    passive        Passive                passive
    recommended    list<Recommended>      recommended
    skins          list<Skin>             skins
    spells         list<ChampionSpell>    spells
    stats          Stats                  stats
    tags           list<str>              tags
    title          str                    title
    """
    def __init__(self, dictionary):
        # list<str> # Ally tips
        self.allytips = dictionary.get("allytips", [])

        # str # Blurb
        self.blurb = dictionary.get("blurb", "")

        # list<str> # Enemy tips
        self.enemytips = dictionary.get("enemytips", [])

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # Info # Info
        val = dictionary.get("info", None)
        self.info = Info(val) if val and not isinstance(val, Info) else val

        # str # Key
        self.key = dictionary.get("key", "")

        # str # Lore
        self.lore = dictionary.get("lore", "")

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Partype
        self.partype = dictionary.get("partype", "")

        # Passive # Passive
        val = dictionary.get("passive", None)
        self.passive = Passive(val) if val and not isinstance(val, Passive) else val

        # list<Recommended> # Recommended
        self.recommended = [(Recommended(rec) if not isinstance(rec, Recommended) else rec) for rec in dictionary.get("recommended", []) if rec]

        # list<Skin> # Skins
        self.skins = [(Skin(skin) if val and not isinstance(skin, Skin) else skin) for skin in dictionary.get("skins", []) if skin]

        # list<ChampionSpell> # Spells
        self.spells = [(ChampionSpell(spell) if not isinstance(spell, ChampionSpell) else spell) for spell in dictionary.get("spells", []) if spell]

        # Stats # Stats
        val = dictionary.get("stats", None)
        self.stats = Stats(val) if val and not isinstance(val, Stats) else val

        # list<str> # Tags
        self.tags = dictionary.get("tags", [])

        # str # Title
        self.title = dictionary.get("title", "")

    @property
    def item_ids(self):
        """Gets all item IDs contained in this object"""
        ids = set()
        for r in self.recommended:
            for b in r.blocks:
                for i in b.items:
                    ids.add(i.id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class ChampionList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    data       dict<str, Champion>    champion data
    format     str                    format
    keys       dict<str, str>         keys
    type       str                    type
    version    str                    version
    """
    def __init__(self, dictionary):
        # dict<str, Champion> # Champion data
        self.data = {name: Champion(champ) if not isinstance(champ, Champion) else champ for name, champ in dictionary.get("data", {}).items()}

        # str # Format
        self.format = dictionary.get("format", "")

        # dict<str, str> # Keys
        self.keys = dictionary.get("keys", {})

        # str # Type
        self.type = dictionary.get("type", "")

        # str # version
        self.version = dictionary.get("version", "")

    @property
    def item_ids(self):
        """Gets all item IDs contained in this object"""
        ids = set()
        for c in self.data.items():
            ids = ids | c[1].item_ids
        return ids

##################
# Item Endpoints #
##################

@cassiopeia.type.core.common.inheritdocs
class MetaData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    isRune    bool    is a rune
    tier      str     tier
    type      str     type
    """
    def __init__(self, dictionary):
        # bool # Is a rune
        self.isRune = dictionary.get("isRune", False)

        # str # Tier
        self.tier = dictionary.get("tier", "")

        # str # Type
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class Gold(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    base           int     base price
    purchasable    bool    is purchasable
    sell           int     sell price
    total          int     total price
    """
    def __init__(self, dictionary):
        # int # Base price
        self.base = dictionary.get("base", 0)

        # bool # Is purchasable
        self.purchasable = dictionary.get("purchasable", False)

        # int # Sell price
        self.sell = dictionary.get("sell", 0)

        # int # Total price
        self.total = dictionary.get("total", 0)


@cassiopeia.type.core.common.inheritdocs
class BasicDataStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    FlatArmorMod                           float    the FlatArmorMod
    FlatAttackSpeedMod                     float    the FlatAttackSpeedMod
    FlatBlockMod                           float    the FlatBlockMod
    FlatCritChanceMod                      float    the FlatCritChanceMod
    FlatCritDamageMod                      float    the FlatCritDamageMod
    FlatEXPBonus                           float    the FlatEXPBonus
    FlatEnergyPoolMod                      float    the FlatEnergyPoolMod
    FlatEnergyRegenMod                     float    the FlatEnergyRegenMod
    FlatHPPoolMod                          float    the FlatHPPoolMod
    FlatHPRegenMod                         float    the FlatHPRegenMod
    FlatMPPoolMod                          float    the FlatMPPoolMod
    FlatMPRegenMod                         float    the FlatMPRegenMod
    FlatMagicDamageMod                     float    the FlatMagicDamageMod
    FlatMovementSpeedMod                   float    the FlatMovementSpeedMod
    FlatPhysicalDamageMod                  float    the FlatPhysicalDamageMod
    FlatSpellBlockMod                      float    the FlatSpellBlockMod
    PercentArmorMod                        float    the PercentArmorMod
    PercentAttackSpeedMod                  float    the PercentAttackSpeedMod
    PercentBlockMod                        float    the PercentBlockMod
    PercentCritChanceMod                   float    the PercentCritChanceMod
    PercentCritDamageMod                   float    the PercentCritDamageMod
    PercentDodgeMod                        float    the PercentDodgeMod
    PercentEXPBonus                        float    the PercentEXPBonus
    PercentHPPoolMod                       float    the PercentHPPoolMod
    PercentHPRegenMod                      float    the PercentHPRegenMod
    PercentLifeStealMod                    float    the PercentLifeStealMod
    PercentMPPoolMod                       float    the PercentMPPoolMod
    PercentMPRegenMod                      float    the PercentMPRegenMod
    PercentMagicDamageMod                  float    the PercentMagicDamageMod
    PercentMovementSpeedMod                float    the PercentMovementSpeedMod
    PercentPhysicalDamageMod               float    the PercentPhysicalDamageMod
    PercentSpellBlockMod                   float    the PercentSpellBlockMod
    PercentSpellVampMod                    float    the PercentSpellVampMod
    rFlatArmorModPerLevel                  float    the rFlatArmorModPerLevel
    rFlatArmorPenetrationMod               float    the rFlatArmorPenetrationMod
    rFlatArmorPenetrationModPerLevel       float    the rFlatArmorPenetrationModPerLevel
    rFlatCritChanceModPerLevel             float    the rFlatCritChanceModPerLevel
    rFlatCritDamageModPerLevel             float    the rFlatCritDamageModPerLevel
    rFlatDodgeMod                          float    the rFlatDodgeMod
    rFlatDodgeModPerLevel                  float    the rFlatDodgeModPerLevel
    rFlatEnergyModPerLevel                 float    the rFlatEnergyModPerLevel
    rFlatEnergyRegenModPerLevel            float    the rFlatEnergyRegenModPerLevel
    rFlatGoldPer10Mod                      float    the rFlatGoldPer10Mod
    rFlatHPModPerLevel                     float    the rFlatHPModPerLevel
    rFlatHPRegenModPerLevel                float    the rFlatHPRegenModPerLevel
    rFlatMPModPerLevel                     float    the rFlatMPModPerLevel
    rFlatMPRegenModPerLevel                float    the rFlatMPRegenModPerLevel
    rFlatMagicDamageModPerLevel            float    the rFlatMagicDamageModPerLevel
    rFlatMagicPenetrationMod               float    the rFlatMagicPenetrationMod
    rFlatMagicPenetrationModPerLevel       float    the rFlatMagicPenetrationModPerLevel
    rFlatMovementSpeedModPerLevel          float    the rFlatMovementSpeedModPerLevel
    rFlatPhysicalDamageModPerLevel         float    the rFlatPhysicalDamageModPerLevel
    rFlatSpellBlockModPerLevel             float    the rFlatSpellBlockModPerLevel
    rFlatTimeDeadMod                       float    the rFlatTimeDeadMod
    rFlatTimeDeadModPerLevel               float    the rFlatTimeDeadModPerLevel
    rPercentArmorPenetrationMod            float    the rPercentArmorPenetrationMod
    rPercentArmorPenetrationModPerLevel    float    the rPercentArmorPenetrationModPerLevel
    rPercentAttackSpeedModPerLevel         float    the rPercentAttackSpeedModPerLevel
    rPercentCooldownMod                    float    the rPercentCooldownMod
    rPercentCooldownModPerLevel            float    the rPercentCooldownModPerLevel
    rPercentMagicPenetrationMod            float    the rPercentMagicPenetrationMod
    rPercentMagicPenetrationModPerLevel    float    the rPercentMagicPenetrationModPerLevel
    rPercentMovementSpeedModPerLevel       float    the rPercentMovementSpeedModPerLevel
    rPercentTimeDeadMod                    float    the rPercentTimeDeadMod
    rPercentTimeDeadModPerLevel            float    the rPercentTimeDeadModPerLevel
    """
    def __init__(self, dictionary):
        # float # The FlatArmorMod
        self.FlatArmorMod = dictionary.get("FlatArmorMod", 0.0)

        # float # The FlatAttackSpeedMod
        self.FlatAttackSpeedMod = dictionary.get("FlatAttackSpeedMod", 0.0)

        # float # The FlatBlockMod
        self.FlatBlockMod = dictionary.get("FlatBlockMod", 0.0)

        # float # The FlatCritChanceMod
        self.FlatCritChanceMod = dictionary.get("FlatCritChanceMod", 0.0)

        # float # The FlatCritDamageMod
        self.FlatCritDamageMod = dictionary.get("FlatCritDamageMod", 0.0)

        # float # The FlatEXPBonus
        self.FlatEXPBonus = dictionary.get("FlatEXPBonus", 0.0)

        # float # The FlatEnergyPoolMod
        self.FlatEnergyPoolMod = dictionary.get("FlatEnergyPoolMod", 0.0)

        # float # The FlatEnergyRegenMod
        self.FlatEnergyRegenMod = dictionary.get("FlatEnergyRegenMod", 0.0)

        # float # The FlatHPPoolMod
        self.FlatHPPoolMod = dictionary.get("FlatHPPoolMod", 0.0)

        # float # The FlatHPRegenMod
        self.FlatHPRegenMod = dictionary.get("FlatHPRegenMod", 0.0)

        # float # The FlatMPPoolMod
        self.FlatMPPoolMod = dictionary.get("FlatMPPoolMod", 0.0)

        # float # The FlatMPRegenMod
        self.FlatMPRegenMod = dictionary.get("FlatMPRegenMod", 0.0)

        # float # The FlatMagicDamageMod
        self.FlatMagicDamageMod = dictionary.get("FlatMagicDamageMod", 0.0)

        # float # The FlatMovementSpeedMod
        self.FlatMovementSpeedMod = dictionary.get("FlatMovementSpeedMod", 0.0)

        # float # The FlatPhysicalDamageMod
        self.FlatPhysicalDamageMod = dictionary.get("FlatPhysicalDamageMod", 0.0)

        # float # The FlatSpellBlockMod
        self.FlatSpellBlockMod = dictionary.get("FlatSpellBlockMod", 0.0)

        # float # The PercentArmorMod
        self.PercentArmorMod = dictionary.get("PercentArmorMod", 0.0)

        # float # The PercentAttackSpeedMod
        self.PercentAttackSpeedMod = dictionary.get("PercentAttackSpeedMod", 0.0)

        # float # The PercentBlockMod
        self.PercentBlockMod = dictionary.get("PercentBlockMod", 0.0)

        # float # The PercentCritChanceMod
        self.PercentCritChanceMod = dictionary.get("PercentCritChanceMod", 0.0)

        # float # The PercentCritDamageMod
        self.PercentCritDamageMod = dictionary.get("PercentCritDamageMod", 0.0)

        # float # The PercentDodgeMod
        self.PercentDodgeMod = dictionary.get("PercentDodgeMod", 0.0)

        # float # The PercentEXPBonus
        self.PercentEXPBonus = dictionary.get("PercentEXPBonus", 0.0)

        # float # The PercentHPPoolMod
        self.PercentHPPoolMod = dictionary.get("PercentHPPoolMod", 0.0)

        # float # The PercentHPRegenMod
        self.PercentHPRegenMod = dictionary.get("PercentHPRegenMod", 0.0)

        # float # The PercentLifeStealMod
        self.PercentLifeStealMod = dictionary.get("PercentLifeStealMod", 0.0)

        # float # The PercentMPPoolMod
        self.PercentMPPoolMod = dictionary.get("PercentMPPoolMod", 0.0)

        # float # The PercentMPRegenMod
        self.PercentMPRegenMod = dictionary.get("PercentMPRegenMod", 0.0)

        # float # The PercentMagicDamageMod
        self.PercentMagicDamageMod = dictionary.get("PercentMagicDamageMod", 0.0)

        # float # The PercentMovementSpeedMod
        self.PercentMovementSpeedMod = dictionary.get("PercentMovementSpeedMod", 0.0)

        # float # The PercentPhysicalDamageMod
        self.PercentPhysicalDamageMod = dictionary.get("PercentPhysicalDamageMod", 0.0)

        # float # The PercentSpellBlockMod
        self.PercentSpellBlockMod = dictionary.get("PercentSpellBlockMod", 0.0)

        # float # The PercentSpellVampMod
        self.PercentSpellVampMod = dictionary.get("PercentSpellVampMod", 0.0)

        # float # The rFlatArmorModPerLevel
        self.rFlatArmorModPerLevel = dictionary.get("rFlatArmorModPerLevel", 0.0)

        # float # The rFlatArmorPenetrationMod
        self.rFlatArmorPenetrationMod = dictionary.get("rFlatArmorPenetrationMod", 0.0)

        # float # The rFlatArmorPenetrationModPerLevel
        self.rFlatArmorPenetrationModPerLevel = dictionary.get("rFlatArmorPenetrationModPerLevel", 0.0)

        # float # The rFlatCritChanceModPerLevel
        self.rFlatCritChanceModPerLevel = dictionary.get("rFlatCritChanceModPerLevel", 0.0)

        # float # The rFlatCritDamageModPerLevel
        self.rFlatCritDamageModPerLevel = dictionary.get("rFlatCritDamageModPerLevel", 0.0)

        # float # The rFlatDodgeMod
        self.rFlatDodgeMod = dictionary.get("rFlatDodgeMod", 0.0)

        # float # The rFlatDodgeModPerLevel
        self.rFlatDodgeModPerLevel = dictionary.get("rFlatDodgeModPerLevel", 0.0)

        # float # The rFlatEnergyModPerLevel
        self.rFlatEnergyModPerLevel = dictionary.get("rFlatEnergyModPerLevel", 0.0)

        # float # The rFlatEnergyRegenModPerLevel
        self.rFlatEnergyRegenModPerLevel = dictionary.get("rFlatEnergyRegenModPerLevel", 0.0)

        # float # The rFlatGoldPer10Mod
        self.rFlatGoldPer10Mod = dictionary.get("rFlatGoldPer10Mod", 0.0)

        # float # The rFlatHPModPerLevel
        self.rFlatHPModPerLevel = dictionary.get("rFlatHPModPerLevel", 0.0)

        # float # The rFlatHPRegenModPerLevel
        self.rFlatHPRegenModPerLevel = dictionary.get("rFlatHPRegenModPerLevel", 0.0)

        # float # The rFlatMPModPerLevel
        self.rFlatMPModPerLevel = dictionary.get("rFlatMPModPerLevel", 0.0)

        # float # The rFlatMPRegenModPerLevel
        self.rFlatMPRegenModPerLevel = dictionary.get("rFlatMPRegenModPerLevel", 0.0)

        # float # The rFlatMagicDamageModPerLevel
        self.rFlatMagicDamageModPerLevel = dictionary.get("rFlatMagicDamageModPerLevel", 0.0)

        # float # The rFlatMagicPenetrationMod
        self.rFlatMagicPenetrationMod = dictionary.get("rFlatMagicPenetrationMod", 0.0)

        # float # The rFlatMagicPenetrationModPerLevel
        self.rFlatMagicPenetrationModPerLevel = dictionary.get("rFlatMagicPenetrationModPerLevel", 0.0)

        # float # The rFlatMovementSpeedModPerLevel
        self.rFlatMovementSpeedModPerLevel = dictionary.get("rFlatMovementSpeedModPerLevel", 0.0)

        # float # The rFlatPhysicalDamageModPerLevel
        self.rFlatPhysicalDamageModPerLevel = dictionary.get("rFlatPhysicalDamageModPerLevel", 0.0)

        # float # The rFlatSpellBlockModPerLevel
        self.rFlatSpellBlockModPerLevel = dictionary.get("rFlatSpellBlockModPerLevel", 0.0)

        # float # The rFlatTimeDeadMod
        self.rFlatTimeDeadMod = dictionary.get("rFlatTimeDeadMod", 0.0)

        # float # The rFlatTimeDeadModPerLevel
        self.rFlatTimeDeadModPerLevel = dictionary.get("rFlatTimeDeadModPerLevel", 0.0)

        # float # The rPercentArmorPenetrationMod
        self.rPercentArmorPenetrationMod = dictionary.get("rPercentArmorPenetrationMod", 0.0)

        # float # The rPercentArmorPenetrationModPerLevel
        self.rPercentArmorPenetrationModPerLevel = dictionary.get("rPercentArmorPenetrationModPerLevel", 0.0)

        # float # The rPercentAttackSpeedModPerLevel
        self.rPercentAttackSpeedModPerLevel = dictionary.get("rPercentAttackSpeedModPerLevel", 0.0)

        # float # The rPercentCooldownMod
        self.rPercentCooldownMod = dictionary.get("rPercentCooldownMod", 0.0)

        # float # The rPercentCooldownModPerLevel
        self.rPercentCooldownModPerLevel = dictionary.get("rPercentCooldownModPerLevel", 0.0)

        # float # The rPercentMagicPenetrationMod
        self.rPercentMagicPenetrationMod = dictionary.get("rPercentMagicPenetrationMod", 0.0)

        # float # The rPercentMagicPenetrationModPerLevel
        self.rPercentMagicPenetrationModPerLevel = dictionary.get("rPercentMagicPenetrationModPerLevel", 0.0)

        # float # The rPercentMovementSpeedModPerLevel
        self.rPercentMovementSpeedModPerLevel = dictionary.get("rPercentMovementSpeedModPerLevel", 0.0)

        # float # The rPercentTimeDeadMod
        self.rPercentTimeDeadMod = dictionary.get("rPercentTimeDeadMod", 0.0)

        # float # The rPercentTimeDeadModPerLevel
        self.rPercentTimeDeadModPerLevel = dictionary.get("rPercentTimeDeadModPerLevel", 0.0)


@cassiopeia.type.core.common.inheritdocs
class ItemTree(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    header    str          the header
    tags      list[str]    tags
    """
    def __init__(self, dictionary):
        # str # The header
        self.header = dictionary.get("header", "")

        # list[str] # Tags
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class Item(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    colloq                  str                colloq
    consumeOnFull           bool               consume on full
    consumed                bool               consumed
    depth                   int                depth
    description             str                description
    from_                   list<str>          from
    gold                    Gold               data dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
    group                   str                group
    hideFromAll             bool               hide from all
    id                      int                ID
    image                   Image              image
    inStore                 bool               in store
    into                    list<str>          into
    maps                    dict<str, bool>    maps
    name                    str                name
    plaintext               str                plain text
    requiredChampion        str                required champion
    rune                    MetaData           rune
    sanitizedDescription    str                sanitized description
    specialRecipe           int                special recipe
    stacks                  int                stacks
    tags                    list<str>          tags
    """
    def __init__(self, dictionary):
        # str # Colloq
        self.colloq = dictionary.get("colloq", "")

        # bool # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull", False)

        # bool # Consumed
        self.consumed = dictionary.get("consumed", False)

        # int # Depth
        self.depth = dictionary.get("depth", 0)

        # str # Description
        self.description = dictionary.get("description", "")

        # list<str> # From
        self.from_ = dictionary.get("from", [])

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val

        # str # Group
        self.group = dictionary.get("group", "")

        # bool # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll", False)

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # bool # In store
        self.inStore = dictionary.get("inStore", False)

        # list<str> # into
        self.into = dictionary.get("into", [])

        # dict<str, bool> # Maps
        self.maps = dictionary.get("maps", {})

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Plain text
        self.plaintext = dictionary.get("plaintext", "")

        # str # Required champion
        self.requiredChampion = dictionary.get("requiredChampion", "")

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe", 0)

        # int # Stacks
        self.stacks = dictionary.get("stacks", 0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        # Sometimes Riot sends {} instead of no value for this field when it's blank.
        self.stats = None if not val else BasicDataStats(val) if not isinstance(val, BasicDataStats) else val

        # list<str> # Tags
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class Group(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    MaxGroupOwnable    str    max ownable of group
    key                str    key
    """
    def __init__(self, dictionary):
        # str # Max ownable of group
        self.MaxGroupOwnable = dictionary.get("MaxGroupOwnable", "")

        # str # Key
        self.key = dictionary.get("key", "")


@cassiopeia.type.core.common.inheritdocs
class BasicData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    colloq                  str                colloq
    consumeOnFull           bool               consume on full
    consumed                bool               consumed
    depth                   int                depth
    description             str                description
    from_                   list<str>          from
    gold                    Gold               data dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
    group                   str                group
    hideFromAll             bool               hide from all
    id                      int                ID
    image                   Image              image
    inStore                 bool               in store
    into                    list<str>          into
    maps                    dict<str, bool>    maps
    name                    str                name
    plaintext               str                plain text
    requiredChampion        str                required champion
    rune                    MetaData           rune
    sanitizedDescription    str                sanitized description
    specialRecipe           int                special recipe
    stacks                  int                stacks
    stats                   BasicDataStats     stats
    tags                    list[str]          tags
    """
    def __init__(self, dictionary):
        # str # Colloq
        self.colloq = dictionary.get("colloq", "")

        # bool # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull", False)

        # bool # Consumed
        self.consumed = dictionary.get("consumed", False)

        # int # Depth
        self.depth = dictionary.get("depth", 0)

        # str # Description
        self.description = dictionary.get("description", "")

        # list<str> # From
        self.from_ = dictionary.get("from", [])

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val

        # str # Group
        self.group = dictionary.get("group", "")

        # bool # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll", False)

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # bool # In store
        self.inStore = dictionary.get("inStore", False)

        # list<str> # into
        self.into = dictionary.get("into", [])

        # dict<str, bool> # Maps
        self.maps = dictionary.get("maps", {})

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Plain text
        self.plaintext = dictionary.get("plaintext", "")

        # str # Required champion
        self.requiredChampion = dictionary.get("requiredChampion", "")

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe", 0)

        # int # Stacks
        self.stacks = dictionary.get("stacks", 0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val

        # list[str] # Tags
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class ItemList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    basic      BasicData         basic data
    data       dict<str, Item>   item data
    groups     list<Group>       groups
    tree       list<ItemTree>    item tree
    type       str               type
    version    str               version
    """
    def __init__(self, dictionary):
        # BasicData # Basic data
        val = dictionary.get("basic", None)
        self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val

        # dict<str, Item> # Item data
        self.data = {id_: Item(item) if not isinstance(item, Item) else item for id_, item in dictionary.get("data", {}).items()}

        # list<Group> # Groups
        self.groups = [(Group(group) if not isinstance(group, Group) else group) for group in dictionary.get("groups", []) if group]

        # list<ItemTree> # Item tree
        self.tree = [(ItemTree(tree) if not isinstance(tree, ItemTree) else tree) for tree in dictionary.get("tree", []) if tree]

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

######################
# Language Endpoints #
######################

@cassiopeia.type.core.common.inheritdocs
class LanguageStrings(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    data       dict<str, str>    language str data
    type       str               type
    version    str               version
    """
    def __init__(self, dictionary):
        # dict<str, str> # Language str data
        self.data = dictionary.get("data", {})

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

################
# Map Endpoint #
################

@cassiopeia.type.core.common.inheritdocs
class MapDetails(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    image                    Image        image
    mapId                    int          ID
    mapName                  str          name
    unpurchasableItemList    list<int>    items that can't be purchased on this map (IDs)
    """
    def __init__(self, dictionary):
        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # int # ID
        self.mapId = dictionary.get("mapId", 0)

        # str # Name
        self.mapName = dictionary.get("mapName", "")

        # list<int> # Items that can't be purchased on this map (IDs)
        self.unpurchasableItemList = dictionary.get("unpurchasableItemList", [])


@cassiopeia.type.core.common.inheritdocs
class MapData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    data       dict<str, MapDetails>    map data
    type       str                      type
    version    str                      version
    """
    def __init__(self, dictionary):
        # dict<str, MapDetails> # Map data
        self.data = {id_: MapDetails(map_) if not isinstance(map_, MapDetails) else map_ for id_, map_ in dictionary.get("data", {}).items()}

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

#####################
# Mastery Endpoints #
#####################

@cassiopeia.type.core.common.inheritdocs
class MasteryTreeItem(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    masteryId    int    mastery ID
    prereq       str    prerequisites
    """
    def __init__(self, dictionary):
        # int # Mastery ID
        self.masteryId = dictionary.get("masteryId", 0)

        # str # Prerequisites
        self.prereq = dictionary.get("prereq", "")


@cassiopeia.type.core.common.inheritdocs
class MasteryTreeList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    masteryTreeItems    list<MasteryTreeItem>    mastery tree items
    """
    def __init__(self, dictionary):
        # list<MasteryTreeItem> # Mastery tree items
        self.masteryTreeItems = [(MasteryTreeItem(item) if not isinstance(item, MasteryTreeItem) else item) for item in dictionary.get("masteryTreeItems", []) if item]


@cassiopeia.type.core.common.inheritdocs
class MasteryTree(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Defense    list<MasteryTreeList>    defense tree
    Offense    list<MasteryTreeList>    offense tree
    Utility    list<MasteryTreeList>    utility tree
    """
    def __init__(self, dictionary):
        # list<MasteryTreeList> # Defense tree
        self.Defense = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Defense", []) if list_]

        # list<MasteryTreeList> # Offense tree
        self.Offense = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Offense", []) if list_]

        # list<MasteryTreeList> # Utility tree
        self.Utility = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Utility", []) if list_]


@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    description             list<str>    description
    id                      int          iD
    image                   Image        image
    masteryTree             str          legal values: Defense, Offense, Utility
    name                    str          name
    prereq                  str          prerequisites
    ranks                   int          ranks
    sanitizedDescription    list<str>    sanitized description
    """
    def __init__(self, dictionary):
        # list<str> # Description
        self.description = dictionary.get("description", [])

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # str # Legal values: Defense, Offense, Utility
        self.masteryTree = dictionary.get("masteryTree", "")

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Prerequisites
        self.prereq = dictionary.get("prereq", "")

        # int # Ranks
        self.ranks = dictionary.get("ranks", 0)

        # list<str> # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", [])


@cassiopeia.type.core.common.inheritdocs
class MasteryList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    data       dict<str, Mastery>    mastery data
    tree       MasteryTree           mastery tree
    type       str                   type
    version    str                   version
    """
    def __init__(self, dictionary):
        # dict<str, Mastery> # Mastery data
        self.data = {id_: Mastery(mastery) if not isinstance(mastery, Mastery) else mastery for id_, mastery in dictionary.get("data", {}).items()}

        # MasteryTree # Mastery tree
        val = dictionary.get("tree", None)
        self.tree = MasteryTree(val) if val and not isinstance(val, MasteryTree) else val

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

##################
# Realm Endpoint #
##################

@cassiopeia.type.core.common.inheritdocs
class Realm(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    cdn               str               the base CDN url
    css               str               latest changed version of Dragon Magic's css file
    dd                str               latest changed version of Dragon Magic
    l                 str               default language for this realm
    lg                str               legacy script mode for IE6 or older
    n                 dict<str, str>    latest changed version for each data type listed
    profileiconmax    int               special behavior number identifying the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0
    store             str               additional api data drawn from other sources that may be related to data dragon functionality
    v                 str               current version of this file for this realm
    """
    def __init__(self, dictionary):
        # str # The base CDN url.
        self.cdn = dictionary.get("cdn", "")

        # str # Latest changed version of Dragon Magic's css file.
        self.css = dictionary.get("css", "")

        # str # Latest changed version of Dragon Magic.
        self.dd = dictionary.get("dd", "")

        # str # Default language for this realm.
        self.l = dictionary.get("l", "")

        # str # Legacy script mode for IE6 or older.
        self.lg = dictionary.get("lg", "")

        # dict<str, str> # Latest changed version for each data type listed.
        self.n = dictionary.get("n", {})

        # int # Special behavior number identifying the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0
        self.profileiconmax = dictionary.get("profileiconmax", 0)

        # str # Additional api data drawn from other sources that may be related to data dragon functionality.
        self.store = dictionary.get("store", "")

        # str # Current version of this file for this realm.
        self.v = dictionary.get("v", "")

##################
# Rune Endpoints #
##################

@cassiopeia.type.core.common.inheritdocs
class Rune(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    colloq                  str                colloq
    consumeOnFull           bool               consume on full
    consumed                bool               consumed
    depth                   int                depth
    description             str                description
    from_                   list<str>          from
    group                   str                group
    hideFromAll             bool               hide from all
    id                      int                ID
    image                   Image              image
    inStore                 bool               in store
    into                    list<str>          into
    maps                    dict<str, bool>    maps
    name                    str                name
    plaintext               str                plain text
    requiredChampion        str                required champion
    rune                    MetaData           rune
    sanitizedDescription    str                sanitized description
    specialRecipe           int                special recipe
    stacks                  int                stacks
    stats                   BasicDataStats     stats
    tags                    list<str>          tags
    """
    def __init__(self, dictionary):
        # str # Colloq
        self.colloq = dictionary.get("colloq", "")

        # bool # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull", False)

        # bool # Consumed
        self.consumed = dictionary.get("consumed", False)

        # int # Depth
        self.depth = dictionary.get("depth", 0)

        # str # Description
        self.description = dictionary.get("description", "")

        # list<str> # From
        self.from_ = dictionary.get("from", [])

        # str # Group
        self.group = dictionary.get("group", "")

        # bool # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll", False)

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # bool # In store
        self.inStore = dictionary.get("inStore", False)

        # list<str> # into
        self.into = dictionary.get("into", [])

        # dict<str, bool> # Maps
        self.maps = dictionary.get("maps", {})

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Plain text
        self.plaintext = dictionary.get("plaintext", "")

        # str # Required champion
        self.requiredChampion = dictionary.get("requiredChampion", "")

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe", 0)

        # int # Stacks
        self.stacks = dictionary.get("stacks", 0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val

        # list<str> # Tags
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class RuneList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    basic      BasicData          basic data
    data       dict<str, Rune>    rune data
    type       str                type
    version    str                version
    """
    def __init__(self, dictionary):
        # BasicData # Basic data
        val = dictionary.get("basic", None)
        self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val

        # dict<str, Rune> # Rune data
        self.data = {id_: Rune(rune) if not isinstance(rune, Rune) else rune for id_, rune in dictionary.get("data", {}).items()}

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

############################
# Summoner Spell Endpoints #
############################

@cassiopeia.type.core.common.inheritdocs
class SummonerSpell(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    cooldown                list<float>            cooldown
    cooldownBurn            str                    cooldown burn
    cost                    list<int>              cost
    costBurn                str                    cost burn
    costType                str                    cost type
    description             str                    description
    effect                  list<list<float>>      effects
    effectBurn              list<str>              effect burn 
    id                      int                    iD
    image                   Image                  image
    key                     str                    key
    leveltip                LevelTip               level tip
    maxrank                 int                    max rank
    modes                   list<str>              modes
    name                    str                    name
    range                   list<int> or "self"    range
    rangeBurn               str                    range burn
    resource                str                    resource
    sanitizedDescription    str                    sanitized description
    sanitizedTooltip        str                    sanitized tooltip
    summonerLevel           int                    summoner level
    tooltip                 str                    tooltip
    vars                    list<SpellVars>        spell vars
    """
    def __init__(self, dictionary):
        # list<float> # Cooldown
        self.cooldown = dictionary.get("cooldown", [])

        # str # Cooldown burn
        self.cooldownBurn = dictionary.get("cooldownBurn", "")

        # list<int> # Cost
        self.cost = dictionary.get("cost", [])

        # str # Cost burn
        self.costBurn = dictionary.get("costBurn", "")

        # str # Cost type
        self.costType = dictionary.get("costType", "")

        # str # Description
        self.description = dictionary.get("description", "")

        # list<list<float>> # Effects
        self.effect = dictionary.get("effect", [])

        # list<str> # Effect burn 
        self.effectBurn = dictionary.get("effectBurn", [])

        # int # ID
        self.id = dictionary.get("id", 0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # str # Key
        self.key = dictionary.get("key", "")

        # LevelTip # Level tip
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val

        # int # Max rank
        self.maxrank = dictionary.get("maxrank", 0)

        # list<str> # Modes
        self.modes = dictionary.get("modes", [])

        # str # Name
        self.name = dictionary.get("name", "")

        # list<int> or "self" # Range
        self.range = dictionary.get("range", "self")

        # str # Range burn
        self.rangeBurn = dictionary.get("rangeBurn", "")

        # str # Resource
        self.resource = dictionary.get("resource", "")

        # str # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")

        # str # Sanitized tooltip
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip", "")

        # int # Summoner level
        self.summonerLevel = dictionary.get("summonerLevel", 0)

        # str # Tooltip
        self.tooltip = dictionary.get("tooltip", "")

        # list<SpellVars> # Spell vars
        self.vars = [(SpellVars(svars) if not isinstance(svars, SpellVars) else svars) for svars in dictionary.get("vars", []) if svars]


@cassiopeia.type.core.common.inheritdocs
class SummonerSpellList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    data       dict<str, SummonerSpell>    summoner spell data
    type       str                         type
    version    str                         version
    """
    def __init__(self, dictionary):
        # dict<str, SummonerSpell> # Summoner spell data
        self.data = {id_: SummonerSpell(spell) if not isinstance(spell, SummonerSpell) else spell for id_, spell in dictionary.get("data", {}).items()}

        # str # Type
        self.type = dictionary.get("type", "")

        # str # Version
        self.version = dictionary.get("version", "")

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_bind_block_item():
    global BlockItem
    class BlockItem(BlockItem, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "BlockItem"
        count = sqlalchemy.Column(sqlalchemy.Integer)
        id = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _block_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Block._id", ondelete="CASCADE"))

def sa_bind_block():
    global Block
    class Block(Block, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Block"
        items = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.BlockItem", cascade="all, delete-orphan", passive_deletes=True)
        recMath = sqlalchemy.Column(sqlalchemy.Boolean)
        type = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _recommended_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Recommended._id", ondelete="CASCADE"))

def sa_bind_spell_vars():
    global SpellVars
    class SpellVars(SpellVars, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "SpellVars"
        coeff = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        dyn = sqlalchemy.Column(sqlalchemy.String(30))
        key = sqlalchemy.Column(sqlalchemy.String(30))
        link = sqlalchemy.Column(sqlalchemy.String(30))
        ranksWith = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _c_spell_key = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey("ChampionSpell.key", ondelete="CASCADE"))
        _s_spell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("SummonerSpell.id", ondelete="CASCADE"))

def sa_bind_level_tip():
    global LevelTip
    class LevelTip(LevelTip, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "LevelTip"
        effect = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        label = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _c_spell_key = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey("ChampionSpell.key", ondelete="CASCADE"))
        _s_spell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("SummonerSpell.id", ondelete="CASCADE"))

def sa_bind_stats():
    global Stats
    class Stats(Stats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Stats"
        armor = sqlalchemy.Column(sqlalchemy.Float)
        armorperlevel = sqlalchemy.Column(sqlalchemy.Float)
        attackdamage = sqlalchemy.Column(sqlalchemy.Float)
        attackdamageperlevel = sqlalchemy.Column(sqlalchemy.Float)
        attackrange = sqlalchemy.Column(sqlalchemy.Float)
        attackspeedoffset = sqlalchemy.Column(sqlalchemy.Float)
        attackspeedperlevel = sqlalchemy.Column(sqlalchemy.Float)
        crit = sqlalchemy.Column(sqlalchemy.Float)
        critperlevel = sqlalchemy.Column(sqlalchemy.Float)
        hp = sqlalchemy.Column(sqlalchemy.Float)
        hpperlevel = sqlalchemy.Column(sqlalchemy.Float)
        hpregen = sqlalchemy.Column(sqlalchemy.Float)
        hpregenperlevel = sqlalchemy.Column(sqlalchemy.Float)
        movespeed = sqlalchemy.Column(sqlalchemy.Float)
        mp = sqlalchemy.Column(sqlalchemy.Float)
        mpperlevel = sqlalchemy.Column(sqlalchemy.Float)
        mpregen = sqlalchemy.Column(sqlalchemy.Float)
        mpregenperlevel = sqlalchemy.Column(sqlalchemy.Float)
        spellblock = sqlalchemy.Column(sqlalchemy.Float)
        spellblockperlevel = sqlalchemy.Column(sqlalchemy.Float)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))
        _rune_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Rune.id", ondelete="CASCADE"))
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_skin():
    global Skin
    class Skin(Skin, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Skin"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        num = sqlalchemy.Column(sqlalchemy.Integer)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_recommended():
    global Recommended
    class Recommended(Recommended, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Recommended"
        blocks = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Block", cascade="all, delete-orphan", passive_deletes=True)
        champion = sqlalchemy.Column(sqlalchemy.String(30))
        map = sqlalchemy.Column(sqlalchemy.String(30))
        mode = sqlalchemy.Column(sqlalchemy.String(30))
        priority = sqlalchemy.Column(sqlalchemy.Boolean)
        title = sqlalchemy.Column(sqlalchemy.String(50))
        type = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_image():
    global Image
    class Image(Image, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Image"
        full = sqlalchemy.Column(sqlalchemy.String(50))
        group = sqlalchemy.Column(sqlalchemy.String(30))
        h = sqlalchemy.Column(sqlalchemy.Integer)
        sprite = sqlalchemy.Column(sqlalchemy.String(30))
        w = sqlalchemy.Column(sqlalchemy.Integer)
        x = sqlalchemy.Column(sqlalchemy.Integer)
        y = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _is_alt = sqlalchemy.Column(sqlalchemy.Boolean)
        _passive_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Passive._id", ondelete="CASCADE"))
        _c_spell_key = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey("ChampionSpell.key", ondelete="CASCADE"))
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))
        _map_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MapDetails.mapId", ondelete="CASCADE"))
        _mastery_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Mastery.id", ondelete="CASCADE"))
        _rune_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Rune.id", ondelete="CASCADE"))
        _s_spell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("SummonerSpell.id", ondelete="CASCADE"))

def sa_bind_passive():
    global Passive
    class Passive(Passive, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Passive"
        description = sqlalchemy.Column(sqlalchemy.Text)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_info():
    global Info
    class Info(Info, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ChampionInfo"
        attack = sqlalchemy.Column(sqlalchemy.Integer)
        defense = sqlalchemy.Column(sqlalchemy.Integer)
        difficulty = sqlalchemy.Column(sqlalchemy.Integer)
        magic = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_champion_spell():
    global ChampionSpell
    class ChampionSpell(ChampionSpell, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ChampionSpell"
        altimages = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", primaryjoin="and_(cassiopeia.type.dto.staticdata.ChampionSpell.key==cassiopeia.type.dto.staticdata.Image._c_spell_key, cassiopeia.type.dto.staticdata.Image._is_alt==True)", cascade="all, delete-orphan", passive_deletes=True)
        cooldown = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        cooldownBurn = sqlalchemy.Column(sqlalchemy.String(30))
        cost = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        costBurn = sqlalchemy.Column(sqlalchemy.String(30))
        costType = sqlalchemy.Column(sqlalchemy.String(50))
        description = sqlalchemy.Column(sqlalchemy.Text)
        effect = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        effectBurn = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", primaryjoin="and_(cassiopeia.type.dto.staticdata.ChampionSpell.key==cassiopeia.type.dto.staticdata.Image._c_spell_key, cassiopeia.type.dto.staticdata.Image._is_alt==False)", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        key = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
        leveltip = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.LevelTip", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        maxrank = sqlalchemy.Column(sqlalchemy.Integer)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        range = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        rangeBurn = sqlalchemy.Column(sqlalchemy.String(30))
        resource = sqlalchemy.Column(sqlalchemy.String(50))
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        sanitizedTooltip = sqlalchemy.Column(sqlalchemy.Text)
        tooltip = sqlalchemy.Column(sqlalchemy.Text)
        vars = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.SpellVars", cascade="all, delete-orphan", passive_deletes=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))

def sa_bind_champion():
    global Champion
    class Champion(Champion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Champion"
        allytips = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        blurb = sqlalchemy.Column(sqlalchemy.Text)
        enemytips = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        info = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Info", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        key = sqlalchemy.Column(sqlalchemy.String(30))
        lore = sqlalchemy.Column(sqlalchemy.Text)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        partype = sqlalchemy.Column(sqlalchemy.String(30))
        passive = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Passive", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        recommended = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Recommended", cascade="all, delete-orphan", passive_deletes=True)
        skins = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Skin", cascade="all, delete-orphan", passive_deletes=True)
        spells = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.ChampionSpell", cascade="all, delete-orphan", passive_deletes=True)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Stats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        tags = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        title = sqlalchemy.Column(sqlalchemy.String(50))

def sa_bind_meta_data():
    global MetaData
    class MetaData(MetaData, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MetaData"
        isRune = sqlalchemy.Column(sqlalchemy.Boolean)
        tier = sqlalchemy.Column(sqlalchemy.String(30))
        type = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))
        _rune_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Rune.id", ondelete="CASCADE"))

def sa_bind_gold():
    global Gold
    class Gold(Gold, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Gold"
        base = sqlalchemy.Column(sqlalchemy.Integer)
        purchasable = sqlalchemy.Column(sqlalchemy.Boolean)
        sell = sqlalchemy.Column(sqlalchemy.Integer)
        total = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))

def sa_bind_basic_data_stats():
    global BasicDataStats
    class BasicDataStats(BasicDataStats, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ItemStats"
        FlatArmorMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatAttackSpeedMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatBlockMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatCritChanceMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatCritDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatEXPBonus = sqlalchemy.Column(sqlalchemy.Float)
        FlatEnergyPoolMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatEnergyRegenMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatHPPoolMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatHPRegenMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatMPPoolMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatMPRegenMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatMagicDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatMovementSpeedMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatPhysicalDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        FlatSpellBlockMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentArmorMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentAttackSpeedMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentBlockMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentCritChanceMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentCritDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentDodgeMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentEXPBonus = sqlalchemy.Column(sqlalchemy.Float)
        PercentHPPoolMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentHPRegenMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentLifeStealMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentMPPoolMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentMPRegenMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentMagicDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentMovementSpeedMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentPhysicalDamageMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentSpellBlockMod = sqlalchemy.Column(sqlalchemy.Float)
        PercentSpellVampMod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatArmorModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatArmorPenetrationMod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatArmorPenetrationModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatCritChanceModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatCritDamageModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatDodgeMod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatDodgeModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatEnergyModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatEnergyRegenModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatGoldPer10Mod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatHPModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatHPRegenModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMPModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMPRegenModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMagicDamageModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMagicPenetrationMod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMagicPenetrationModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatMovementSpeedModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatPhysicalDamageModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatSpellBlockModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rFlatTimeDeadMod = sqlalchemy.Column(sqlalchemy.Float)
        rFlatTimeDeadModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentArmorPenetrationMod = sqlalchemy.Column(sqlalchemy.Float)
        rPercentArmorPenetrationModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentAttackSpeedModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentCooldownMod = sqlalchemy.Column(sqlalchemy.Float)
        rPercentCooldownModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentMagicPenetrationMod = sqlalchemy.Column(sqlalchemy.Float)
        rPercentMagicPenetrationModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentMovementSpeedModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        rPercentTimeDeadMod = sqlalchemy.Column(sqlalchemy.Float)
        rPercentTimeDeadModPerLevel = sqlalchemy.Column(sqlalchemy.Float)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))
        _rune_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Rune.id", ondelete="CASCADE"))

def sa_bind_item():
    global Item
    class Item(Item, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Item"
        colloq = sqlalchemy.Column(sqlalchemy.String(100))
        consumeOnFull = sqlalchemy.Column(sqlalchemy.Boolean)
        consumed = sqlalchemy.Column(sqlalchemy.Boolean)
        depth = sqlalchemy.Column(sqlalchemy.Integer)
        description = sqlalchemy.Column(sqlalchemy.Text)
        from_ = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        gold = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Gold", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        group = sqlalchemy.Column(sqlalchemy.String(30))
        hideFromAll = sqlalchemy.Column(sqlalchemy.Boolean)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inStore = sqlalchemy.Column(sqlalchemy.Boolean)
        into = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        maps = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(50))
        plaintext = sqlalchemy.Column(sqlalchemy.String(100))
        requiredChampion = sqlalchemy.Column(sqlalchemy.String(30))
        rune = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.MetaData", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        specialRecipe = sqlalchemy.Column(sqlalchemy.Integer)
        stacks = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.BasicDataStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        tags = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)

def sa_bind_map_details():
    global MapDetails
    class MapDetails(MapDetails, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MapDetails"
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        mapId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        mapName = sqlalchemy.Column(sqlalchemy.String(30))
        unpurchasableItemList = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)

def sa_bind_mastery():
    global Mastery
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Mastery"
        description = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        masteryTree = sqlalchemy.Column(sqlalchemy.String(30))
        name = sqlalchemy.Column(sqlalchemy.String(50))
        prereq = sqlalchemy.Column(sqlalchemy.String(30))
        ranks = sqlalchemy.Column(sqlalchemy.Integer)
        sanitizedDescription = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)

def sa_bind_realm():
    global Realm
    class Realm(Realm, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Realm"
        cdn = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
        css = sqlalchemy.Column(sqlalchemy.String(30))
        dd = sqlalchemy.Column(sqlalchemy.String(30))
        l = sqlalchemy.Column(sqlalchemy.String(30))
        lg = sqlalchemy.Column(sqlalchemy.String(30))
        n = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        profileiconmax = sqlalchemy.Column(sqlalchemy.Integer)
        store = sqlalchemy.Column(sqlalchemy.String(30))
        v = sqlalchemy.Column(sqlalchemy.String(30))

def sa_bind_rune():
    global Rune
    class Rune(Rune, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Rune"
        colloq = sqlalchemy.Column(sqlalchemy.String(100))
        consumeOnFull = sqlalchemy.Column(sqlalchemy.Boolean)
        consumed = sqlalchemy.Column(sqlalchemy.Boolean)
        depth = sqlalchemy.Column(sqlalchemy.Integer)
        description = sqlalchemy.Column(sqlalchemy.Text)
        from_ = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        group = sqlalchemy.Column(sqlalchemy.String(30))
        hideFromAll = sqlalchemy.Column(sqlalchemy.Boolean)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        inStore = sqlalchemy.Column(sqlalchemy.Boolean)
        into = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        maps = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(100))
        plaintext = sqlalchemy.Column(sqlalchemy.String(100))
        requiredChampion = sqlalchemy.Column(sqlalchemy.String(30))
        rune = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.MetaData", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        specialRecipe = sqlalchemy.Column(sqlalchemy.Integer)
        stacks = sqlalchemy.Column(sqlalchemy.Integer)
        stats = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.BasicDataStats", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        tags = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)

def sa_bind_summoner_spell():
    global SummonerSpell
    class SummonerSpell(SummonerSpell, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "SummonerSpell"
        cooldown = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        cooldownBurn = sqlalchemy.Column(sqlalchemy.String(30))
        cost = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        costBurn = sqlalchemy.Column(sqlalchemy.String(30))
        costType = sqlalchemy.Column(sqlalchemy.String(50))
        description = sqlalchemy.Column(sqlalchemy.Text)
        effect = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        effectBurn = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        key = sqlalchemy.Column(sqlalchemy.String(30))
        leveltip = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.LevelTip", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        maxrank = sqlalchemy.Column(sqlalchemy.Integer)
        modes = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        range = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        rangeBurn = sqlalchemy.Column(sqlalchemy.String(30))
        resource = sqlalchemy.Column(sqlalchemy.String(50))
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        sanitizedTooltip = sqlalchemy.Column(sqlalchemy.Text)
        summonerLevel = sqlalchemy.Column(sqlalchemy.Integer)
        tooltip = sqlalchemy.Column(sqlalchemy.Text)
        vars = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.SpellVars", cascade="all, delete-orphan", passive_deletes=True)

def sa_bind_all():
    sa_bind_block_item()
    sa_bind_block()
    sa_bind_spell_vars()
    sa_bind_level_tip()
    sa_bind_stats()
    sa_bind_skin()
    sa_bind_recommended()
    sa_bind_image()
    sa_bind_passive()
    sa_bind_info()
    sa_bind_champion_spell()
    sa_bind_champion()
    sa_bind_meta_data()
    sa_bind_gold()
    sa_bind_basic_data_stats()
    sa_bind_item()
    sa_bind_map_details()
    sa_bind_mastery()
    sa_bind_realm()
    sa_bind_rune()
    sa_bind_summoner_spell()