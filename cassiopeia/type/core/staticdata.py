import re

import cassiopeia.riotapi
import cassiopeia.type.core.common
import cassiopeia.type.dto.staticdata

try:
    from future.builtins.misc import super
except ImportError:
    pass


######################
# Champion Endpoints #
######################
@cassiopeia.type.core.common.inheritdocs
class SetItem(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.BlockItem

    def __str__(self):
        return "{item} ({count})".format(item=self.item, count=self.count)

    @property
    def count(self):
        """int    how many of this item are in the block"""
        return self.data.count

    @property
    def item(self):
        """Item    the item itself"""
        return cassiopeia.riotapi.get_item(self.data.id)


@cassiopeia.type.core.common.inheritdocs
class ItemSet(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Block

    def __str__(self):
        return "Item Set"

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    @cassiopeia.type.core.common.lazyproperty
    def items(self):
        """list<SetItem>    the items in this item set"""
        return [SetItem(item) for item in self.data.items]

    @property
    def rec_math(self):
        """bool    well, we don't know what this one is. let us know if you figure it out."""
        return self.data.recMath

    @property
    def type(self):
        """str    what type the item set is (e.g. starting items)"""
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class SpellVariables(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.SpellVars

    def __str__(self):
        return "Spell Variables"

    @property
    def coefficients(self):
        """list<float>    the coefficients for determining spell scaling"""
        return self.data.coeff

    @property
    def dynamic(self):
        """str    whether the spell variables are dynamic"""
        return self.data.dyn

    @property
    def key(self):
        """str    the identifying key for these variables"""
        return self.data.key

    @property
    def link(self):
        """str    the thing these variables scale off of"""
        return self.data.link

    @property
    def ranks_with(self):
        """str    what these variables rank with"""
        return self.data.ranksWith


@cassiopeia.type.core.common.inheritdocs
class LevelTip(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.LevelTip

    def __str__(self):
        return "Level Tip"

    @property
    def effects(self):
        """list<str>    the changes for the level tooltip, level-by-level"""
        return self.data.effect

    @property
    def labels(self):
        """list<str>    the labels for the changes in effects"""
        return self.data.label


@cassiopeia.type.core.common.inheritdocs
class ChampionStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Stats

    def __str__(self):
        return "Champion Stats"

    @property
    def armor(self):
        """float    armor"""
        return self.data.armor

    @property
    def armor_per_level(self):
        """float    armor per level"""
        return self.data.armorperlevel

    @property
    def attack_damage(self):
        """float    attack damage"""
        return self.data.attackdamage

    @property
    def attack_damage_per_level(self):
        """float    attack damage per level"""
        return self.data.attackdamageperlevel

    @property
    def attack_range(self):
        """float    attack range"""
        return self.data.attackrange

    @property
    def attack_speed(self):
        """float    attack speed"""
        return 0.625 / (1.0 + self.data.attackspeedoffset)

    @property
    def percent_attack_speed_per_level(self):
        """float    attack speed per level"""
        return self.data.attackspeedperlevel / 100

    @property
    def critical_strike_chance(self):
        """float    crititical strike chance"""
        return self.data.crit

    @property
    def critical_strike_chance_per_level(self):
        """float    crititical strike chance per level"""
        return self.data.critperlevel

    @property
    def health(self):
        """float    health"""
        return self.data.hp

    @property
    def health_per_level(self):
        """float    health per level"""
        return self.data.hpperlevel

    @property
    def health_regen(self):
        """float    health regen"""
        return self.data.hpregen

    @property
    def health_regen_per_level(self):
        """float    health regen per level"""
        return self.data.hpregenperlevel

    @property
    def movespeed(self):
        """float    movespeed"""
        return self.data.movespeed

    @property
    def mana(self):
        """float    mana"""
        return self.data.mp

    @property
    def mana_per_level(self):
        """float    mana per level"""
        return self.data.mpperlevel

    @property
    def mana_regen(self):
        """float    mana regen"""
        return self.data.mpregen

    @property
    def mana_regen_per_level(self):
        """float    mana regen per level"""
        return self.data.mpregenperlevel

    @property
    def magic_resist(self):
        """float    magic resist"""
        return self.data.spellblock

    @property
    def magic_resist_per_level(self):
        """float    magic resist per level"""
        return self.data.spellblockperlevel


@cassiopeia.type.core.common.inheritdocs
class Skin(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Skin

    def __init__(self, data, key):
        super().__init__(data)
        self.__key = key

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def splash(self):
        """str    the link to the splash art for this skin"""
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{0}_{1}.jpg".format(self.__key, self.number)

    @property
    def loading(self):
        """str    the link to the loading art for this skin"""
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{0}_{1}.jpg".format(self.__key, self.number)

    @property
    def id(self):
        """int    the ID of this skin"""
        return self.data.id

    @property
    def name(self):
        """str    the name of this skin"""
        return self.data.name

    @property
    def number(self):
        """int    where in the skin order this skin comes"""
        return self.data.num


@cassiopeia.type.core.common.inheritdocs
class RecommendedItems(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Recommended

    def __str__(self):
        "Recommended Items for {champion} on {mode}".format(champion=self.data.champion, mode=self.mode)

    def __iter__(self):
        return iter(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, index):
        return self.blocks[index]

    @cassiopeia.type.core.common.lazyproperty
    def item_sets(self):
        """list<ItemSet>    the sets of items that make up this reommended page"""
        return [ItemSet(block) for block in self.data.blocks]

    @property
    def champion(self):
        """Champion    the champion these recommendations are for"""
        return cassiopeia.riotapi.get_champion_by_name(self.data.champion) if self.data.champion else None

    @property
    def map(self):
        """str    the name of the map these recommendations are for"""
        return self.data.map

    @property
    def mode(self):
        """GameMode    the game mode these recommendations are for"""
        return cassiopeia.type.core.common.GameMode(self.data.mode) if self.data.mode else None

    @property
    def priority(self):
        """bool    whether this is a priority recommendation"""
        return self.data.priority

    @property
    def name(self):
        """str    the name of the recommendations"""
        return self.data.title

    @property
    def type(self):
        """str    the type of recommendations these are"""
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class Image(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Image

    def __str__(self):
        return "Image ({link})".format(link=self.link)

    @property
    def link(self):
        """str    the link to the image. See https://developer.riotgames.com/docs/static-data for more information."""
        return self.data.full

    @property
    def group(self):
        """str    the group for this image"""
        return self.data.group

    @property
    def height(self):
        """int    the height of the image"""
        return self.data.h

    @property
    def sprite(self):
        """str    the sprite image link. See https://developer.riotgames.com/docs/static-data for more information."""
        return self.data.sprite

    @property
    def width(self):
        """int    the width of the image"""
        return self.data.w

    @property
    def x(self):
        """int    the x offset of the image"""
        return self.data.x

    @property
    def y(self):
        """int    the y offset of the image"""
        return self.data.y


@cassiopeia.type.core.common.inheritdocs
class Passive(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Passive

    def __str__(self):
        return self.name

    @property
    def description(self):
        """str    the description for the passive"""
        return self.data.description

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    the image for the passive"""
        return Image(self.data.image) if self.data.image else None

    @property
    def name(self):
        """str    the name of the passive"""
        return self.data.name

    @property
    def sanitized_description(self):
        """str    the sanitized description of the passive"""
        return self.data.sanitizedDescription


@cassiopeia.type.core.common.inheritdocs
class ChampionInfo(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Info

    def __str__(self):
        return "Champion Information"

    @property
    def physical(self):
        """int    physical damage output rating (out of 10)"""
        return self.data.attack

    @property
    def defense(self):
        """int    defensive rating (out of 10)"""
        return self.data.defense

    @property
    def difficulty(self):
        """int    difficulty rating (out of 10)"""
        return self.data.difficulty

    @property
    def magic(self):
        """int    magic damage output rating (out of 10)"""
        return self.data.magic


@cassiopeia.type.core.common.inheritdocs
class Spell(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.ChampionSpell

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

    def __hash__(self):
        return hash(self.key)

    @cassiopeia.type.core.common.lazyproperty
    def alternate_images(self):
        """list<Image>    the alternate images for this spell"""
        return [Image(img) for img in self.data.altimages]

    @property
    def cooldowns(self):
        """list<float>    the cooldowns of this spell level-by-level"""
        return self.data.cooldown

    @property
    def cooldown_burn(self):
        """str    a string formatted list of the spell's cooldowns by level"""
        return self.data.cooldownBurn

    @property
    def costs(self):
        """list<int>    the cost of the spell level-by-level"""
        return self.data.cost

    @property
    def cost_burn(self):
        """str    a string formatted list of the spell's cost by level"""
        return self.data.costBurn

    @property
    def cost_type(self):
        """str    what the spell costs to use (e.g. mana or energy)"""
        return self.data.costType

    @property
    def description(self):
        """str    the description of the spell"""
        return self.data.description

    @property
    def effects(self):
        """list<list<float>>    the level-by-level replacements for {{ e# }} tags in other values"""
        return self.data.effect

    @property
    def effect_burn(self):
        """list<str>    the string formatted replacements for {{ e# }} tags in other values by level"""
        return self.data.effectBurn

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    the image for this spell"""
        return Image(self.data.image) if self.data.image else None

    @property
    def key(self):
        """str    this spell's identifying key"""
        return self.data.key

    @cassiopeia.type.core.common.lazyproperty
    def level_tip(self):
        """LevelTip    the level-up tips for this spell"""
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    @property
    def max_rank(self):
        """int    the maximum level for this spell"""
        return self.data.maxrank

    @property
    def name(self):
        """str    the name of this spell"""
        return self.data.name

    @property
    def range(self):
        """self | list<int>    the level-by-level range of this spell"""
        return self.data.range

    @property
    def range_burn(self):
        """str    the string formatted range of this spell by level"""
        return self.data.rangeBurn

    @property
    def resource(self):
        """str    what resource this spell uses"""
        return self.data.resource

    @property
    def sanitized_description(self):
        """str    the sanitized description of this spell"""
        return self.data.sanitizedDescription

    @property
    def sanitized_tooltip(self):
        """str    the sanitized tooltip for this spell"""
        return self.data.sanitizedTooltip

    @property
    def tooltip(self):
        """str    the tooltip for this spell"""
        return self.data.tooltip

    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        """SpellVariables    the variables that determine this spell's damage"""
        return [SpellVariables(svars) for svars in self.data.vars]

    def __replace_variables(self, text, level, rank):
        if level < 1 or level > 18:
            raise ValueError("Not a valid champion level")
        if rank < 1 or rank > self.max_rank:
            raise ValueError("Not a valid spell rank")

        i = 1
        for effect in self.effects:
            if effect:
                text = text.replace("{{{{ e{i} }}}}".format(i=i), str(effect[rank - 1]))
                i += 1

        for svar in self.variables:
            val = svar.coefficients[0]
            if len(svar.coefficients) == self.max_rank:
                val = svar.coefficients[rank - 1]
            elif svar.coefficients == 18:
                val = svar.coefficients[level - 1]
            replacement = str(val)

            if svar.link == "attackdamage":
                replacement = replacement + " AD"
            elif svar.link == "spelldamage":
                replacement = replacement + " AP"

            text = text.replace("{{{{ {key} }}}}".format(key=svar.key), replacement)

        return text

    @cassiopeia.type.core.common.immutablemethod
    def tooltip_for_level(self, level, rank):
        """Gets the tooltip for this spell for a specific level/rank

        level     int    the level of the champion
        rank      int    the rank of this spell

        return    str    the tooltip for that rank/level
        """
        return self.__replace_variables(self.tooltip, level, rank)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level, rank):
        """Gets the sanitized tooltip for this spell for a specific level/rank

        level     int    the level of the champion
        rank      int    the rank of this spell

        return    str    the sanitized tooltip for that rank/level
        """
        return self.__replace_variables(self.sanitized_tooltip, level, rank)


@cassiopeia.type.core.common.inheritdocs
class Champion(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Champion

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def ally_tips(self):
        """list<str>    the set of tips for allies of this champion"""
        return self.data.allytips

    @property
    def blurb(self):
        """str    the blurb for this champion"""
        return self.data.blurb

    @property
    def enemy_tips(self):
        """list<str>    the set of tips for enemies of this champion"""
        return self.data.enemytips

    @property
    def id(self):
        """int    the ID of this champion"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    the image of this champion"""
        return Image(self.data.image) if self.data.image else None

    @cassiopeia.type.core.common.lazyproperty
    def info(self):
        """ChampionInfo    ratings of what this champion is good/bad at"""
        return ChampionInfo(self.data.info) if self.data.info else None

    @property
    def key(self):
        """str    the identifying key for this champion"""
        return self.data.key

    @property
    def lore(self):
        """str    this champion's lore"""
        return self.data.lore

    @property
    def name(self):
        """str    this champion's name"""
        return self.data.name

    @property
    def resource(self):
        """str    the resource this champion uses"""
        return self.data.partype

    @cassiopeia.type.core.common.lazyproperty
    def passive(self):
        """Passive    this champion's passive"""
        return Passive(self.data.passive) if self.data.passive else None

    @cassiopeia.type.core.common.lazyproperty
    def recommended_items(self):
        """list<RecommendedItems>    item recommendations for this champion"""
        return [RecommendedItems(rec) for rec in self.data.recommended]

    @cassiopeia.type.core.common.lazyproperty
    def skins(self):
        """list<Skin>    this champion's skins"""
        return [Skin(skin, self.key) for skin in self.data.skins]

    @cassiopeia.type.core.common.lazyproperty
    def spells(self):
        """list<Spell>    this champion's spells"""
        return [Spell(spell) for spell in self.data.spells]

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """ChampionStats    this champion's combat stats"""
        return ChampionStats(self.data.stats) if self.data.stats else None

    @property
    def tags(self):
        """list<str>    tags for searching for this champion"""
        return self.data.tags

    @property
    def title(self):
        """str    this champion's title"""
        return self.data.title

    @cassiopeia.type.core.common.immutablemethod
    def status(self):
        """Gets the status for this champion (whether they are disabled, etc.)

        return      ChampionStatus    the champion's status
        """
        return cassiopeia.riotapi.get_champion_status(self)

    @cassiopeia.type.core.common.immutablemethod
    def mastery_level(self, summoner):
        """Gets the ChampionMastery object for the specified summoner

        summoner    Summoner           the summoner to get champion mastery for

        return      ChampionMastery    the summoner's champion mastery value for the champion
        """
        return cassiopeia.riotapi.get_champion_mastery(summoner, self)


##################
# Item Endpoints #
##################
@cassiopeia.type.core.common.inheritdocs
class MetaData(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.MetaData

    def __str__(self):
        return "Meta Data"

    @property
    def rune(self):
        """bool    whether the item is a rune"""
        return self.data.isRune

    @property
    def tier(self):
        """str    what tier the item is"""
        return self.data.tier

    @property
    def type(self):
        """str    the type of item it is"""
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class Gold(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Gold

    def __str__(self):
        return "{price} gold".format(price=self.total)

    @property
    def base(self):
        """int    the base price of the item"""
        return self.data.base

    @property
    def purchasable(self):
        """bool    whether the item can be bought"""
        return self.data.purchasable

    @property
    def sell(self):
        """int    the sell price of the item"""
        return self.data.sell

    @property
    def total(self):
        """int    the total price of the item"""
        return self.data.total


@cassiopeia.type.core.common.inheritdocs
class ItemStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.BasicDataStats

    def __init__(self, data, scraped_stats={}):
        super().__init__(data)
        for k, v in scraped_stats.items():
            if "percent" in k and v > 1.0:
                scraped_stats[k] = v / 100.0
        self.__scraped_stats = scraped_stats

    def __str__(self):
        return "Item Stats"

    @property
    def armor(self):
        """float    armor"""
        return self.data.FlatArmorMod

    @property
    def attack_speed(self):
        """float    attack speed"""
        return self.data.FlatAttackSpeedMod

    @property
    def block(self):
        """float    blocked damage per attack"""
        return self.data.FlatBlockMod

    @property
    def percent_block(self):
        """float    percent blocked damage per attack"""
        return self.data.PercentBlockMod

    @property
    def critical_strike_chance(self):
        """float    critical strike chance"""
        return self.data.FlatCritChanceMod + self.data.PercentCritChanceMod

    @property
    def critical_strike_damage(self):
        """float    critical strike damage modification"""
        return self.data.FlatCritDamageMod

    @property
    def xp_bonus(self):
        """float    experience bonus"""
        return self.data.FlatEXPBonus

    @property
    def energy(self):
        """float    energy"""
        return self.data.FlatEnergyPoolMod

    @property
    def energy_regen(self):
        """float    energy regen"""
        return self.data.FlatEnergyRegenMod

    @property
    def health(self):
        """float    health"""
        return self.data.FlatHPPoolMod

    @property
    def health_regen(self):
        """float    health regen"""
        return self.data.FlatHPRegenMod

    @property
    def mana(self):
        """float    mana"""
        return self.data.FlatMPPoolMod

    @property
    def mana_regen(self):
        """float    mana regen"""
        return self.data.FlatMPRegenMod

    @property
    def ability_power(self):
        """float    ability power"""
        return self.data.FlatMagicDamageMod

    @property
    def movespeed(self):
        """float    movespeed"""
        return self.data.FlatMovementSpeedMod

    @property
    def attack_damage(self):
        """float    attack damage"""
        return self.data.FlatPhysicalDamageMod

    @property
    def magic_resist(self):
        """float    magic resist"""
        return self.data.FlatSpellBlockMod

    @property
    def percent_armor(self):
        """float    percent armor"""
        return self.data.PercentArmorMod

    @property
    def percent_attack_speed(self):
        """float    percent attack speed"""
        return self.data.PercentAttackSpeedMod

    @property
    def percent_critical_strike_damage(self):
        """float    percent critical strike damage modification"""
        return self.data.PercentCritDamageMod

    @property
    def percent_xp_bonus(self):
        """float    percent experience bonus"""
        return self.data.PercentEXPBonus

    @property
    def percent_health(self):
        """float    percent health"""
        return self.data.PercentHPPoolMod

    @property
    def percent_health_regen(self):
        """float    percent health regen"""
        return self.data.PercentHPRegenMod

    @property
    def life_steal(self):
        """float    life steal"""
        return self.data.PercentLifeStealMod

    @property
    def percent_mana(self):
        """float    percent mana"""
        return self.data.PercentMPPoolMod

    @property
    def percent_mana_regen(self):
        """float    percent mana regen"""
        return self.data.PercentMPRegenMod

    @property
    def percent_ability_power(self):
        """float    percent ability power"""
        return self.data.PercentMagicDamageMod + self.__scraped_stats.get("percent_ability_power", 0.0)

    @property
    def percent_movespeed(self):
        """float    percent movespeed"""
        return self.data.PercentMovementSpeedMod

    @property
    def percent_attack_damage(self):
        """float    percent attack damage"""
        return self.data.PercentPhysicalDamageMod

    @property
    def percent_magic_resist(self):
        """float    percent magic resist"""
        return self.data.PercentSpellBlockMod

    @property
    def spell_vamp(self):
        """float    spell vamp"""
        return self.data.PercentSpellVampMod

    @property
    def armor_per_level(self):
        """float    armor per level"""
        return self.data.rFlatArmorModPerLevel

    @property
    def armor_penetration(self):
        """float    armor penetration"""
        return self.data.rFlatArmorPenetrationMod + self.__scraped_stats.get("armor_pen", 0.0)

    @property
    def armor_penetration_per_level(self):
        """float    armor penetration per level"""
        return self.data.rFlatArmorPenetrationModPerLevel

    @property
    def critical_strike_chance_per_level(self):
        """float    critical strike chance per level"""
        return self.data.rFlatCritChanceModPerLevel

    @property
    def critical_strike_damage_per_level(self):
        """float    critical strike damage per level"""
        return self.data.rFlatCritDamageModPerLevel

    @property
    def dodge_chance(self):
        """float    dodge chance"""
        return self.data.rFlatDodgeMod + self.data.PercentDodgeMod

    @property
    def dodge_chance_per_level(self):
        """float    dodge change per level"""
        return self.data.rFlatDodgeModPerLevel

    @property
    def energy_per_level(self):
        """float    energy per level"""
        return self.data.rFlatEnergyModPerLevel

    @property
    def energy_regen_per_level(self):
        """float    energy regen per level"""
        return self.data.rFlatEnergyRegenModPerLevel

    @property
    def gold_per_ten(self):
        """float    gold per 10 seconds"""
        return self.data.rFlatGoldPer10Mod + self.__scraped_stats.get("gold_per_ten", 0.0)

    @property
    def health_per_level(self):
        """float    health per level"""
        return self.data.rFlatHPModPerLevel

    @property
    def health_regen_per_level(self):
        """float    health regen per level"""
        return self.data.rFlatHPRegenModPerLevel

    @property
    def mana_per_level(self):
        """float    mana per level"""
        return self.data.rFlatMPModPerLevel

    @property
    def mana_regen_per_level(self):
        """float    mana regen per level"""
        return self.data.rFlatMPRegenModPerLevel

    @property
    def ability_power_per_level(self):
        """float    ability power per level"""
        return self.data.rFlatMagicDamageModPerLevel

    @property
    def magic_penetration(self):
        """float    magic penetration"""
        return self.data.rFlatMagicPenetrationMod + self.__scraped_stats.get("magic_pen", 0.0)

    @property
    def magic_penetration_per_level(self):
        """float    magic penetration per level"""
        return self.data.rFlatMagicPenetrationModPerLevel

    @property
    def movespeed_per_level(self):
        """float    movespeed per level"""
        return self.data.rFlatMovementSpeedModPerLevel

    @property
    def attack_damage_per_level(self):
        """float    attack damage per level"""
        return self.data.rFlatPhysicalDamageModPerLevel

    @property
    def magic_resist_per_level(self):
        """float    magic reists per level"""
        return self.data.rFlatSpellBlockModPerLevel

    @property
    def time_dead(self):
        """float    time dead modification"""
        return abs(self.data.rFlatTimeDeadMod)

    @property
    def time_dead_per_level(self):
        """float    time dead modification per level"""
        return abs(self.data.rFlatTimeDeadModPerLevel)

    @property
    def percent_armor_penetration(self):
        """float    percent armor pentration"""
        return self.data.rPercentArmorPenetrationMod + self.__scraped_stats.get("percent_armor_pen", 0.0)

    @property
    def percent_armor_penetration_per_level(self):
        """float    percent armor penetration per level"""
        return self.data.rPercentArmorPenetrationModPerLevel

    @property
    def percent_attack_speed_per_level(self):
        """float    percent attack speed per level"""
        return self.data.rPercentAttackSpeedModPerLevel

    @property
    def cooldown_reduction(self):
        """float    cooldown reduction"""
        return abs(self.data.rPercentCooldownMod + self.__scraped_stats.get("percent_cooldown_reduction", 0.0))

    @property
    def cooldown_reduction_per_level(self):
        """float    cooldown reduction per level"""
        return abs(self.data.rPercentCooldownModPerLevel)

    @property
    def percent_magic_penetration(self):
        """float    percent magic penetration"""
        return self.data.rPercentMagicPenetrationMod + self.__scraped_stats.get("percent_magic_pen", 0.0)

    @property
    def percent_magic_pen_per_level(self):
        """float    percent magic penetration per level"""
        return self.data.rPercentMagicPenetrationModPerLevel

    @property
    def percent_movespeed_per_level(self):
        """float    percent movespeed per level"""
        return self.data.rPercentMovementSpeedModPerLevel

    @property
    def percent_time_dead(self):
        """float    percent time dead modification"""
        return abs(self.data.rPercentTimeDeadMod)

    @property
    def percent_time_dead_per_level(self):
        """float    percent time dead modification per level"""
        return abs(self.data.rPercentTimeDeadModPerLevel)


@cassiopeia.type.core.common.inheritdocs
class Item(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Item

    __stat_patterns = {
        "percent_cooldown_reduction": "\\+(\\d+) *% Cooldown Reduction *(<br>|</stats>|</passive>|$)",
        "armor_pen": "\\+(\\d+) *Armor Penetration *(<br>|</stats>|</passive>|$)",
        "percent_armor_pen": "ignores (\\d+)% of the target's Armor",
        "magic_pen": "\\+(\\d+) *Magic Penetration *(<br>|</stats>|</passive>|$)",
        "percent_magic_pen": "ignores (\\d+)% of the target's Magic Resist",
        "gold_per_ten": "\\+(\\d+) *Gold per 10 seconds *(<br>|</stats>|</passive>|$)",
        "percent_ability_power": "Increases Ability Power by (\\d+)%"
    }

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def keywords(self):
        """str    a string formatted list of search keywords for this item in the shop"""
        return self.data.colloq

    @property
    def consume_on_full(self):
        """bool    well, we don't know what this one is. let us know if you figure it out."""
        return self.data.consumeOnFull

    @property
    def consumable(self):
        """bool    whether the item is a consumable"""
        return self.data.consumed

    @property
    def tier(self):
        """int    the tier of the item"""
        return self.data.depth

    @property
    def description(self):
        """str    the item's description"""
        return self.data.description

    @property
    def effect(self):
        """dict<str, bool>    the item's effects"""
        return self.effect

    @property
    def components(self):
        """list<Item>    the components for this item"""
        return cassiopeia.riotapi.get_items([int(id_) for id_ in self.data.from_])

    @cassiopeia.type.core.common.lazyproperty
    def gold(self):
        """Gold    price information for this item"""
        return Gold(self.data.gold) if self.data.gold else None

    @property
    def group(self):
        """str    the group for this item"""
        return self.data.group

    @property
    def hide(self):
        """bool    well, we don't know what this one is. let us know if you figure it out."""
        return self.data.hide_from_all

    @property
    def id(self):
        """int    the ID of this item"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    this item's image"""
        return Image(self.data.image) if self.data.image else None

    @property
    def in_store(self):
        """bool    well, we don't know what this one is. let us know if you figure it out."""
        return self.data.inStore

    @property
    def component_of(self):
        """list<Item>    the items this one is a component of"""
        return cassiopeia.riotapi.get_items([int(id_) for id_ in self.data.into])

    @property
    def maps(self):
        """dict<Map, bool>    a listing of whether this item is available on each map"""
        return {cassiopeia.type.core.common.Map(int(id_)): allowed for id_, allowed in self.data.maps.items()}

    @property
    def name(self):
        """str    the name of this item"""
        return self.data.name

    @property
    def blurb(self):
        """str    the blurb for this item"""
        return self.data.plaintext

    @property
    def required_champion(self):
        """Champion    the required champion for this item"""
        return cassiopeia.riotapi.get_champion_by_name(self.data.requiredChampion) if self.data.requiredChampion else None

    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        """MetaData    meta data about this item"""
        return MetaData(self.data.rune) if self.data.rune else None

    @property
    def sanitized_description(self):
        """str    the sanitized description of this item"""
        return self.data.sanitizedDescription

    @property
    def special_recipe(self):
        """int    well, we don't know what this one is. let us know if you figure it out."""
        return self.data.specialRecipe

    @property
    def stacks(self):
        """int    the number of stacks this item can have"""
        return self.data.stacks

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """ItemStats    the stats for this item"""
        scraped_stats = {}
        for stat, regex in Item.__stat_patterns.items():
            match = re.search(regex, self.description)
            if match:
                scraped_stats[stat] = float(match.group(1))
        return ItemStats(self.data.stats, scraped_stats) if self.data.stats else None

    @property
    def tags(self):
        """list<str>    this item's tags for sorting items"""
        return self.data.tags

    # Left out these: attack_range, percent_time_dead, percent_time_dead_per_level, time_dead, time_dead_per_level, gold_per_ten, starting_gold, percent_xp_bonus, xp_bonus
    __item_categories = {
        "Defense": {
            "Health": ["base_health", "health", "percent_health", "health_regen", "health_regen_per_level", "bonus_health_regen", "percent_health_regen", "health_per_level", "base_health_regen", "bonus_health"],
            "Armor": ["armor", "bonus_armor", "armor_per_level", "base_armor", "percent_armor"],
            "Magic Resist": ["magic_resist_per_level", "base_magic_resist", "magic_resist", "percent_magic_resist", "bonus_magic_resist"],
            "Tenacity": ["percent_crowd_control_reduction"],
            "Other": ["dodge_chance", "dodge_chance_per_level", "block", "percent_block"]
        },
        "Attack": {
            "Damage": ["bonus_attack_damage", "attack_damage", "base_attack_damage", "percent_attack_damage", "percent_total_damage_increase", "attack_damage_per_level"],
            "Critical Strike": ["percent_critical_strike_damage", "critical_strike_chance_per_level", "critical_strike_damage", "critical_strike_damage_per_level", "critical_strike_chance", "critical_strike_chance_per_level"],
            "Attack Speed": ["percent_attack_speed", "attack_speed", "bonus_attack_speed", "attack_speed_per_level", "base_attack_speed", "percent_attack_speed_per_level"],
            "Life Steal": ["life_steal"],
            "Other": ["armor_penetration", "percent_armor_penetration", "armor_penetration_per_level", "percent_armor_penetration_per_level", "magic_penetration", "percent_magic_penetration", "magic_penetration_per_level", "percent_magic_pen_per_level"]
        },
        "Magic": {
            "Ability Power": ["ability_power", "ability_power_per_level", "percent_ability_power"],
            "Cooldown Reduction": ["item_cooldown_reduction", "cooldown_reduction_per_level", "cooldown_reduction"],
            "Spell Vamp": ["spell_vamp"],
            "Mana": ["base_mana", "bonus_mana", "energy_per_level", "energy", "mana_per_level", "mana", "percent_mana"],
            "Mana Regen": ["base_mana_regen", "bonus_mana_regen", "mana_regen_per_level", "percent_mana_regen", "mana_regen", "energy_regen", "energy_regen_per_level"],
            "Other": []
        },
        "Movement": {
            "Other Movement Items": ["out_of_combat_movespeed", "percent_movespeed", "movespeed_per_level", "movespeed", "percent_movespeed_per_level"],
            "Other": []
        }
    }
    __boot_ids = {"1001", "3117", "3158", "3111", "3006", "3009", "3020", "3047"}

    @cassiopeia.type.core.common.lazyproperty
    def categories(self):
        """list<str>    the shop categories that this item belongs to"""
        if self.consumable:
            cats = {"Consumable"}
        else:
            cats = set()
        if self.stats is not None:
            for cat_name, cat in Item.__item_categories.items():
                for subcat, attrs in cat.items():
                    for attr in attrs:
                        if getattr(self.stats, attr, 0.0) != 0.0:
                            cats.add(cat_name)
                            cats.add(subcat)
        if str(self.id) in Item.__boot_ids or len(set(self.data.from_) & Item.__boot_ids) > 0:
            cats.add("Boots")
            cats.remove("Other Movement Items")

        return list(cats)


################
# Map Endpoint #
################
@cassiopeia.type.core.common.inheritdocs
class MapDetails(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.MapDetails

    def __str__(self):
        return self.data.name

    def __eq__(self, other):
        return self.data.mapId == other.data.mapId

    def __ne__(self, other):
        return self.data.mapId != other.data.mapId

    def __hash__(self):
        return hash(self.data.mapId)

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    the image of this map"""
        return Image(self.data.image) if self.data.image else None

    @property
    def map_id(self):
        """int    the ID of this map"""
        return self.data.mapId

    @property
    def map(self):
        """Map    the map"""
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def unpurchasable_items(self):
        """list<Item>    the items that can't be bought on this map"""
        return list(filter(None, cassiopeia.riotapi.get_items(self.data.unpurchasableItemList)))


#####################
# Mastery Endpoints #
#####################
@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Mastery

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def descriptions(self):
        """list<str>    descriptions of this mastery by rank"""
        return self.data.description

    @property
    def id(self):
        """int    the ID of this mastery"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    this mastery's image"""
        return Image(self.data.image) if self.data.image else None

    @property
    def tree(self):
        """str    which mastery tree this mastery belongs to"""
        return self.data.masteryTree

    @property
    def name(self):
        """name    the name of this mastery"""
        return self.data.name.strip()

    @property
    def prerequisite(self):
        """Mastery    the prerequisite for this mastery"""
        return cassiopeia.riotapi.get_mastery(int(self.data.prereq)) if self.data.prereq else None

    @property
    def max_rank(self):
        """int    the max rank for this mastery"""
        return self.data.ranks

    @property
    def sanitized_descriptions(self):
        """list<str>    sanitized descriptions of this mastery by rank"""
        return self.data.sanitizedDescription


##################
# Realm Endpoint #
##################
@cassiopeia.type.core.common.inheritdocs
class Realm(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Realm

    def __str__(self):
        return "Realm"

    def __eq__(self, other):
        return self.cdn == other.cdn

    def __ne__(self, other):
        return self.cdn != other.cdn

    def __hash__(self):
        return hash(self.cdn)

    @property
    def cdn(self):
        """str    the base CDN url"""
        return self.data.cdn

    @property
    def css(self):
        """str    the latest version of the Dragon Magic's css file"""
        return self.data.css

    @property
    def dragon_magic(self):
        """str    the lastest version of Dragon Magic"""
        return self.data.dd

    @property
    def language(self):
        """str    the default locale for this realm"""
        return self.data.l

    @property
    def legacy(self):
        """str    the legacy script mode for IE6 or older"""
        return self.data.lg

    @property
    def data_type_versions(self):
        """dict<str, str>    the latest versions for listed data types"""
        return self.data.n

    @property
    def profile_icon_id_max(self):
        """int    the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0."""
        return self.data.profileiconmax

    @property
    def store(self):
        """str    additional api data drawn from other sources that may be related to data dragon functionality"""
        return self.data.store

    @property
    def version(self):
        """str    the current version of this file"""
        return self.data.v


##################
# Rune Endpoints #
##################
@cassiopeia.type.core.common.inheritdocs
class Rune(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Rune

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def description(self):
        """str    the rune's description"""
        return self.data.description

    @property
    def id(self):
        """int    the ID of this rune"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    this rune's image"""
        return Image(self.data.image) if self.data.image else None

    @property
    def name(self):
        """str    the name of this rune"""
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        """MetaData    meta data about this rune"""
        return MetaData(self.data.rune) if self.data.rune else None

    @property
    def sanitized_description(self):
        """str    the sanitized description of this rune"""
        return self.data.sanitizedDescription

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """ItemStats    the stats for this rune"""
        return ItemStats(self.data.stats) if self.data.stats else None

    @property
    def tags(self):
        """list<str>    this rune's tags for sorting runes"""
        return self.data.tags

    @property
    def rune_type(self):
        """str    what type of rune this is"""
        try:
            return next(iter(set(self.tags).intersection({"mark", "seal", "glyph", "quintessence"})))
        except:
            return ""


############################
# Summoner Spell Endpoints #
############################
@cassiopeia.type.core.common.inheritdocs
class SummonerSpell(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.SummonerSpell

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def cooldowns(self):
        """list<float>    the cooldowns of this spell level-by-level"""
        return self.data.cooldown

    @property
    def cooldown_burn(self):
        """str    a string formatted list of the spell's cooldowns by level"""
        return self.data.cooldownBurn

    @property
    def costs(self):
        """list<int>    the cost of the spell level-by-level"""
        return self.data.cost

    @property
    def cost_burn(self):
        """str    a string formatted list of the spell's cost by level"""
        return self.data.costBurn

    @property
    def cost_type(self):
        """str    what the spell costs to use (e.g. mana or energy)"""
        return self.data.costType

    @property
    def description(self):
        """str    the description of the spell"""
        return self.data.description

    @property
    def effects(self):
        """list<list<float>>    the level-by-level replacements for {{ e# }} tags in other values"""
        return self.data.effect

    @property
    def effect_burn(self):
        """list<str>    the string formatted replacements for {{ e# }} tags in other values by level"""
        return self.data.effectBurn

    @property
    def id(self):
        """int    the ID of this spell"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """Image    the image for this spell"""
        return Image(self.data.image) if self.data.image else None

    @property
    def key(self):
        """str    this spell's identifying key"""
        return self.data.key

    @cassiopeia.type.core.common.lazyproperty
    def leveltip(self):
        """LevelTip    the level-up tips for this spell"""
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    @property
    def max_rank(self):
        """int    the maximum level for this spell"""
        return self.data.maxrank

    @property
    def modes(self):
        """list<GameMode>    the game modes that this spell is allowed on"""
        return [cassiopeia.type.core.common.GameMode(mode) for mode in self.data.modes]

    @property
    def name(self):
        """str    the name of this spell"""
        return self.data.name

    @property
    def range(self):
        """self | list<int>    the level-by-level range of this spell"""
        return self.data.range

    @property
    def range_burn(self):
        """str    the string formatted range of this spell by level"""
        return self.data.rangeBurn

    @property
    def resource(self):
        """str    what resource this spell uses"""
        return self.data.resource

    @property
    def sanitized_description(self):
        """str    the sanitized description of this spell"""
        return self.data.sanitizedDescription

    @property
    def sanitized_tooltip(self):
        """str    the sanitized tooltip for this spell"""
        return self.data.sanitizedTooltip

    @property
    def summoner_level(self):
        """int    the summoner level required to use this spell"""
        return self.data.summonerLevel

    @property
    def tooltip(self):
        """str    the tooltip for this spell"""
        return self.data.tooltip

    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        """SpellVariables    the variables that determine this spell's effects"""
        return [SpellVariables(svars) for svars in self.data.vars]

    def __replace_variables(self, text, level):
        if level < 1 or level > 18:
            raise ValueError("Not a valid champion level")

        for svar in self.variables:
            val = svar.coefficients[level - 1] if svar.link == "@player.level" else svar.coefficients[0]
            text = text.replace("{{{{ {key} }}}}".format(key=svar.key), str(val))

        return text

    @cassiopeia.type.core.common.immutablemethod
    def tooltip_for_level(self, level):
        """Gets the tooltip for this spell for a specific level

        level     int    the level of the champion

        return    str    the tooltip for that rank/level
        """
        return self.__replace_variables(self.tooltip, level)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level):
        """Gets the sanitized tooltip for this spell for a specific level

        level     int    the level of the champion

        return    str    the sanitized tooltip for that rank/level
        """
        return self.__replace_variables(self.sanitized_tooltip, level)


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_rebind_all():
    SetItem.dto_type = cassiopeia.type.dto.staticdata.BlockItem
    ItemSet.dto_type = cassiopeia.type.dto.staticdata.Block
    SpellVariables.dto_type = cassiopeia.type.dto.staticdata.SpellVars
    LevelTip.dto_type = cassiopeia.type.dto.staticdata.LevelTip
    ChampionStats.dto_type = cassiopeia.type.dto.staticdata.Stats
    Skin.dto_type = cassiopeia.type.dto.staticdata.Skin
    RecommendedItems.dto_type = cassiopeia.type.dto.staticdata.Recommended
    Image.dto_type = cassiopeia.type.dto.staticdata.Image
    Passive.dto_type = cassiopeia.type.dto.staticdata.Passive
    ChampionInfo.dto_type = cassiopeia.type.dto.staticdata.Info
    Spell.dto_type = cassiopeia.type.dto.staticdata.ChampionSpell
    Champion.dto_type = cassiopeia.type.dto.staticdata.Champion
    MetaData.dto_type = cassiopeia.type.dto.staticdata.MetaData
    Gold.dto_type = cassiopeia.type.dto.staticdata.Gold
    ItemStats.dto_type = cassiopeia.type.dto.staticdata.BasicDataStats
    Item.dto_type = cassiopeia.type.dto.staticdata.Item
    MapDetails.dto_type = cassiopeia.type.dto.staticdata.MapDetails
    Mastery.dto_type = cassiopeia.type.dto.staticdata.Mastery
    Realm.dto_type = cassiopeia.type.dto.staticdata.Realm
    Rune.dto_type = cassiopeia.type.dto.staticdata.Rune
    SummonerSpell.dto_type = cassiopeia.type.dto.staticdata.SummonerSpell
