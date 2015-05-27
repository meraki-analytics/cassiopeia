from cassiopeia.type.dto.common import CassiopeiaDto

######################
# Champion Endpoints #
######################

class BlockItem(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Item count
        self.count = dictionary["count"]

        # int # Item ID
        self.id = dictionary["id"]


class Block(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<BlockItem> # The items
        self.items = [BlockItem(item) if not isinstance(item, BlockItem) else item for item in dictionary["items"]]

        # boolean # RecMath
        self.recMath = dictionary["recMath"]

        # string # Type
        self.type = dictionary["type"]


class SpellVars(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<double> # Coefficients
        self.coeff = dictionary["coeff"]

        # string # Dyn
        self.dyn = dictionary["dyn"]

        # string # Key
        self.key = dictionary["key"]

        # string # Link
        self.link = dictionary["link"]

        # string # Ranks with
        self.ranksWith = dictionary["ranksWith"]


class LevelTip(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # effects
        self.effect = dictionary["effect"]

        # list<string> # labels
        self.label = dictionary["label"]


class Stats(CassiopeiaDto):
    def __init__(self, dictionary):
        # double # Armor
        self.armor = dictionary["armor"]

        # double # Armor per level 
        self.armorperlevel = dictionary["armorperlevel"]

        # double # Attack damage
        self.attackdamage = dictionary["attackdamage"]

        # double # Attack damage per level
        self.attackdamageperlevel = dictionary["attackdamageperlevel"]

        # double # Attack range
        self.attackrange = dictionary["attackrange"]

        # double # Attack speed offset
        self.attackspeedoffset = dictionary["attackspeedoffset"]

        # double # Attack speed per level
        self.attackspeedperlevel = dictionary["attackspeedperlevel"]

        # double # Crit chance
        self.crit = dictionary["crit"]

        # double # Crit change per level
        self.critperlevel = dictionary["critperlevel"]

        # double # Health
        self.hp = dictionary["hp"]

        # double # Health per level
        self.hpperlevel = dictionary["hpperlevel"]

        # double # Health regen
        self.hpregen = dictionary["hpregen"]

        # double # Health regen per level
        self.hpregenperlevel = dictionary["hpregenperlevel"]

        # double # Movespeed
        self.movespeed = dictionary["movespeed"]

        # double # Mana
        self.mp = dictionary["mp"]

        # double # Mana per level
        self.mpperlevel = dictionary["mpperlevel"]

        # double # Mana regen
        self.mpregen = dictionary["mpregen"]

        # double # Mana regen per level
        self.mpregenperlevel = dictionary["mpregenperlevel"]

        # double # Magic resist
        self.spellblock = dictionary["spellblock"]

        # double # Magic resist per level
        self.spellblockperlevel = dictionary["spellblockperlevel"]


class Skin(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # ID
        self.id = dictionary["id"]

        # string # Name
        self.name = dictionary["name"]

        # int # Number
        self.num = dictionary["num"]


class Recommended(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Block> # Blocks
        self.blocks = [Block(block) if not isinstance(block, Block) else block for block in dictionary["blocks"]]

        # string # Champion
        self.champion = dictionary["champion"]

        # string # Map
        self.map = dictionary["map"]

        # string # Mode
        self.mode = dictionary["mode"]

        # boolean # Priority
        self.priority = dictionary["priority"]

        # string # Title
        self.title = dictionary["title"]

        # string # Type
        self.type = dictionary["type"]


class Image(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Full link
        self.full = dictionary["full"]

        # string # Group
        self.group = dictionary["group"]

        # int # H
        self.h = dictionary["h"]

        # string # Sprite
        self.sprite = dictionary["sprite"]

        # int # W
        self.w = dictionary["w"]

        # int # X
        self.x = dictionary["x"]

        # int # Y
        self.y = dictionary["y"]


class Passive(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Description
        self.description = dictionary["description"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # string # Name
        self.name = dictionary["name"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]


class Info(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Attack rating
        self.attack = dictionary["attack"]

        # int # Defense rating
        self.defense = dictionary["defense"]

        # int # Difficulty rating
        self.difficulty = dictionary["difficulty"]

        # int # Magic rating
        self.magic = dictionary["magic"]


class ChampionSpell(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Image> # Alternate images
        self.altimages = [Image(image) if not isinstance(image, Image) else image for image in dictionary["altimages"]]

        # list<double> # Cooldown
        self.cooldown = dictionary["cooldown"]

        # string # Cooldown burn
        self.cooldownBurn = dictionary["cooldownBurn"]

        # List<int> # Cost
        self.cost = dictionary["cost"]

        # string # Cost burn
        self.costBurn = dictionary["costBurn"]

        # string # Cost type
        self.costType = dictionary["costType"]

        # string # Description
        self.description = dictionary["description"]

        # list<list<double>> # Effects
        self.effect = dictionary["effect"]

        # list<string> # Effect burn
        self.effectBurn = dictionary["effectBurn"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # string # Key
        self.key = dictionary["key"]

        # LevelTip # Level tip
        self.leveltip = LevelTip(dictionary["leveltip"]) if not isinstance(dictionary["leveltip"], LevelTip) else dictionary["leveltip"]

        # int # Max rank
        self.maxrank = dictionary["maxrank"]

        # string # Name
        self.name = dictionary["name"]

        # list<int> or 'self' # Range
        self.range = dictionary["range"]

        # string # Range burn
        self.rangeBurn = dictionary["rangeBurn"]

        # string # Resource
        self.resource = dictionary["resource"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]

        # string # Sanitized tooltip
        self.sanitizedTooltip = dictionary["sanitizedTooltip"]

        # string # Tooltip
        self.tooltip = dictionary["tooltip"]

        # list<SpellVars> # Vars
        self.vars = [SpellVars(svars) if not isinstance(svars, SpellVars) else svars for svars in dictionary["vars"]]


class Champion(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # Ally tips
        self.allytips = dictionary["allytips"]

        # string # Blurb
        self.blurb = dictionary["blurb"]

        # list<string> # Enemy tips
        self.enemytips = dictionary["enemytips"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # Info # Info
        self.info = Info(dictionary["info"]) if not isinstance(dictionary["info"], Info) else dictionary["info"]

        # string # Key
        self.key = dictionary["key"]

        # string # Lore
        self.lore = dictionary["lore"]

        # string # Name
        self.name = dictionary["name"]

        # string # Partype
        self.partype = dictionary["partype"]

        # Passive # Passive
        self.passive = Passive(dictionary["passive"]) if not isinstance(dictionary["passive"], Passive) else dictionary["passive"]

        # list<Recommended> # Recommended
        self.recommended = [Recommended(rec) if not isinstance(rec, Recommended) else rec for rec in dictionary["recommended"]]

        # List<Skin> # Skins
        self.skins = [Skin(skin) if not isinstance(skin, Skin) else skin for skin in dictionary["skins"]]

        # List<ChampionSpell> # Spells
        self.spells = [ChampionSpell(spell) if not isinstance(spell, ChampionSpell) else spell for spell in dictionary["spells"]]

        # Stats # Stats
        self.stats = Stats(dictionary["stats"]) if not isinstance(dictionary["stats"], Stats) else dictionary["stats"]

        # list<string> # Tags
        self.tags = dictionary["tags"]

        # string # Title
        self.title = dictionary["title"]


class ChampionList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, Champion> # Champion data
        self.data = {name: Champion(champ) if not isinstance(champ, Champion) else champ for name, champ in dictionary["data"]}

        # string # Format
        self.format = dictionary["format"]

        # dict<string, string> # Keys
        self.keys = dictionary["keys"]

        # string # Type
        self.type = dictionary["type"]

        # string # version
        self.version = dictionary["version"]

##################
# Item Endpoints #
##################

class MetaData(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Is a rune
        self.isRune = dictionary["isRune"]

        # string # Tier
        self.tier = dictionary["tier"]

        # string # Type
        self.type = dictionary["type"]


class Gold(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Base price
        self.base = dictionary["base"]

        # boolean # Is purchasable
        self.purchasable = dictionary["purchasable"]

        # int # Sell price
        self.sell = dictionary["sell"]

        # int # Total price
        self.total = dictionary["total"]


class BasicDataStats(CassiopeiaDto):
    def __init__(self, dictionary):
        # double # The FlatArmorMod
        self.FlatArmorMod = dictionary["FlatArmorMod"]

        # double # The FlatAttackSpeedMod
        self.FlatAttackSpeedMod = dictionary["FlatAttackSpeedMod"]

        # double # The FlatBlockMod
        self.FlatBlockMod = dictionary["FlatBlockMod"]

        # double # The FlatCritChanceMod
        self.FlatCritChanceMod = dictionary["FlatCritChanceMod"]

        # double # The FlatCritDamageMod
        self.FlatCritDamageMod = dictionary["FlatCritDamageMod"]

        # double # The FlatEXPBonus
        self.FlatEXPBonus = dictionary["FlatEXPBonus"]

        # double # The FlatEnergyPoolMod
        self.FlatEnergyPoolMod = dictionary["FlatEnergyPoolMod"]

        # double # The FlatEnergyRegenMod
        self.FlatEnergyRegenMod = dictionary["FlatEnergyRegenMod"]

        # double # The FlatHPPoolMod
        self.FlatHPPoolMod = dictionary["FlatHPPoolMod"]

        # double # The FlatHPRegenMod
        self.FlatHPRegenMod = dictionary["FlatHPRegenMod"]

        # double # The FlatMPPoolMod
        self.FlatMPPoolMod = dictionary["FlatMPPoolMod"]

        # double # The FlatMPRegenMod
        self.FlatMPRegenMod = dictionary["FlatMPRegenMod"]

        # double # The FlatMagicDamageMod
        self.FlatMagicDamageMod = dictionary["FlatMagicDamageMod"]

        # double # The FlatMovementSpeedMod
        self.FlatMovementSpeedMod = dictionary["FlatMovementSpeedMod"]

        # double # The FlatPhysicalDamageMod
        self.FlatPhysicalDamageMod = dictionary["FlatPhysicalDamageMod"]

        # double # The FlatSpellBlockMod
        self.FlatSpellBlockMod = dictionary["FlatSpellBlockMod"]

        # double # The PercentArmorMod
        self.PercentArmorMod = dictionary["PercentArmorMod"]

        # double # The PercentAttackSpeedMod
        self.PercentAttackSpeedMod = dictionary["PercentAttackSpeedMod"]

        # double # The PercentBlockMod
        self.PercentBlockMod = dictionary["PercentBlockMod"]

        # double # The PercentCritChanceMod
        self.PercentCritChanceMod = dictionary["PercentCritChanceMod"]

        # double # The PercentCritDamageMod
        self.PercentCritDamageMod = dictionary["PercentCritDamageMod"]

        # double # The PercentDodgeMod
        self.PercentDodgeMod = dictionary["PercentDodgeMod"]

        # double # The PercentEXPBonus
        self.PercentEXPBonus = dictionary["PercentEXPBonus"]

        # double # The PercentHPPoolMod
        self.PercentHPPoolMod = dictionary["PercentHPPoolMod"]

        # double # The PercentHPRegenMod
        self.PercentHPRegenMod = dictionary["PercentHPRegenMod"]

        # double # The PercentLifeStealMod
        self.PercentLifeStealMod = dictionary["PercentLifeStealMod"]

        # double # The PercentMPPoolMod
        self.PercentMPPoolMod = dictionary["PercentMPPoolMod"]

        # double # The PercentMPRegenMod
        self.PercentMPRegenMod = dictionary["PercentMPRegenMod"]

        # double # The PercentMagicDamageMod
        self.PercentMagicDamageMod = dictionary["PercentMagicDamageMod"]

        # double # The PercentMovementSpeedMod
        self.PercentMovementSpeedMod = dictionary["PercentMovementSpeedMod"]

        # double # The PercentPhysicalDamageMod
        self.PercentPhysicalDamageMod = dictionary["PercentPhysicalDamageMod"]

        # double # The PercentSpellBlockMod
        self.PercentSpellBlockMod = dictionary["PercentSpellBlockMod"]

        # double # The PercentSpellVampMod
        self.PercentSpellVampMod = dictionary["PercentSpellVampMod"]

        # double # The rFlatArmorModPerLevel
        self.rFlatArmorModPerLevel = dictionary["rFlatArmorModPerLevel"]

        # double # The rFlatArmorPenetrationMod
        self.rFlatArmorPenetrationMod = dictionary["rFlatArmorPenetrationMod"]

        # double # The rFlatArmorPenetrationModPerLevel
        self.rFlatArmorPenetrationModPerLevel = dictionary["rFlatArmorPenetrationModPerLevel"]

        # double # The rFlatCritChanceModPerLevel
        self.rFlatCritChanceModPerLevel = dictionary["rFlatCritChanceModPerLevel"]

        # double # The rFlatCritDamageModPerLevel
        self.rFlatCritDamageModPerLevel = dictionary["rFlatCritDamageModPerLevel"]

        # double # The rFlatDodgeMod
        self.rFlatDodgeMod = dictionary["rFlatDodgeMod"]

        # double # The rFlatDodgeModPerLevel
        self.rFlatDodgeModPerLevel = dictionary["rFlatDodgeModPerLevel"]

        # double # The rFlatEnergyModPerLevel
        self.rFlatEnergyModPerLevel = dictionary["rFlatEnergyModPerLevel"]

        # double # The rFlatEnergyRegenModPerLevel
        self.rFlatEnergyRegenModPerLevel = dictionary["rFlatEnergyRegenModPerLevel"]

        # double # The rFlatGoldPer10Mod
        self.rFlatGoldPer10Mod = dictionary["rFlatGoldPer10Mod"]

        # double # The rFlatHPModPerLevel
        self.rFlatHPModPerLevel = dictionary["rFlatHPModPerLevel"]

        # double # The rFlatHPRegenModPerLevel
        self.rFlatHPRegenModPerLevel = dictionary["rFlatHPRegenModPerLevel"]

        # double # The rFlatMPModPerLevel
        self.rFlatMPModPerLevel = dictionary["rFlatMPModPerLevel"]

        # double # The rFlatMPRegenModPerLevel
        self.rFlatMPRegenModPerLevel = dictionary["rFlatMPRegenModPerLevel"]

        # double # The rFlatMagicDamageModPerLevel
        self.rFlatMagicDamageModPerLevel = dictionary["rFlatMagicDamageModPerLevel"]

        # double # The rFlatMagicPenetrationMod
        self.rFlatMagicPenetrationMod = dictionary["rFlatMagicPenetrationMod"]

        # double # The rFlatMagicPenetrationModPerLevel
        self.rFlatMagicPenetrationModPerLevel = dictionary["rFlatMagicPenetrationModPerLevel"]

        # double # The rFlatMovementSpeedModPerLevel
        self.rFlatMovementSpeedModPerLevel = dictionary["rFlatMovementSpeedModPerLevel"]

        # double # The rFlatPhysicalDamageModPerLevel
        self.rFlatPhysicalDamageModPerLevel = dictionary["rFlatPhysicalDamageModPerLevel"]

        # double # The rFlatSpellBlockModPerLevel
        self.rFlatSpellBlockModPerLevel = dictionary["rFlatSpellBlockModPerLevel"]

        # double # The rFlatTimeDeadMod
        self.rFlatTimeDeadMod = dictionary["rFlatTimeDeadMod"]

        # double # The rFlatTimeDeadModPerLevel
        self.rFlatTimeDeadModPerLevel = dictionary["rFlatTimeDeadModPerLevel"]

        # double # The rPercentArmorPenetrationMod
        self.rPercentArmorPenetrationMod = dictionary["rPercentArmorPenetrationMod"]

        # double # The rPercentArmorPenetrationModPerLevel
        self.rPercentArmorPenetrationModPerLevel = dictionary["rPercentArmorPenetrationModPerLevel"]

        # double # The rPercentAttackSpeedModPerLevel
        self.rPercentAttackSpeedModPerLevel = dictionary["rPercentAttackSpeedModPerLevel"]

        # double # The rPercentCooldownMod
        self.rPercentCooldownMod = dictionary["rPercentCooldownMod"]

        # double # The rPercentCooldownModPerLevel
        self.rPercentCooldownModPerLevel = dictionary["rPercentCooldownModPerLevel"]

        # double # The rPercentMagicPenetrationMod
        self.rPercentMagicPenetrationMod = dictionary["rPercentMagicPenetrationMod"]

        # double # The rPercentMagicPenetrationModPerLevel
        self.rPercentMagicPenetrationModPerLevel = dictionary["rPercentMagicPenetrationModPerLevel"]

        # double # The rPercentMovementSpeedModPerLevel
        self.rPercentMovementSpeedModPerLevel = dictionary["rPercentMovementSpeedModPerLevel"]

        # double # The rPercentTimeDeadMod
        self.rPercentTimeDeadMod = dictionary["rPercentTimeDeadMod"]

        # double # The rPercentTimeDeadModPerLevel
        self.rPercentTimeDeadModPerLevel = dictionary["rPercentTimeDeadModPerLevel"]


class ItemTree(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The header
        self.header = dictionary["header"]

        # List[string] # Tags
        self.tags = dictionary["tags"]


class Item(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary["colloq"]

        # boolean # Consume on full
        self.consumeOnFull = dictionary["consumeOnFull"]

        # boolean # Consumed
        self.consumed = dictionary["consumed"]

        # int # Depth
        self.depth = dictionary["depth"]

        # string # Description
        self.description = dictionary["description"]

        # list<string> # From
        self.from_ = dictionary["from"]

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        self.gold = Gold(dictionary["gold"]) if not isinstance(dictionary["gold"], Gold) else dictionary["gold"]

        # string # Group
        self.group = dictionary["group"]

        # boolean # Hide from all
        self.hideFromAll = dictionary["hideFromAll"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # boolean # In store
        self.inStore = dictionary["inStore"]

        # list<string> # Into
        self.into = dictionary["into"]

        # map<string, boolean> # Maps
        self.maps = dictionary["maps"]

        # string # Name
        self.name = dictionary["name"]

        # string # Plain text
        self.plaintext = dictionary["plaintext"]

        # string # Required champion
        self.requiredChampion = dictionary["requiredChampion"]

        # MetaData # Rune
        self.rune = MetaData(dictionary["rune"]) if not isinstance(dictionary["rune"], MetaData) else dictionary["rune"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]

        # int # Special recipe
        self.specialRecipe = dictionary["specialRecipe"]

        # int # Stacks
        self.stacks = dictionary["stacks"]

        # BasicDataStats # Stats
        self.stats = BasicDataStats(dictionary["stats"]) if not isinstance(dictionary["stats"], BasicDataStats) else dictionary["stats"]

        # list<string> # Tags
        self.tags = dictionary["tags"]


class Group(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Max ownable of group
        self.MaxGroupOwnable = dictionary["MaxGroupOwnable"]

        # string # Key
        self.key = dictionary["key"]


class BasicData(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary["colloq"]

        # boolean # Consume on full
        self.consumeOnFull = dictionary["consumeOnFull"]

        # boolean # Consumed
        self.consumed = dictionary["consumed"]

        # int # Depth
        self.depth = dictionary["depth"]

        # string # Description
        self.description = dictionary["description"]

        # list<string> # From
        self.from_ = dictionary["from"]

        # Gold # Data Dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        self.gold = Gold(dictionary["gold"]) if not isinstance(dictionary["gold"], Gold) else dictionary["gold"]

        # string # Group
        self.group = dictionary["group"]

        # boolean # Hide from all
        self.hideFromAll = dictionary["hideFromAll"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # boolean # In store
        self.inStore = dictionary["inStore"]

        # list<string> # Into
        self.into = dictionary["into"]

        # dict<string, boolean> # Maps
        self.maps = dictionary["maps"]

        # string # Name
        self.name = dictionary["name"]

        # string # Plain text
        self.plaintext = dictionary["plaintext"]

        # string # Required champion
        self.requiredChampion = dictionary["requiredChampion"]

        # MetaData # Rune
        self.rune = MetaData(dictionary["rune"]) if not isinstance(dictionary["rune"], MetaData) else dictionary["rune"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]

        # int # Special recipe
        self.specialRecipe = dictionary["specialRecipe"]

        # int # Stacks
        self.stacks = dictionary["stacks"]

        # BasicDataStats # Stats
        self.stats = BasicDataStats(dictionary["stats"]) if not isinstance(dictionary["stats"], BasicDataStats) else dictionary["stats"]

        # List[string] # Tags
        self.tags = dictionary["tags"]


class ItemList(CassiopeiaDto):
    def __init__(self, dictionary):
    # BasicData # Basic data
    self.basic = BasicData(dictionary["basic"]) if not isinstance(dictionary["basic"], BasicData) else dictionary["basic"]

    # dict<string, Item> # Item data
    self.data = {id_: Item(item) if not isinstance(item, Item) else item for id_, item in dictionary["data"]}

    # list<Group> # Groups
    self.groups = [Group(group) if not isinstance(group, Group) else group for group in dictionary["groups"]]

    # list<ItemTree> # Item tree
    self.tree = [ItemTree(tree) if not isinstance(tree, ItemTree) else tree for tree in dictionary["tree"]]

    # string # Type
    self.type = dictionary["type"]

    # string # Version
    self.version = dictionary["version"]

######################
# Language Endpoints #
######################

class LanguageStrings(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, string> # Language string data
        self.data = dictionary["data"]

        # string # Type
        self.type = dictionary["type"]

        # string # Version
        self.version = dictionary["version"]

################
# Map Endpoint #
################

class MapDetails(CassiopeiaDto):
    def __init__(self, dictionary):
        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # long # ID
        self.mapId = dictionary["mapId"]

        # string # Name
        self.mapName = dictionary["mapName"]

        # list<long> # Items that can't be purchased on this map (IDs)
        self.unpurchasableItemList = dictionary["unpurchasableItemList"]


class MapData(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, MapDetails> # Map data
        self.data = {id_: MapDetails(map_) if not isinstance(map_, MapDetails) else map_ for id_, map_ in dictionary["data"]}

        # string # Type
        self.type = dictionary["type"]

        # string # Version
        self.version = dictionary["version"]

#####################
# Mastery Endpoints #
#####################

class MasteryTreeItem(CassiopeiaDto):
    def __init__(self, dictionary):
        # int # Mastery ID
        self.masteryId = dictionary["masteryId"]

        # string # Prerequisites
        self.prereq = dictionary["prereq"]


class MasteryTreeList(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<MasteryTreeItem> # Mastery tree items
        self.masteryTreeItems = [MasteryTreeItem(item) if not isinstance(item, MasteryTreeItem) else item for item in dictionary["masteryTreeItems"]]


class MasteryTree(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<MasteryTreeList> # Defense tree
        self.Defense = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary["Defense"]]

        # list<MasteryTreeList> # Offense tree
        self.Offense = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary["Offense"]]

        # list<MasteryTreeList> # Utility tree
        self.Utility = [MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_ for list_ in dictionary["Utility"]]


class Mastery(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<string> # Description
        self.description = dictionary["description"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # string # Legal values: Defense, Offense, Utility
        self.masteryTree = dictionary["masteryTree"]

        # string # Name
        self.name = dictionary["name"]

        # string # Prerequisites
        self.prereq = dictionary["prereq"]

        # int # Ranks
        self.ranks = dictionary["ranks"]

        # list<string> # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]


class MasteryList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, Mastery> # Mastery data
        self.data = {id_: Mastery(mastery) if not isinstance(mastery, Mastery) else mastery for id_, mastery in dictionary["data"]}

        # MasteryTree # Mastery tree
        self.tree = MasteryTree(dictionary["tree"]) if not isinstance(dictionary["tree"], MasteryTree) else dictionary["tree"]

        # string # Type
        self.type = dictionary["type"]

        # string # Version
        self.version = dictionary["version"]

##################
# Realm Endpoint #
##################

class Realm(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # The base CDN url.
        self.cdn = dictionary["cdn"]

        # string # Latest changed version of Dragon Magic's css file.
        self.css = dictionary["css"]

        # string # Latest changed version of Dragon Magic.
        self.dd = dictionary["dd"]

        # string # Default language for this realm.
        self.l = dictionary["l"]

        # string # Legacy script mode for IE6 or older.
        self.lg = dictionary["lg"]

        # dict<string, string> # Latest changed version for each data type listed.
        self.n = dictionary["n"]

        # int # Special behavior number identifying the largest profileicon id that can be used under 500. Any profileicon that is requested between this number and 500 should be mapped to 0.
        self.profileiconmax = dictionary["profileiconmax"]

        # string # Additional api data drawn from other sources that may be related to data dragon functionality.
        self.store = dictionary["store"]

        # string # Current version of this file for this realm.
        self.v = dictionary["v"]

##################
# Rune Endpoints #
##################

class Rune(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Colloq
        self.colloq = dictionary["colloq"]

        # boolean # Consume on full
        self.consumeOnFull = dictionary["consumeOnFull"]

        # boolean # Consumed
        self.consumed = dictionary["consumed"]

        # int # Depth
        self.depth = dictionary["depth"]

        # string # Description
        self.description = dictionary["description"]

        # list<string> # From
        self.from_ = dictionary["from"]

        # string # Group
        self.group = dictionary["group"]

        # boolean # Hide from all
        self.hideFromAll = dictionary["hideFromAll"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # boolean # In store
        self.inStore = dictionary["inStore"]

        # list<string> # Into
        self.into = dictionary["into"]

        # dict<string, boolean> # Maps
        self.maps = dictionary["maps"]

        # string # Name
        self.name = dictionary["name"]

        # string # Plain text
        self.plaintext = dictionary["plaintext"]

        # string # Required champion
        self.requiredChampion = dictionary["requiredChampion"]

        # MetaData # Rune
        self.rune = MetaData(dictionary["rune"]) if not isinstance(dictionary["rune"], MetaData) else dictionary["rune"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]

        # int # Special recipe
        self.specialRecipe = dictionary["specialRecipe"]

        # int # Stacks
        self.stacks = dictionary["stacks"]

        # BasicDataStats # Stats
        self.stats = BasicDataStats(dictionary["stats"]) if not isinstance(dictionary["stats"], BasicDataStats) else dictionary["stats"]

        # list<string> # Tags
        self.tags = dictionary["tags"]


class RuneList(CassiopeiaDto):
    def __init__(self, dictionary):
        # BasicData # Basic data
        self.basic = BasicData(dictionary["basic"]) if not isinstance(dictionary["basic"], BasicData) else dictionary["basic"]

        # dict<string, Rune> # Rune data
        self.data = {id_: Rune(rune) if not isinstance(rune, Rune) else rune for id_, rune in dictionary["data"]}

        # string # Type
        self.type = dictionary["type"]

        # string # Version
        self.version = dictionary["version"]

############################
# Summoner Spell Endpoints #
############################

class SummonerSpell(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<double> # Cooldown
        self.cooldown = dictionary["cooldown"]

        # string # Cooldown burn
        self.cooldownBurn = dictionary["cooldownBurn"]

        # list<int> # Cost
        self.cost = dictionary["cost"]

        # string # Cost burn
        self.costBurn = dictionary["costBurn"]

        # string # Cost type
        self.costType = dictionary["costType"]

        # string # Description
        self.description = dictionary["description"]

        # list<list<double>> # Effects
        self.effect = dictionary["effect"]

        # list<string> # Effect burn 
        self.effectBurn = dictionary["effectBurn"]

        # int # ID
        self.id = dictionary["id"]

        # Image # Image
        self.image = Image(dictionary["image"]) if not isinstance(dictionary["image"], Image) else dictionary["image"]

        # string # Key
        self.key = dictionary["key"]

        # LevelTip # Level tip
        self.leveltip = LevelTip(dictionary["leveltip"]) if not isinstance(dictionary["leveltip"], LevelTip) else dictionary["leveltip"]

        # int # Max rank
        self.maxrank = dictionary["maxrank"]

        # list<string> # Modes
        self.modes = dictionary["modes"]

        # string # Name
        self.name = dictionary["name"]

        # list<int> or 'self' # Range
        self.range = dictionary["range"]

        # string # Range burn
        self.rangeBurn = dictionary["rangeBurn"]

        # string # Resource
        self.resource = dictionary["resource"]

        # string # Sanitized description
        self.sanitizedDescription = dictionary["sanitizedDescription"]

        # string # Sanitized tooltip
        self.sanitizedTooltip = dictionary["sanitizedTooltip"]

        # int # Summoner level
        self.summonerLevel = dictionary["summonerLevel"]

        # string # Tooltip
        self.tooltip = dictionary["tooltip"]

        # list<SpellVars> # Spell vars
        self.vars = [SpellVars(svars) if not isinstance(svars, SpellVars) else svars for svars in dictionary["vars"]]


class SummonerSpellList(CassiopeiaDto):
    def __init__(self, dictionary):
        # dict<string, SummonerSpell> # Summoner spell data
        self.data = {id_: SummonerSpell(spell) if not isinstance(spell, SummonerSpell) else spell for id_, spell in dictionary["data"]}

        # string # Type
        self.type = dictionary["type"]

        # string # Version
        self.version = dictionary["version"]