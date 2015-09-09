import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.staticdata import *

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
        name = sqlalchemy.Column(sqlalchemy.String(30))
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