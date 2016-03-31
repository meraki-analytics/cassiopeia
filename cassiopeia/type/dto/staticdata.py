import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


######################
# Champion Endpoints #
######################
@cassiopeia.type.core.common.inheritdocs
class BlockItem(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        count (int): item count
        id (int): item ID
    """

    def __init__(self, dictionary):
        self.count = dictionary.get("count", 0)
        self.id = dictionary.get("id", 0)


@cassiopeia.type.core.common.inheritdocs
class Block(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        items (list<BlockItem>): the items
        recMath (bool): rec math
        type (str): type
    """

    def __init__(self, dictionary):
        self.items = [(BlockItem(item) if not isinstance(item, BlockItem) else item) for item in dictionary.get("items", []) if item]
        self.recMath = dictionary.get("recMath", False)
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class SpellVars(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        coeff (list<float>): coefficients
        dyn (str): dyn
        key (str): key
        link (str): link
        ranksWith (str): ranks with
    """

    def __init__(self, dictionary):
        self.coeff = dictionary.get("coeff", [])
        self.dyn = dictionary.get("dyn", "")
        self.key = dictionary.get("key", "")
        self.link = dictionary.get("link", "")
        self.ranksWith = dictionary.get("ranksWith", "")


@cassiopeia.type.core.common.inheritdocs
class LevelTip(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        effect (list<str>): effects
        label (list<str>): labels
    """

    def __init__(self, dictionary):
        self.effect = dictionary.get("effect", [])
        self.label = dictionary.get("label", [])


@cassiopeia.type.core.common.inheritdocs
class Stats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        armor (float): armor
        armorperlevel (float): armor per level
        attackdamage (float): attack damage
        attackdamageperlevel (float): attack damage per level
        attackrange (float): attack range
        attackspeedoffset (float): attack speed offset
        attackspeedperlevel (float): attack speed per level
        crit (float): crit chance
        critperlevel (float): crit change per level
        hp (float): health
        hpperlevel (float): health per level
        hpregen (float): health regen
        hpregenperlevel (float): health regen per level
        movespeed (float): movespeed
        mp (float): mana
        mpperlevel (float): mana per level
        mpregen (float): mana regen
        mpregenperlevel (float): mana regen per level
        spellblock (float): magic resist
        spellblockperlevel (float): magic resist per level
    """

    def __init__(self, dictionary):
        self.armor = dictionary.get("armor", 0.0)
        self.armorperlevel = dictionary.get("armorperlevel", 0.0)
        self.attackdamage = dictionary.get("attackdamage", 0.0)
        self.attackdamageperlevel = dictionary.get("attackdamageperlevel", 0.0)
        self.attackrange = dictionary.get("attackrange", 0.0)
        self.attackspeedoffset = dictionary.get("attackspeedoffset", 0.0)
        self.attackspeedperlevel = dictionary.get("attackspeedperlevel", 0.0)
        self.crit = dictionary.get("crit", 0.0)
        self.critperlevel = dictionary.get("critperlevel", 0.0)
        self.hp = dictionary.get("hp", 0.0)
        self.hpperlevel = dictionary.get("hpperlevel", 0.0)
        self.hpregen = dictionary.get("hpregen", 0.0)
        self.hpregenperlevel = dictionary.get("hpregenperlevel", 0.0)
        self.movespeed = dictionary.get("movespeed", 0.0)
        self.mp = dictionary.get("mp", 0.0)
        self.mpperlevel = dictionary.get("mpperlevel", 0.0)
        self.mpregen = dictionary.get("mpregen", 0.0)
        self.mpregenperlevel = dictionary.get("mpregenperlevel", 0.0)
        self.spellblock = dictionary.get("spellblock", 0.0)
        self.spellblockperlevel = dictionary.get("spellblockperlevel", 0.0)


@cassiopeia.type.core.common.inheritdocs
class Skin(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        id (int): ID
        name (str): name
        num (int): number
    """

    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.num = dictionary.get("num", 0)


@cassiopeia.type.core.common.inheritdocs
class Recommended(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        blocks (list<Block>): blocks
        champion (str): champion
        map (str): map
        mode (str): mode
        priority (bool): priority
        title (str): title
        type (str): type
    """

    def __init__(self, dictionary):
        self.blocks = [(Block(block) if not isinstance(block, Block) else block) for block in dictionary.get("blocks", []) if block]
        self.champion = dictionary.get("champion", "")
        self.map = dictionary.get("map", "")
        self.mode = dictionary.get("mode", "")
        self.priority = dictionary.get("priority", False)
        self.title = dictionary.get("title", "")
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class Image(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        full (str): full link
        group (str): group
        h (int): h
        sprite (str): sprite
        w (int): w
        x (int): x
        y (int): y
    """

    def __init__(self, dictionary, is_alt=False):
        self.full = dictionary.get("full", "")
        self.group = dictionary.get("group", "")
        self.h = dictionary.get("h", 0)
        self.sprite = dictionary.get("sprite", "")
        self.w = dictionary.get("w", 0)
        self.x = dictionary.get("x", 0)
        self.y = dictionary.get("y", 0)
        self._is_alt = is_alt


@cassiopeia.type.core.common.inheritdocs
class Passive(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        description (str): description
        image (Image): image
        name (str): name
        sanitizedDescription (str): sanitized description
    """

    def __init__(self, dictionary):
        self.description = dictionary.get("description", "")
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.name = dictionary.get("name", "")
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")


@cassiopeia.type.core.common.inheritdocs
class Info(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        attack (int): attack rating
        defense (int): defense rating
        difficulty (int): difficulty rating
        magic (int): magic rating
    """

    def __init__(self, dictionary):
        self.attack = dictionary.get("attack", 0)
        self.defense = dictionary.get("defense", 0)
        self.difficulty = dictionary.get("difficulty", 0)
        self.magic = dictionary.get("magic", 0)


@cassiopeia.type.core.common.inheritdocs
class ChampionSpell(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        altimages (list<Image>): alternate images
        cooldown (list<float>): cooldown
        cooldownBurn (str): cooldown burn
        cost (list<int>): cost
        costBurn (str): cost burn
        costType (str): cost type
        description (str): description
        effect (list<list<float>>): effects
        effectBurn (list<str>): effect burn
        image (Image): image
        key (str): key
        leveltip (LevelTip): level tip
        maxrank (int): max rank
        name (str): name
        range (list<int> or "self"): range
        rangeBurn (str): range burn
        resource (str): resource
        sanitizedDescription (str): sanitized description
        sanitizedTooltip (str): sanitized tooltip
        tooltip (str): tooltip
        vars (list<SpellVars>): vars
    """

    def __init__(self, dictionary):
        self.altimages = [(Image(img, True) if not isinstance(img, Image) else img) for img in dictionary.get("altimages", []) if img]
        self.cooldown = dictionary.get("cooldown", [])
        self.cooldownBurn = dictionary.get("cooldownBurn", "")
        self.cost = dictionary.get("cost", [])
        self.costBurn = dictionary.get("costBurn", "")
        self.costType = dictionary.get("costType", "")
        self.description = dictionary.get("description", "")
        self.effect = dictionary.get("effect", [])
        self.effectBurn = dictionary.get("effectBurn", [])
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.key = dictionary.get("key", "")
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val
        self.maxrank = dictionary.get("maxrank", 0)
        self.name = dictionary.get("name", "")
        self.range = dictionary.get("range", "self")
        self.rangeBurn = dictionary.get("rangeBurn", "")
        self.resource = dictionary.get("resource", "")
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip", "")
        self.tooltip = dictionary.get("tooltip", "")
        self.vars = [(SpellVars(svars) if not isinstance(svars, SpellVars) else svars) for svars in dictionary.get("vars", []) if svars]


@cassiopeia.type.core.common.inheritdocs
class Champion(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        allytips (list<str>): ally tips
        blurb (str): blurb
        enemytips (list<str>): enemy tips
        id (int): ID
        image (Image): image
        info (Info): info
        key (str): key
        lore (str): lore
        name (str): name
        partype (str): partype
        passive (Passive): passive
        recommended (list<Recommended>): recommended
        skins (list<Skin>): skins
        spells (list<ChampionSpell>): spells
        stats (Stats): stats
        tags (list<str>): tags
        title (str): title
    """

    def __init__(self, dictionary):
        self.allytips = dictionary.get("allytips", [])
        self.blurb = dictionary.get("blurb", "")
        self.enemytips = dictionary.get("enemytips", [])
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        val = dictionary.get("info", None)
        self.info = Info(val) if val and not isinstance(val, Info) else val
        self.key = dictionary.get("key", "")
        self.lore = dictionary.get("lore", "")
        self.name = dictionary.get("name", "")
        self.partype = dictionary.get("partype", "")
        val = dictionary.get("passive", None)
        self.passive = Passive(val) if val and not isinstance(val, Passive) else val
        self.recommended = [(Recommended(rec) if not isinstance(rec, Recommended) else rec) for rec in dictionary.get("recommended", []) if rec]
        self.skins = [(Skin(skin) if val and not isinstance(skin, Skin) else skin) for skin in dictionary.get("skins", []) if skin]
        self.spells = [(ChampionSpell(spell) if not isinstance(spell, ChampionSpell) else spell) for spell in dictionary.get("spells", []) if spell]
        val = dictionary.get("stats", None)
        self.stats = Stats(val) if val and not isinstance(val, Stats) else val
        self.tags = dictionary.get("tags", [])
        self.title = dictionary.get("title", "")

    @property
    def item_ids(self):
        """
        Gets all item IDs contained in this object
        """
        ids = set()
        for r in self.recommended:
            for b in r.blocks:
                for i in b.items:
                    ids.add(i.id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class ChampionList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all item IDs contained in this object
    """

    def __init__(self, dictionary):
        self.data = {name: Champion(champ) if not isinstance(champ, Champion) else champ for name, champ in dictionary.get("data", {}).items()}
        self.format = dictionary.get("format", "")
        self.keys = dictionary.get("keys", {})
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")

    @property
    def item_ids(self):
        """
        Args:
            data (dict<str, Champion>): champion data
            format (str): format
            keys (dict<str, str>): keys
            type (str): type
            version (str): version
        """
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
    Args:
        data (dict<str, Champion>): champion data
        format (str): format
        keys (dict<str, str>): keys
        type (str): type
        version (str): version
    """

    def __init__(self, dictionary):
        self.isRune = dictionary.get("isRune", False)
        self.tier = dictionary.get("tier", "")
        self.type = dictionary.get("type", "")


@cassiopeia.type.core.common.inheritdocs
class Gold(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all item IDs contained in this object
    """

    def __init__(self, dictionary):
        self.base = dictionary.get("base", 0)
        self.purchasable = dictionary.get("purchasable", False)
        self.sell = dictionary.get("sell", 0)
        self.total = dictionary.get("total", 0)


@cassiopeia.type.core.common.inheritdocs
class BasicDataStats(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        isRune (bool): is a rune
        tier (str): tier
        type (str): type
    """

    def __init__(self, dictionary):
        self.FlatArmorMod = dictionary.get("FlatArmorMod", 0.0)
        self.FlatAttackSpeedMod = dictionary.get("FlatAttackSpeedMod", 0.0)
        self.FlatBlockMod = dictionary.get("FlatBlockMod", 0.0)
        self.FlatCritChanceMod = dictionary.get("FlatCritChanceMod", 0.0)
        self.FlatCritDamageMod = dictionary.get("FlatCritDamageMod", 0.0)
        self.FlatEXPBonus = dictionary.get("FlatEXPBonus", 0.0)
        self.FlatEnergyPoolMod = dictionary.get("FlatEnergyPoolMod", 0.0)
        self.FlatEnergyRegenMod = dictionary.get("FlatEnergyRegenMod", 0.0)
        self.FlatHPPoolMod = dictionary.get("FlatHPPoolMod", 0.0)
        self.FlatHPRegenMod = dictionary.get("FlatHPRegenMod", 0.0)
        self.FlatMPPoolMod = dictionary.get("FlatMPPoolMod", 0.0)
        self.FlatMPRegenMod = dictionary.get("FlatMPRegenMod", 0.0)
        self.FlatMagicDamageMod = dictionary.get("FlatMagicDamageMod", 0.0)
        self.FlatMovementSpeedMod = dictionary.get("FlatMovementSpeedMod", 0.0)
        self.FlatPhysicalDamageMod = dictionary.get("FlatPhysicalDamageMod", 0.0)
        self.FlatSpellBlockMod = dictionary.get("FlatSpellBlockMod", 0.0)
        self.PercentArmorMod = dictionary.get("PercentArmorMod", 0.0)
        self.PercentAttackSpeedMod = dictionary.get("PercentAttackSpeedMod", 0.0)
        self.PercentBlockMod = dictionary.get("PercentBlockMod", 0.0)
        self.PercentCritChanceMod = dictionary.get("PercentCritChanceMod", 0.0)
        self.PercentCritDamageMod = dictionary.get("PercentCritDamageMod", 0.0)
        self.PercentDodgeMod = dictionary.get("PercentDodgeMod", 0.0)
        self.PercentEXPBonus = dictionary.get("PercentEXPBonus", 0.0)
        self.PercentHPPoolMod = dictionary.get("PercentHPPoolMod", 0.0)
        self.PercentHPRegenMod = dictionary.get("PercentHPRegenMod", 0.0)
        self.PercentLifeStealMod = dictionary.get("PercentLifeStealMod", 0.0)
        self.PercentMPPoolMod = dictionary.get("PercentMPPoolMod", 0.0)
        self.PercentMPRegenMod = dictionary.get("PercentMPRegenMod", 0.0)
        self.PercentMagicDamageMod = dictionary.get("PercentMagicDamageMod", 0.0)
        self.PercentMovementSpeedMod = dictionary.get("PercentMovementSpeedMod", 0.0)
        self.PercentPhysicalDamageMod = dictionary.get("PercentPhysicalDamageMod", 0.0)
        self.PercentSpellBlockMod = dictionary.get("PercentSpellBlockMod", 0.0)
        self.PercentSpellVampMod = dictionary.get("PercentSpellVampMod", 0.0)
        self.rFlatArmorModPerLevel = dictionary.get("rFlatArmorModPerLevel", 0.0)
        self.rFlatArmorPenetrationMod = dictionary.get("rFlatArmorPenetrationMod", 0.0)
        self.rFlatArmorPenetrationModPerLevel = dictionary.get("rFlatArmorPenetrationModPerLevel", 0.0)
        self.rFlatCritChanceModPerLevel = dictionary.get("rFlatCritChanceModPerLevel", 0.0)
        self.rFlatCritDamageModPerLevel = dictionary.get("rFlatCritDamageModPerLevel", 0.0)
        self.rFlatDodgeMod = dictionary.get("rFlatDodgeMod", 0.0)
        self.rFlatDodgeModPerLevel = dictionary.get("rFlatDodgeModPerLevel", 0.0)
        self.rFlatEnergyModPerLevel = dictionary.get("rFlatEnergyModPerLevel", 0.0)
        self.rFlatEnergyRegenModPerLevel = dictionary.get("rFlatEnergyRegenModPerLevel", 0.0)
        self.rFlatGoldPer10Mod = dictionary.get("rFlatGoldPer10Mod", 0.0)
        self.rFlatHPModPerLevel = dictionary.get("rFlatHPModPerLevel", 0.0)
        self.rFlatHPRegenModPerLevel = dictionary.get("rFlatHPRegenModPerLevel", 0.0)
        self.rFlatMPModPerLevel = dictionary.get("rFlatMPModPerLevel", 0.0)
        self.rFlatMPRegenModPerLevel = dictionary.get("rFlatMPRegenModPerLevel", 0.0)
        self.rFlatMagicDamageModPerLevel = dictionary.get("rFlatMagicDamageModPerLevel", 0.0)
        self.rFlatMagicPenetrationMod = dictionary.get("rFlatMagicPenetrationMod", 0.0)
        self.rFlatMagicPenetrationModPerLevel = dictionary.get("rFlatMagicPenetrationModPerLevel", 0.0)
        self.rFlatMovementSpeedModPerLevel = dictionary.get("rFlatMovementSpeedModPerLevel", 0.0)
        self.rFlatPhysicalDamageModPerLevel = dictionary.get("rFlatPhysicalDamageModPerLevel", 0.0)
        self.rFlatSpellBlockModPerLevel = dictionary.get("rFlatSpellBlockModPerLevel", 0.0)
        self.rFlatTimeDeadMod = dictionary.get("rFlatTimeDeadMod", 0.0)
        self.rFlatTimeDeadModPerLevel = dictionary.get("rFlatTimeDeadModPerLevel", 0.0)
        self.rPercentArmorPenetrationMod = dictionary.get("rPercentArmorPenetrationMod", 0.0)
        self.rPercentArmorPenetrationModPerLevel = dictionary.get("rPercentArmorPenetrationModPerLevel", 0.0)
        self.rPercentAttackSpeedModPerLevel = dictionary.get("rPercentAttackSpeedModPerLevel", 0.0)
        self.rPercentCooldownMod = dictionary.get("rPercentCooldownMod", 0.0)
        self.rPercentCooldownModPerLevel = dictionary.get("rPercentCooldownModPerLevel", 0.0)
        self.rPercentMagicPenetrationMod = dictionary.get("rPercentMagicPenetrationMod", 0.0)
        self.rPercentMagicPenetrationModPerLevel = dictionary.get("rPercentMagicPenetrationModPerLevel", 0.0)
        self.rPercentMovementSpeedModPerLevel = dictionary.get("rPercentMovementSpeedModPerLevel", 0.0)
        self.rPercentTimeDeadMod = dictionary.get("rPercentTimeDeadMod", 0.0)
        self.rPercentTimeDeadModPerLevel = dictionary.get("rPercentTimeDeadModPerLevel", 0.0)


@cassiopeia.type.core.common.inheritdocs
class ItemTree(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        base (int): base price
        purchasable (bool): is purchasable
        sell (int): sell price
        total (int): total price
    """

    def __init__(self, dictionary):
        self.header = dictionary.get("header", "")
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class Item(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        FlatArmorMod (float): the FlatArmorMod
        FlatAttackSpeedMod (float): the FlatAttackSpeedMod
        FlatBlockMod (float): the FlatBlockMod
        FlatCritChanceMod (float): the FlatCritChanceMod
        FlatCritDamageMod (float): the FlatCritDamageMod
        FlatEXPBonus (float): the FlatEXPBonus
        FlatEnergyPoolMod (float): the FlatEnergyPoolMod
        FlatEnergyRegenMod (float): the FlatEnergyRegenMod
        FlatHPPoolMod (float): the FlatHPPoolMod
        FlatHPRegenMod (float): the FlatHPRegenMod
        FlatMPPoolMod (float): the FlatMPPoolMod
        FlatMPRegenMod (float): the FlatMPRegenMod
        FlatMagicDamageMod (float): the FlatMagicDamageMod
        FlatMovementSpeedMod (float): the FlatMovementSpeedMod
        FlatPhysicalDamageMod (float): the FlatPhysicalDamageMod
        FlatSpellBlockMod (float): the FlatSpellBlockMod
        PercentArmorMod (float): the PercentArmorMod
        PercentAttackSpeedMod (float): the PercentAttackSpeedMod
        PercentBlockMod (float): the PercentBlockMod
        PercentCritChanceMod (float): the PercentCritChanceMod
        PercentCritDamageMod (float): the PercentCritDamageMod
        PercentDodgeMod (float): the PercentDodgeMod
        PercentEXPBonus (float): the PercentEXPBonus
        PercentHPPoolMod (float): the PercentHPPoolMod
        PercentHPRegenMod (float): the PercentHPRegenMod
        PercentLifeStealMod (float): the PercentLifeStealMod
        PercentMPPoolMod (float): the PercentMPPoolMod
        PercentMPRegenMod (float): the PercentMPRegenMod
        PercentMagicDamageMod (float): the PercentMagicDamageMod
        PercentMovementSpeedMod (float): the PercentMovementSpeedMod
        PercentPhysicalDamageMod (float): the PercentPhysicalDamageMod
        PercentSpellBlockMod (float): the PercentSpellBlockMod
        PercentSpellVampMod (float): the PercentSpellVampMod
        rFlatArmorModPerLevel (float): the rFlatArmorModPerLevel
        rFlatArmorPenetrationMod (float): the rFlatArmorPenetrationMod
        rFlatArmorPenetrationModPerLevel (float): the rFlatArmorPenetrationModPerLevel
        rFlatCritChanceModPerLevel (float): the rFlatCritChanceModPerLevel
        rFlatCritDamageModPerLevel (float): the rFlatCritDamageModPerLevel
        rFlatDodgeMod (float): the rFlatDodgeMod
        rFlatDodgeModPerLevel (float): the rFlatDodgeModPerLevel
        rFlatEnergyModPerLevel (float): the rFlatEnergyModPerLevel
        rFlatEnergyRegenModPerLevel (float): the rFlatEnergyRegenModPerLevel
        rFlatGoldPer10Mod (float): the rFlatGoldPer10Mod
        rFlatHPModPerLevel (float): the rFlatHPModPerLevel
        rFlatHPRegenModPerLevel (float): the rFlatHPRegenModPerLevel
        rFlatMPModPerLevel (float): the rFlatMPModPerLevel
        rFlatMPRegenModPerLevel (float): the rFlatMPRegenModPerLevel
        rFlatMagicDamageModPerLevel (float): the rFlatMagicDamageModPerLevel
        rFlatMagicPenetrationMod (float): the rFlatMagicPenetrationMod
        rFlatMagicPenetrationModPerLevel (float): the rFlatMagicPenetrationModPerLevel
        rFlatMovementSpeedModPerLevel (float): the rFlatMovementSpeedModPerLevel
        rFlatPhysicalDamageModPerLevel (float): the rFlatPhysicalDamageModPerLevel
        rFlatSpellBlockModPerLevel (float): the rFlatSpellBlockModPerLevel
        rFlatTimeDeadMod (float): the rFlatTimeDeadMod
        rFlatTimeDeadModPerLevel (float): the rFlatTimeDeadModPerLevel
        rPercentArmorPenetrationMod (float): the rPercentArmorPenetrationMod
        rPercentArmorPenetrationModPerLevel (float): the rPercentArmorPenetrationModPerLevel
        rPercentAttackSpeedModPerLevel (float): the rPercentAttackSpeedModPerLevel
        rPercentCooldownMod (float): the rPercentCooldownMod
        rPercentCooldownModPerLevel (float): the rPercentCooldownModPerLevel
        rPercentMagicPenetrationMod (float): the rPercentMagicPenetrationMod
        rPercentMagicPenetrationModPerLevel (float): the rPercentMagicPenetrationModPerLevel
        rPercentMovementSpeedModPerLevel (float): the rPercentMovementSpeedModPerLevel
        rPercentTimeDeadMod (float): the rPercentTimeDeadMod
        rPercentTimeDeadModPerLevel (float): the rPercentTimeDeadModPerLevel
    """

    def __init__(self, dictionary):
        self.colloq = dictionary.get("colloq", "")
        self.consumeOnFull = dictionary.get("consumeOnFull", False)
        self.consumed = dictionary.get("consumed", False)
        self.depth = dictionary.get("depth", 0)
        self.description = dictionary.get("description", "")
        self.effect = dictionary.get("effect", {})
        self.from_ = dictionary.get("from", [])
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val
        self.group = dictionary.get("group", "")
        self.hideFromAll = dictionary.get("hideFromAll", False)
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.inStore = dictionary.get("inStore", False)
        self.into = dictionary.get("into", [])
        self.maps = dictionary.get("maps", {})
        self.name = dictionary.get("name", "")
        self.plaintext = dictionary.get("plaintext", "")
        self.requiredChampion = dictionary.get("requiredChampion", "")
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")
        self.specialRecipe = dictionary.get("specialRecipe", 0)
        self.stacks = dictionary.get("stacks", 0)
        val = dictionary.get("stats", None)
        self.stats = None if not val else BasicDataStats(val) if not isinstance(val, BasicDataStats) else val
        self.tags = dictionary.get("tags", [])

    @property
    def item_ids(self):
        """
        Args:
            header (str): the header
            tags (list[str]): tags
        """
        ids = set()
        for id_ in self.from_:
            ids.add(int(id_))
        for id_ in self.into:
            ids.add(int(id_))
        return ids


@cassiopeia.type.core.common.inheritdocs
class Group(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        header (str): the header
        tags (list[str]): tags
    """

    def __init__(self, dictionary):
        self.MaxGroupOwnable = dictionary.get("MaxGroupOwnable", "")
        self.key = dictionary.get("key", "")


@cassiopeia.type.core.common.inheritdocs
class BasicData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        colloq (str): colloq
        consumeOnFull (bool): consume on full
        consumed (bool): consumed
        depth (int): depth
        description (str): description
        effect (dict<str, str>): effect
        from_ (list<str>): from
        gold (Gold): data dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        group (str): group
        hideFromAll (bool): hide from all
        id (int): ID
        image (Image): image
        inStore (bool): in store
        into (list<str>): into
        maps (dict<str, bool>): maps
        name (str): name
        plaintext (str): plain text
        requiredChampion (str): required champion
        rune (MetaData): rune
        sanitizedDescription (str): sanitized description
        specialRecipe (int): special recipe
        stacks (int): stacks
        stats (BasicDataStats): stats
        tags (list<str>): tags
    """

    def __init__(self, dictionary):
        self.colloq = dictionary.get("colloq", "")
        self.consumeOnFull = dictionary.get("consumeOnFull", False)
        self.consumed = dictionary.get("consumed", False)
        self.depth = dictionary.get("depth", 0)
        self.description = dictionary.get("description", "")
        self.from_ = dictionary.get("from", [])
        val = dictionary.get("gold", None)
        self.gold = Gold(val) if val and not isinstance(val, Gold) else val
        self.group = dictionary.get("group", "")
        self.hideFromAll = dictionary.get("hideFromAll", False)
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.inStore = dictionary.get("inStore", False)
        self.into = dictionary.get("into", [])
        self.maps = dictionary.get("maps", {})
        self.name = dictionary.get("name", "")
        self.plaintext = dictionary.get("plaintext", "")
        self.requiredChampion = dictionary.get("requiredChampion", "")
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")
        self.specialRecipe = dictionary.get("specialRecipe", 0)
        self.stacks = dictionary.get("stacks", 0)
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class ItemList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all other item IDs contained in this object
    """

    def __init__(self, dictionary):
        val = dictionary.get("basic", None)
        self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val
        self.data = {id_: Item(item) if not isinstance(item, Item) else item for id_, item in dictionary.get("data", {}).items()}
        self.groups = [(Group(group) if not isinstance(group, Group) else group) for group in dictionary.get("groups", []) if group]
        self.tree = [(ItemTree(tree) if not isinstance(tree, ItemTree) else tree) for tree in dictionary.get("tree", []) if tree]
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


######################
# Language Endpoints #
######################
@cassiopeia.type.core.common.inheritdocs
class LanguageStrings(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        MaxGroupOwnable (str): max ownable of group
        key (str): key
    """

    def __init__(self, dictionary):
        self.data = dictionary.get("data", {})
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


################
# Map Endpoint #
################
@cassiopeia.type.core.common.inheritdocs
class MapDetails(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        colloq (str): colloq
        consumeOnFull (bool): consume on full
        consumed (bool): consumed
        depth (int): depth
        description (str): description
        from_ (list<str>): from
        gold (Gold): data dragon includes the gold field for basic data, which is shared by both rune and item. However, only items have a gold field on them, representing their gold cost in the store. Since runes are not sold in the store, they have no gold cost.
        group (str): group
        hideFromAll (bool): hide from all
        id (int): ID
        image (Image): image
        inStore (bool): in store
        into (list<str>): into
        maps (dict<str, bool>): maps
        name (str): name
        plaintext (str): plain text
        requiredChampion (str): required champion
        rune (MetaData): rune
        sanitizedDescription (str): sanitized description
        specialRecipe (int): special recipe
        stacks (int): stacks
        stats (BasicDataStats): stats
        tags (list[str]): tags
    """

    def __init__(self, dictionary):
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.mapId = dictionary.get("mapId", 0)
        self.mapName = dictionary.get("mapName", "")
        self.unpurchasableItemList = dictionary.get("unpurchasableItemList", [])


@cassiopeia.type.core.common.inheritdocs
class MapData(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        basic (BasicData): basic data
        data (dict<str, Item>) item data
        groups (list<Group>): groups
        tree (list<ItemTree>): item tree
        type (str): type
        version (str): version
    """

    def __init__(self, dictionary):
        self.data = {id_: MapDetails(map_) if not isinstance(map_, MapDetails) else map_ for id_, map_ in dictionary.get("data", {}).items()}
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


#####################
# Mastery Endpoints #
#####################
@cassiopeia.type.core.common.inheritdocs
class MasteryTreeItem(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        data (dict<str, str>): language str data
        type (str): type
        version (str): version
    """

    def __init__(self, dictionary):
        self.masteryId = dictionary.get("masteryId", 0)
        self.prereq = dictionary.get("prereq", "")


@cassiopeia.type.core.common.inheritdocs
class MasteryTreeList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        image (Image): image
        mapId (int): ID
        mapName (str): name
        unpurchasableItemList (list<int>): items that can't be purchased on this map (IDs)
    """

    def __init__(self, dictionary):
        self.masteryTreeItems = [(MasteryTreeItem(item) if not isinstance(item, MasteryTreeItem) else item) for item in dictionary.get("masteryTreeItems", []) if item]


@cassiopeia.type.core.common.inheritdocs
class MasteryTree(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        data (dict<str, MapDetails>): map data
        type (str): type
        version (str): version
    """

    def __init__(self, dictionary):
        self.Cunning = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Cunning", []) if list_]
        self.Ferocity = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Ferocity", []) if list_]
        self.Resolve = [(MasteryTreeList(list_) if not isinstance(list_, MasteryTreeList) else list_) for list_ in dictionary.get("Resolve", []) if list_]


@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        masteryId (int): mastery ID
        prereq (str): prerequisites
    """

    def __init__(self, dictionary):
        self.description = dictionary.get("description", [])
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.masteryTree = dictionary.get("masteryTree", "")
        self.name = dictionary.get("name", "")
        self.prereq = dictionary.get("prereq", "")
        self.ranks = dictionary.get("ranks", 0)
        self.sanitizedDescription = dictionary.get("sanitizedDescription", [])

    @property
    def mastery_ids(self):
        """
        Args:
            masteryTreeItems (list<MasteryTreeItem>): mastery tree items
        """
        ids = set()
        if self.prereq:
            ids.add(int(self.prereq))
        return ids


@cassiopeia.type.core.common.inheritdocs
class MasteryList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        masteryTreeItems (list<MasteryTreeItem>): mastery tree items
    """

    def __init__(self, dictionary):
        self.data = {id_: Mastery(mastery) if not isinstance(mastery, Mastery) else mastery for id_, mastery in dictionary.get("data", {}).items()}
        val = dictionary.get("tree", None)
        self.tree = MasteryTree(val) if val and not isinstance(val, MasteryTree) else val
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


##################
# Realm Endpoint #
##################
@cassiopeia.type.core.common.inheritdocs
class Realm(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        Defense (list<MasteryTreeList>): defense tree
        Offense (list<MasteryTreeList>): offense tree
        Utility (list<MasteryTreeList>): utility tree
    """

    def __init__(self, dictionary):
        self.cdn = dictionary.get("cdn", "")
        self.css = dictionary.get("css", "")
        self.dd = dictionary.get("dd", "")
        self.l = dictionary.get("l", "")
        self.lg = dictionary.get("lg", "")
        self.n = dictionary.get("n", {})
        self.profileiconmax = dictionary.get("profileiconmax", 0)
        self.store = dictionary.get("store", "")
        self.v = dictionary.get("v", "")


##################
# Rune Endpoints #
##################
@cassiopeia.type.core.common.inheritdocs
class Rune(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        description (list<str>): description
        id (int): iD
        image (Image): image
        masteryTree (str): legal values: Defense, Offense, Utility
        name (str): name
        prereq (str): prerequisites
        ranks (int): ranks
        sanitizedDescription (list<str>): sanitized description
    """

    def __init__(self, dictionary):
        self.colloq = dictionary.get("colloq", "")
        self.consumeOnFull = dictionary.get("consumeOnFull", False)
        self.consumed = dictionary.get("consumed", False)
        self.depth = dictionary.get("depth", 0)
        self.description = dictionary.get("description", "")
        self.from_ = dictionary.get("from", [])
        self.group = dictionary.get("group", "")
        self.hideFromAll = dictionary.get("hideFromAll", False)
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.inStore = dictionary.get("inStore", False)
        self.into = dictionary.get("into", [])
        self.maps = dictionary.get("maps", {})
        self.name = dictionary.get("name", "")
        self.plaintext = dictionary.get("plaintext", "")
        self.requiredChampion = dictionary.get("requiredChampion", "")
        val = dictionary.get("rune", None)
        self.rune = MetaData(val) if val and not isinstance(val, MetaData) else val
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")
        self.specialRecipe = dictionary.get("specialRecipe", 0)
        self.stacks = dictionary.get("stacks", 0)
        val = dictionary.get("stats", None)
        self.stats = BasicDataStats(val) if val and not isinstance(val, BasicDataStats) else val
        self.tags = dictionary.get("tags", [])


@cassiopeia.type.core.common.inheritdocs
class RuneList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all other mastery IDs contained in this object
    """

    def __init__(self, dictionary):
        val = dictionary.get("basic", None)
        self.basic = BasicData(val) if val and not isinstance(val, BasicData) else val
        self.data = {id_: Rune(rune) if not isinstance(rune, Rune) else rune for id_, rune in dictionary.get("data", {}).items()}
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


############################
# Summoner Spell Endpoints #
############################
@cassiopeia.type.core.common.inheritdocs
class SummonerSpell(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        data (dict<str, Mastery>): mastery data
        tree (MasteryTree): mastery tree
        type (str): type
        version (str): version
    """

    def __init__(self, dictionary):
        self.cooldown = dictionary.get("cooldown", [])
        self.cooldownBurn = dictionary.get("cooldownBurn", "")
        self.cost = dictionary.get("cost", [])
        self.costBurn = dictionary.get("costBurn", "")
        self.costType = dictionary.get("costType", "")
        self.description = dictionary.get("description", "")
        self.effect = dictionary.get("effect", [])
        self.effectBurn = dictionary.get("effectBurn", [])
        self.id = dictionary.get("id", 0)
        val = dictionary.get("image", None)
        self.image = Image(val) if val and not isinstance(val, Image) else val
        self.key = dictionary.get("key", "")
        val = dictionary.get("leveltip", None)
        self.leveltip = LevelTip(val) if val and not isinstance(val, LevelTip) else val
        self.maxrank = dictionary.get("maxrank", 0)
        self.modes = dictionary.get("modes", [])
        self.name = dictionary.get("name", "")
        self.range = dictionary.get("range", "self")
        self.rangeBurn = dictionary.get("rangeBurn", "")
        self.resource = dictionary.get("resource", "")
        self.sanitizedDescription = dictionary.get("sanitizedDescription", "")
        self.sanitizedTooltip = dictionary.get("sanitizedTooltip", "")
        self.summonerLevel = dictionary.get("summonerLevel", 0)
        self.tooltip = dictionary.get("tooltip", "")
        self.vars = [(SpellVars(svars) if not isinstance(svars, SpellVars) else svars) for svars in dictionary.get("vars", []) if svars]


@cassiopeia.type.core.common.inheritdocs
class SummonerSpellList(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        cdn (str): the base CDN url
        css (str): latest changed version of Dragon Magic's css file
        dd (str): latest changed version of Dragon Magic
        l (str): default language for this realm
        lg (str): legacy script mode for IE6 or older
        n (dict<str, str>): latest changed version for each data type listed
        profileiconmax (int): special behavior number identifying the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0
        store (str): additional api data drawn from other sources that may be related to data dragon functionality
        v (str): current version of this file for this realm
    """

    def __init__(self, dictionary):
        self.data = {id_: SummonerSpell(spell) if not isinstance(spell, SummonerSpell) else spell for id_, spell in dictionary.get("data", {}).items()}
        self.type = dictionary.get("type", "")
        self.version = dictionary.get("version", "")


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_block_item():
    global BlockItem

    @cassiopeia.type.core.common.inheritdocs
    class BlockItem(BlockItem, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "BlockItem"
        count = sqlalchemy.Column(sqlalchemy.Integer)
        id = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _block_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Block._id", ondelete="CASCADE"))


def _sa_bind_block():
    global Block

    @cassiopeia.type.core.common.inheritdocs
    class Block(Block, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Block"
        items = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.BlockItem", cascade="all, delete-orphan", passive_deletes=True)
        recMath = sqlalchemy.Column(sqlalchemy.Boolean)
        type = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _recommended_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Recommended._id", ondelete="CASCADE"))


def _sa_bind_spell_vars():
    global SpellVars

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_level_tip():
    global LevelTip

    @cassiopeia.type.core.common.inheritdocs
    class LevelTip(LevelTip, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "LevelTip"
        effect = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        label = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _c_spell_key = sqlalchemy.Column(sqlalchemy.String(30), sqlalchemy.ForeignKey("ChampionSpell.key", ondelete="CASCADE"))
        _s_spell_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("SummonerSpell.id", ondelete="CASCADE"))


def _sa_bind_stats():
    global Stats

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_skin():
    global Skin

    @cassiopeia.type.core.common.inheritdocs
    class Skin(Skin, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Skin"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        num = sqlalchemy.Column(sqlalchemy.Integer)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))


def _sa_bind_recommended():
    global Recommended

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_image():
    global Image

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_passive():
    global Passive

    @cassiopeia.type.core.common.inheritdocs
    class Passive(Passive, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Passive"
        description = sqlalchemy.Column(sqlalchemy.Text)
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))


def _sa_bind_info():
    global Info

    @cassiopeia.type.core.common.inheritdocs
    class Info(Info, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ChampionInfo"
        attack = sqlalchemy.Column(sqlalchemy.Integer)
        defense = sqlalchemy.Column(sqlalchemy.Integer)
        difficulty = sqlalchemy.Column(sqlalchemy.Integer)
        magic = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))


def _sa_bind_champion_spell():
    global ChampionSpell

    @cassiopeia.type.core.common.inheritdocs
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
        name = sqlalchemy.Column(sqlalchemy.String(50))
        range = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        rangeBurn = sqlalchemy.Column(sqlalchemy.String(30))
        resource = sqlalchemy.Column(sqlalchemy.String(50))
        sanitizedDescription = sqlalchemy.Column(sqlalchemy.Text)
        sanitizedTooltip = sqlalchemy.Column(sqlalchemy.Text)
        tooltip = sqlalchemy.Column(sqlalchemy.Text)
        vars = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.SpellVars", cascade="all, delete-orphan", passive_deletes=True)
        _champion_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Champion.id", ondelete="CASCADE"))


def _sa_bind_champion():
    global Champion

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_meta_data():
    global MetaData

    @cassiopeia.type.core.common.inheritdocs
    class MetaData(MetaData, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MetaData"
        isRune = sqlalchemy.Column(sqlalchemy.Boolean)
        tier = sqlalchemy.Column(sqlalchemy.String(30))
        type = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))
        _rune_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Rune.id", ondelete="CASCADE"))


def _sa_bind_gold():
    global Gold

    @cassiopeia.type.core.common.inheritdocs
    class Gold(Gold, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Gold"
        base = sqlalchemy.Column(sqlalchemy.Integer)
        purchasable = sqlalchemy.Column(sqlalchemy.Boolean)
        sell = sqlalchemy.Column(sqlalchemy.Integer)
        total = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _item_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Item.id", ondelete="CASCADE"))


def _sa_bind_basic_data_stats():
    global BasicDataStats

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_item():
    global Item

    @cassiopeia.type.core.common.inheritdocs
    class Item(Item, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Item"
        colloq = sqlalchemy.Column(sqlalchemy.String(100))
        consumeOnFull = sqlalchemy.Column(sqlalchemy.Boolean)
        consumed = sqlalchemy.Column(sqlalchemy.Boolean)
        depth = sqlalchemy.Column(sqlalchemy.Integer)
        description = sqlalchemy.Column(sqlalchemy.Text)
        effect = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
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


def _sa_bind_map_details():
    global MapDetails

    @cassiopeia.type.core.common.inheritdocs
    class MapDetails(MapDetails, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MapDetails"
        image = sqlalchemy.orm.relationship("cassiopeia.type.dto.staticdata.Image", uselist=False, cascade="all, delete-orphan", passive_deletes=True)
        mapId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        mapName = sqlalchemy.Column(sqlalchemy.String(30))
        unpurchasableItemList = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)


def _sa_bind_mastery():
    global Mastery

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_realm():
    global Realm

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_rune():
    global Rune

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_summoner_spell():
    global SummonerSpell

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_all():
    _sa_bind_block_item()
    _sa_bind_block()
    _sa_bind_spell_vars()
    _sa_bind_level_tip()
    _sa_bind_stats()
    _sa_bind_skin()
    _sa_bind_recommended()
    _sa_bind_image()
    _sa_bind_passive()
    _sa_bind_info()
    _sa_bind_champion_spell()
    _sa_bind_champion()
    _sa_bind_meta_data()
    _sa_bind_gold()
    _sa_bind_basic_data_stats()
    _sa_bind_item()
    _sa_bind_map_details()
    _sa_bind_mastery()
    _sa_bind_realm()
    _sa_bind_rune()
    _sa_bind_summoner_spell()
