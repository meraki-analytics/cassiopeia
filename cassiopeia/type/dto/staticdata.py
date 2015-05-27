from cassiopeia.type.dto.common import CassiopeiaDto

######################
# Champion Endpoints #
######################

class BlockItem(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Item count
        self.count = dictionary.get("count",0)

        # int # Item ID
        self.id = dictionary.get("id",0)


class Block(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<BlockItem> # The items
        self.items = [BlockItem(item) if not isinstance(item, BlockItem) else item for item in dictionary.get("items",[])]

        # boolean # RecMath
        self.recMath = dictionary.get("recMath",False)

        # string # Type
        self.type = dictionary.get("type",'')


class SpellVars(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<double> # Coefficients
        self.coeff = dictionary.get("coeff",[])

        # string # Dyn
        self.dyn = dictionary.get("dyn",'')

        # string # Key
        self.key = dictionary.get("key",'')

        # string # Link
        self.link = dictionary.get("link",'')

        # string # Ranks with
        self.ranksWith = dictionary.get("ranksWith",'')


class LevelTip(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # effects
        self.effect = dictionary.get("effect",[])

        # list<string> # labels
        self.label = dictionary.get("label",[])


class Stats(CassiopeiaDto):
    def __init__(self, dictionary):
        # double # Armor
        self.armor = dictionary.get("armor",0.)

        # double # Armor per level 
        self.armorperlevel = dictionary.get("armorperlevel",0.)

        # double # Attack damage
        self.attackdamage = dictionary.get("attackdamage",0.)

        # double # Attack damage per level
        self.attackdamageperlevel = dictionary.get("attackdamageperlevel",0.)

        # double # Attack range
        self.attackrange = dictionary.get("attackrange",0.)

        # double # Attack speed offset
        self.attackspeedoffset = dictionary.get("attackspeedoffset",0.)

        # double # Attack speed per level
        self.attackspeedperlevel = dictionary.get("attackspeedperlevel",0.)

        # double # Crit chance
        self.crit = dictionary.get("crit",0.)

        # double # Crit change per level
        self.critperlevel = dictionary.get("critperlevel",0.)

        # double # Health
        self.hp = dictionary.get("hp",0.)

        # double # Health per level
        self.hpperlevel = dictionary.get("hpperlevel",0.)

        # double # Health regen
        self.hpregen = dictionary.get("hpregen",0.)

        # double # Health regen per level
        self.hpregenperlevel = dictionary.get("hpregenperlevel",0.)

        # double # Movespeed
        self.movespeed = dictionary.get("movespeed",0.)

        # double # Mana
        self.mp = dictionary.get("mp",0.)

        # double # Mana per level
        self.mpperlevel = dictionary.get("mpperlevel",0.)

        # double # Mana regen
        self.mpregen = dictionary.get("mpregen",0.)

        # double # Mana regen per level
        self.mpregenperlevel = dictionary.get("mpregenperlevel",0.)

        # double # Magic resist
        self.spellblock = dictionary.get("spellblock",0.)

        # double # Magic resist per level
        self.spellblockperlevel = dictionary.get("spellblockperlevel",0.)


class Skin(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # ID
        self.id = dictionary.get("id",0)

        # string # Name
        self.name = dictionary.get("name",'')

        # int # Number
        self.num = dictionary.get("num",0)


class Recommended(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Block> # Blocks
        self.blocks = [Block(block) if not isinstance(block, Block) else block for block in dictionary.get("blocks",[])]

        # string # Champion
        self.champion = dictionary.get("champion",'')

        # string # Map
        self.map = dictionary.get("map",'')

        # string # Mode
        self.mode = dictionary.get("mode",'')

        # boolean # Priority
        self.priority = dictionary.get("priority",False)

        # string # Title
        self.title = dictionary.get("title",'')

        # string # Type
        self.type = dictionary.get("type",'')


class Image(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Full link
        self.full = dictionary.get("full",'')

        # string # Group
        self.group = dictionary.get("group",'')

        # int # H
        self.h = dictionary.get("h",0)

        # string # Sprite
        self.sprite = dictionary.get("sprite",'')

        # int # W
        self.w = dictionary.get("w",0)

        # int # X
        self.x = dictionary.get("x",0)

        # int # Y
        self.y = dictionary.get("y",0)


class Passive(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Description
        self.description = dictionary.get("description",'')

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')


class Info(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Attack rating
        self.attack = dictionary.get("attack",0)

        # int # Defense rating
        self.defense = dictionary.get("defense",0)

        # int # Difficulty rating
        self.difficulty = dictionary.get("difficulty",0)

        # int # Magic rating
        self.magic = dictionary.get("magic",0)


class ChampionSpell(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Image> # Alternate images
        val = dictionary.get("altimages", None)
        self.altimages = Image(val) if val and not isinstance(val, Image) else val

        # list<double> # Cooldown
        self.cooldown = dictionary.get("cooldown",[])

        # string # Cooldown burn
        self.cooldownBurn = dictionary.get("cooldownBurn",'')

        # list<int> # Cost
        self.cost = dictionary.get("cost",[])

        # string # Cost burn
        self.costBurn = dictionary.get("costBurn",'')

        # string # Cost type
        self.costType = dictionary.get("costType",'')

        # string # Description
        self.description = dictionary.get("description",'')

        # list<list<double>> # Effects
        self.effect = dictionary.get("effect",[])

        # list<string> # Effect burn
        self.effectBurn = dictionary.get("effectBurn",[])

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # string # Key
        self.key = dictionary.get("key",'')

        # LevelTip # Level tip
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val

        # int # Max rank
        self.maxrank = dictionary.get("maxrank",0)

        # string # Name
        self.name = dictionary.get("name",'')

        # list<int> or 'self' # Range
        self.range = dictionary.get("range",[])

        # string # Range burn
        self.rangeBurn = dictionary.get("rangeBurn",'')

        # string # Resource
        self.resource = dictionary.get("resource",'')

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')

        # string # Sanitized tooltip
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip",'')

        # string # Tooltip
        self.tooltip = dictionary.get("tooltip",'')

        # list<SpellVars> # Vars
        self.vars = [SpellVars(svars) if not isinstance(svars, SpellVars) else svars for svars in dictionary.get("vars",[])]


class Champion(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # Ally tips
        self.allytips = dictionary.get("allytips",[])

        # string # Blurb
        self.blurb = dictionary.get("blurb",'')

        # list<string> # Enemy tips
        self.enemytips = dictionary.get("enemytips",[])

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # Info # Info
        val = dictionary.get("info", None)
        self.info = Info(val) if val and not isinstance(val, Info) else val

        # string # Key
        self.key = dictionary.get("key",'')

        # string # Lore
        self.lore = dictionary.get("lore",'')

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Partype
        self.partype = dictionary.get("partype",'')

        # Passive # Passive
        val = dictionary.get("passive", None)
        self.passive = Passive(val) if val and not isinstance(val, Passive) else val

        # list<Recommended> # Recommended
        self.recommended = [Recommended(rec) if not isinstance(rec, Recommended) else rec for rec in dictionary.get("recommended",[])]

        # list<Skin> # Skins
        self.skins = [Skin(skin) if val and not isinstance(skin, Skin) else skin for skin in dictionary.get("skins",[])]

        # list<ChampionSpell> # Spells
        self.spells = [ChampionSpell(spell) if not isinstance(spell, ChampionSpell) else spell for spell in dictionary.get("spells",[])]

        # Stats # Stats
        val = dictionary.get("stats", None)
        self.stats = Stats(val) if val and not isinstance(val, Stats) else val

        # list<string> # Tags
        self.tags = dictionary.get("tags",[])

        # string # Title
        self.title = dictionary.get("title",'')


class ChampionList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, Champion> # Champion data
        self.data = {name: Champion(champ) if not isinstance(champ, Champion) else champ for name, champ in dictionary.get("data",{})}

        # string # Format
        self.format = dictionary.get("format",'')

        # dict<string, string> # Keys
        self.keys = dictionary.get("keys",{})

        # string # Type
        self.type = dictionary.get("type",'')

        # string # version
        self.version = dictionary.get("version",'')

##################
# Item Endpoints #
##################

class MetaData(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Is a rune
        self.isRune = dictionary.get("isRune",False)

        # string # Tier
        self.tier = dictionary.get("tier",'')

        # string # Type
        self.type = dictionary.get("type",'')


class Gold(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Base price
        self.base = dictionary.get("base",0)

        # boolean # Is purchasable
        self.purchasable = dictionary.get("purchasable",False)

        # int # Sell price
        self.sell = dictionary.get("sell",0)

        # int # Total price
        self.total = dictionary.get("total",0)


class BasicDataStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # double # The FlatArmorMod
        self.FlatArmorMod = dictionary.get("FlatArmorMod",0.)

        # double # The FlatAttackSpeedMod
        self.FlatAttackSpeedMod = dictionary.get("FlatAttackSpeedMod",0.)

        # double # The FlatBlockMod
        self.FlatBlockMod = dictionary.get("FlatBlockMod",0.)

        # double # The FlatCritChanceMod
        self.FlatCritChanceMod = dictionary.get("FlatCritChanceMod",0.)

        # double # The FlatCritDamageMod
        self.FlatCritDamageMod = dictionary.get("FlatCritDamageMod",0.)

        # double # The FlatEXPBonus
        self.FlatEXPBonus = dictionary.get("FlatEXPBonus",0.)

        # double # The FlatEnergyPoolMod
        self.FlatEnergyPoolMod = dictionary.get("FlatEnergyPoolMod",0.)

        # double # The FlatEnergyRegenMod
        self.FlatEnergyRegenMod = dictionary.get("FlatEnergyRegenMod",0.)

        # double # The FlatHPPoolMod
        self.FlatHPPoolMod = dictionary.get("FlatHPPoolMod",0.)

        # double # The FlatHPRegenMod
        self.FlatHPRegenMod = dictionary.get("FlatHPRegenMod",0.)

        # double # The FlatMPPoolMod
        self.FlatMPPoolMod = dictionary.get("FlatMPPoolMod",0.)

        # double # The FlatMPRegenMod
        self.FlatMPRegenMod = dictionary.get("FlatMPRegenMod",0.)

        # double # The FlatMagicDamageMod
        self.FlatMagicDamageMod = dictionary.get("FlatMagicDamageMod",0.)

        # double # The FlatMovementSpeedMod
        self.FlatMovementSpeedMod = dictionary.get("FlatMovementSpeedMod",0.)

        # double # The FlatPhysicalDamageMod
        self.FlatPhysicalDamageMod = dictionary.get("FlatPhysicalDamageMod",0.)

        # double # The FlatSpellBlockMod
        self.FlatSpellBlockMod = dictionary.get("FlatSpellBlockMod",0.)

        # double # The PercentArmorMod
        self.PercentArmorMod = dictionary.get("PercentArmorMod",0.)

        # double # The PercentAttackSpeedMod
        self.PercentAttackSpeedMod = dictionary.get("PercentAttackSpeedMod",0.)

        # double # The PercentBlockMod
        self.PercentBlockMod = dictionary.get("PercentBlockMod",0.)

        # double # The PercentCritChanceMod
        self.PercentCritChanceMod = dictionary.get("PercentCritChanceMod",0.)

        # double # The PercentCritDamageMod
        self.PercentCritDamageMod = dictionary.get("PercentCritDamageMod",0.)

        # double # The PercentDodgeMod
        self.PercentDodgeMod = dictionary.get("PercentDodgeMod",0.)

        # double # The PercentEXPBonus
        self.PercentEXPBonus = dictionary.get("PercentEXPBonus",0.)

        # double # The PercentHPPoolMod
        self.PercentHPPoolMod = dictionary.get("PercentHPPoolMod",0.)

        # double # The PercentHPRegenMod
        self.PercentHPRegenMod = dictionary.get("PercentHPRegenMod",0.)

        # double # The PercentLifeStealMod
        self.PercentLifeStealMod = dictionary.get("PercentLifeStealMod",0.)

        # double # The PercentMPPoolMod
        self.PercentMPPoolMod = dictionary.get("PercentMPPoolMod",0.)

        # double # The PercentMPRegenMod
        self.PercentMPRegenMod = dictionary.get("PercentMPRegenMod",0.)

        # double # The PercentMagicDamageMod
        self.PercentMagicDamageMod = dictionary.get("PercentMagicDamageMod",0.)

        # double # The PercentMovementSpeedMod
        self.PercentMovementSpeedMod = dictionary.get("PercentMovementSpeedMod",0.)

        # double # The PercentPhysicalDamageMod
        self.PercentPhysicalDamageMod = dictionary.get("PercentPhysicalDamageMod",0.)

        # double # The PercentSpellBlockMod
        self.PercentSpellBlockMod = dictionary.get("PercentSpellBlockMod",0.)

        # double # The PercentSpellVampMod
        self.PercentSpellVampMod = dictionary.get("PercentSpellVampMod",0.)

        # double # The rFlatArmorModPerLevel
        self.rFlatArmorModPerLevel = dictionary.get("rFlatArmorModPerLevel",0.)

        # double # The rFlatArmorPenetrationMod
        self.rFlatArmorPenetrationMod = dictionary.get("rFlatArmorPenetrationMod",0.)

        # double # The rFlatArmorPenetrationModPerLevel
        self.rFlatArmorPenetrationModPerLevel = dictionary.get("rFlatArmorPenetrationModPerLevel",0.)

        # double # The rFlatCritChanceModPerLevel
        self.rFlatCritChanceModPerLevel = dictionary.get("rFlatCritChanceModPerLevel",0.)

        # double # The rFlatCritDamageModPerLevel
        self.rFlatCritDamageModPerLevel = dictionary.get("rFlatCritDamageModPerLevel",0.)

        # double # The rFlatDodgeMod
        self.rFlatDodgeMod = dictionary.get("rFlatDodgeMod",0.)

        # double # The rFlatDodgeModPerLevel
        self.rFlatDodgeModPerLevel = dictionary.get("rFlatDodgeModPerLevel",0.)

        # double # The rFlatEnergyModPerLevel
        self.rFlatEnergyModPerLevel = dictionary.get("rFlatEnergyModPerLevel",0.)

        # double # The rFlatEnergyRegenModPerLevel
        self.rFlatEnergyRegenModPerLevel = dictionary.get("rFlatEnergyRegenModPerLevel",0.)

        # double # The rFlatGoldPer10Mod
        self.rFlatGoldPer10Mod = dictionary.get("rFlatGoldPer10Mod",0.)

        # double # The rFlatHPModPerLevel
        self.rFlatHPModPerLevel = dictionary.get("rFlatHPModPerLevel",0.)

        # double # The rFlatHPRegenModPerLevel
        self.rFlatHPRegenModPerLevel = dictionary.get("rFlatHPRegenModPerLevel",0.)

        # double # The rFlatMPModPerLevel
        self.rFlatMPModPerLevel = dictionary.get("rFlatMPModPerLevel",0.)

        # double # The rFlatMPRegenModPerLevel
        self.rFlatMPRegenModPerLevel = dictionary.get("rFlatMPRegenModPerLevel",0.)

        # double # The rFlatMagicDamageModPerLevel
        self.rFlatMagicDamageModPerLevel = dictionary.get("rFlatMagicDamageModPerLevel",0.)

        # double # The rFlatMagicPenetrationMod
        self.rFlatMagicPenetrationMod = dictionary.get("rFlatMagicPenetrationMod",0.)

        # double # The rFlatMagicPenetrationModPerLevel
        self.rFlatMagicPenetrationModPerLevel = dictionary.get("rFlatMagicPenetrationModPerLevel",0.)

        # double # The rFlatMovementSpeedModPerLevel
        self.rFlatMovementSpeedModPerLevel = dictionary.get("rFlatMovementSpeedModPerLevel",0.)

        # double # The rFlatPhysicalDamageModPerLevel
        self.rFlatPhysicalDamageModPerLevel = dictionary.get("rFlatPhysicalDamageModPerLevel",0.)

        # double # The rFlatSpellBlockModPerLevel
        self.rFlatSpellBlockModPerLevel = dictionary.get("rFlatSpellBlockModPerLevel",0.)

        # double # The rFlatTimeDeadMod
        self.rFlatTimeDeadMod = dictionary.get("rFlatTimeDeadMod",0.)

        # double # The rFlatTimeDeadModPerLevel
        self.rFlatTimeDeadModPerLevel = dictionary.get("rFlatTimeDeadModPerLevel",0.)

        # double # The rPercentArmorPenetrationMod
        self.rPercentArmorPenetrationMod = dictionary.get("rPercentArmorPenetrationMod",0.)

        # double # The rPercentArmorPenetrationModPerLevel
        self.rPercentArmorPenetrationModPerLevel = dictionary.get("rPercentArmorPenetrationModPerLevel",0.)

        # double # The rPercentAttackSpeedModPerLevel
        self.rPercentAttackSpeedModPerLevel = dictionary.get("rPercentAttackSpeedModPerLevel",0.)

        # double # The rPercentCooldownMod
        self.rPercentCooldownMod = dictionary.get("rPercentCooldownMod",0.)

        # double # The rPercentCooldownModPerLevel
        self.rPercentCooldownModPerLevel = dictionary.get("rPercentCooldownModPerLevel",0.)

        # double # The rPercentMagicPenetrationMod
        self.rPercentMagicPenetrationMod = dictionary.get("rPercentMagicPenetrationMod",0.)

        # double # The rPercentMagicPenetrationModPerLevel
        self.rPercentMagicPenetrationModPerLevel = dictionary.get("rPercentMagicPenetrationModPerLevel",0.)

        # double # The rPercentMovementSpeedModPerLevel
        self.rPercentMovementSpeedModPerLevel = dictionary.get("rPercentMovementSpeedModPerLevel",0.)

        # double # The rPercentTimeDeadMod
        self.rPercentTimeDeadMod = dictionary.get("rPercentTimeDeadMod",0.)

        # double # The rPercentTimeDeadModPerLevel
        self.rPercentTimeDeadModPerLevel = dictionary.get("rPercentTimeDeadModPerLevel",0.)


class ItemTree(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The header
        self.header = dictionary.get("header",'')

        # list[string] # Tags
        self.tags = dictionary.get("tags",[])


class Item(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary.get("colloq",'')

        # boolean # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull",False)

        # boolean # Consumed
        self.consumed = dictionary.get("consumed",False)

        # int # Depth
        self.depth = dictionary.get("depth",0)

        # string # Description
        self.description = dictionary.get("description",'')

        # list<string> # From
        self.from_ = dictionary.get("from",[])

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val

        # string # Group
        self.group = dictionary.get("group",'')

        # boolean # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll",False)

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # boolean # In store
        self.inStore = dictionary.get("inStore",False)

        # list<string> # into
        self.into = dictionary.get("into",0)

        # dict<string, boolean> # Maps
        self.maps = dictionary.get("maps",{})

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Plain text
        self.plaintext = dictionary.get("plaintext",'')

        # string # Required champion
        self.requiredChampion = dictionary.get("requiredChampion",'')

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe",0)

        # int # Stacks
        self.stacks = dictionary.get("stacks",0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val

        # list<string> # Tags
        self.tags = dictionary.get("tags",[])


class Group(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Max ownable of group
        self.MaxGroupOwnable = dictionary.get("MaxGroupOwnable",'')

        # string # Key
        self.key = dictionary.get("key",'')


class BasicData(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary.get("colloq",'')

        # boolean # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull",False)

        # boolean # Consumed
        self.consumed = dictionary.get("consumed",False)

        # int # Depth
        self.depth = dictionary.get("depth",0)

        # string # Description
        self.description = dictionary.get("description",'')

        # list<string> # From
        self.from_ = dictionary.get("from",[])

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val

        # string # Group
        self.group = dictionary.get("group",'')

        # boolean # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll",False)

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # boolean # In store
        self.inStore = dictionary.get("inStore",False)

        # list<string> # into
        self.into = dictionary.get("into",0)

        # dict<string, boolean> # Maps
        self.maps = dictionary.get("maps",{})

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Plain text
        self.plaintext = dictionary.get("plaintext",'')

        # string # Required champion
        self.requiredChampion = dictionary.get("requiredChampion",'')

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe",0)

        # int # Stacks
        self.stacks = dictionary.get("stacks",0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val

        # list[string] # Tags
        self.tags = dictionary.get("tags",[])


class ItemList(CassiopeiaDto):
    def __init__(self, dictionary):
    # BasicData # Basic data
    val = dictionary.get("basic", None)
    self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val

    # dict<string, Item> # Item data
    self.data = {id_: Item(item) if not isinstance(item, Item) else item for id_, item in dictionary.get("data",{})}

    # list<Group> # Groups
    self.groups = [Group(group) if not isinstance(group, Group) else group for group in dictionary.get("groups",[])]

    # list<ItemTree> # Item tree
    self.tree = [ItemTree(tree) if not isinstance(tree, ItemTree) else tree for tree in dictionary.get("tree",[])]

    # string # Type
    self.type = dictionary.get("type",'')

    # string # Version
    self.version = dictionary.get("version",'')

######################
# Language Endpoints #
######################

class LanguageStrings(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, string> # Language string data
        self.data = dictionary.get("data",{})

        # string # Type
        self.type = dictionary.get("type",'')

        # string # Version
        self.version = dictionary.get("version",'')

################
# Map Endpoint #
################

class MapDetails(CassiopeiaDto):
    def __init__(self, dictionary):
        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # long # ID
        self.mapId = dictionary.get("mapId",0)

        # string # Name
        self.mapName = dictionary.get("mapName",'')

        # list<long> # Items that can't be purchased on this map (IDs)
        self.unpurchasableItemList = dictionary.get("unpurchasableItemList",[])


class MapData(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, MapDetails> # Map data
        self.data = {id_: MapDetails(map_) if not isinstance(map_, MapDetails) else map_ for id_, map_ in dictionary.get("data",{})}

        # string # Type
        self.type = dictionary.get("type",'')

        # string # Version
        self.version = dictionary.get("version",'')

#####################
# Mastery Endpoints #
#####################

class MasteryTreeItem(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Mastery ID
        self.masteryId = dictionary.get("masteryId",0)

        # string # Prerequisites
        self.prereq = dictionary.get("prereq",'')


class MasteryTreeList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<MasteryTreeItem> # Mastery tree items
        self.masteryTreeItems = [MasteryTreeItem(item) if not isinstance(item, MasteryTreeItem) else item for item in dictionary.get("masteryTreeItems",[])]


class MasteryTree(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<MasteryTreeList> # Defense tree
        self.Defense = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary.get("Defense",[])]

        # list<MasteryTreeList> # Offense tree
        self.Offense = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary.get("Offense",[])]

        # list<MasteryTreeList> # Utility tree
        self.Utility = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary.get("Utility",[])]


class Mastery(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # Description
        self.description = dictionary.get("description",[])

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # string # Legal values: Defense, Offense, Utility
        self.masteryTree = dictionary.get("masteryTree",'')

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Prerequisites
        self.prereq = dictionary.get("prereq",'')

        # int # Ranks
        self.ranks = dictionary.get("ranks",0)

        # list<string> # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",[])


class MasteryList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, Mastery> # Mastery data
        self.data = {id_: Mastery(mastery) if not isinstance(mastery, Mastery) else mastery for id_, mastery in dictionary.get("data",{})}

        # MasteryTree # Mastery tree
        val = dictionary.get("tree", None)
        self.tree = MasteryTree(val) if val and not isinstance(val, MasteryTree) else val

        # string # Type
        self.type = dictionary.get("type",'')

        # string # Version
        self.version = dictionary.get("version",'')

##################
# Realm Endpoint #
##################

class Realm(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The base CDN url.
        self.cdn = dictionary.get("cdn",'')

        # string # Latest changed version of Dragon Magic's css file.
        self.css = dictionary.get("css",'')

        # string # Latest changed version of Dragon Magic.
        self.dd = dictionary.get("dd",'')

        # string # Default language for this realm.
        self.l = dictionary.get("l",'')

        # string # Legacy script mode for IE6 or older.
        self.lg = dictionary.get("lg",'')

        # dict<string, string> # Latest changed version for each data type listed.
        self.n = dictionary.get("n",{})

        # int # Special behavior number identifying the largest profileicon id that can be used under 500. Any profileicon that is requested between this number and 500 should be mapped to 0.
        self.profileiconmax = dictionary.get("profileiconmax",0)

        # string # Additional api data drawn from other sources that may be related to data dragon functionality.
        self.store = dictionary.get("store",'')

        # string # Current version of this file for this realm.
        self.v = dictionary.get("v",'')

##################
# Rune Endpoints #
##################

class Rune(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary.get("colloq",'')

        # boolean # Consume on full
        self.consumeOnFull = dictionary.get("consumeOnFull",False)

        # boolean # Consumed
        self.consumed = dictionary.get("consumed",False)

        # int # Depth
        self.depth = dictionary.get("depth",0)

        # string # Description
        self.description = dictionary.get("description",'')

        # list<string> # From
        self.from_ = dictionary.get("from",[])

        # string # Group
        self.group = dictionary.get("group",'')

        # boolean # Hide from all
        self.hideFromAll = dictionary.get("hideFromAll",False)

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # boolean # In store
        self.inStore = dictionary.get("inStore",False)

        # list<string> # into
        self.into = dictionary.get("into",0)

        # dict<string, boolean> # Maps
        self.maps = dictionary.get("maps",{})

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Plain text
        self.plaintext = dictionary.get("plaintext",'')

        # string # Required champion
        self.requiredChampion = dictionary.get("requiredChampion",'')

        # MetaData # Rune
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')

        # int # Special recipe
        self.specialRecipe = dictionary.get("specialRecipe",0)

        # int # Stacks
        self.stacks = dictionary.get("stacks",0)

        # BasicDataStats # Stats
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val

        # list<string> # Tags
        self.tags = dictionary.get("tags",[])


class RuneList(CassiopeiaDto):
    def __init__(self, dictionary):
        # BasicData # Basic data
        val = dictionary.get("basic", None)
        self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val

        # dict<string, Rune> # Rune data
        self.data = {id_: Rune(rune) if not isinstance(rune, Rune) else rune for id_, rune in dictionary.get("data",{})}

        # string # Type
        self.type = dictionary.get("type",'')

        # string # Version
        self.version = dictionary.get("version",'')

############################
# Summoner Spell Endpoints #
############################

class SummonerSpell(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<double> # Cooldown
        self.cooldown = dictionary.get("cooldown",[])

        # string # Cooldown burn
        self.cooldownBurn = dictionary.get("cooldownBurn",'')

        # list<int> # Cost
        self.cost = dictionary.get("cost",[])

        # string # Cost burn
        self.costBurn = dictionary.get("costBurn",'')

        # string # Cost type
        self.costType = dictionary.get("costType",'')

        # string # Description
        self.description = dictionary.get("description",'')

        # list<list<double>> # Effects
        self.effect = dictionary.get("effect",[])

        # list<string> # Effect burn 
        self.effectBurn = dictionary.get("effectBurn",[])

        # int # ID
        self.id = dictionary.get("id",0)

        # Image # Image
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val

        # string # Key
        self.key = dictionary.get("key",'')

        # LevelTip # Level tip
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val

        # int # Max rank
        self.maxrank = dictionary.get("maxrank",0)

        # list<string> # Modes
        self.modes = dictionary.get("modes",[])

        # string # Name
        self.name = dictionary.get("name",'')

        # list<int> or 'self' # Range
        self.range = dictionary.get("range",[])

        # string # Range burn
        self.rangeBurn = dictionary.get("rangeBurn",'')

        # string # Resource
        self.resource = dictionary.get("resource",'')

        # string # Sanitized description
        self.sanitizedDescription = dictionary.get("sanitizedDescription",'')

        # string # Sanitized tooltip
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip",'')

        # int # Summoner level
        self.summonerLevel = dictionary.get("summonerLevel",0)

        # string # Tooltip
        self.tooltip = dictionary.get("tooltip",'')

        # list<SpellVars> # Spell vars
        self.vars = [SpellVars(svars) if not isinstance(svars, SpellVars) else svars for svars in dictionary.get("vars",[])]


class SummonerSpellList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, SummonerSpell> # Summoner spell data
        self.data = {id_: SummonerSpell(spell) if not isinstance(spell, SummonerSpell) else spell for id_, spell in dictionary.get("data",{})}

        # string # Type
        self.type = dictionary.get("type",'')

        # string # Version
        self.version = dictionary.get("version",'')