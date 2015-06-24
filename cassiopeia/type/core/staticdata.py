import re

import cassiopeia.riotapi
import cassiopeia.type.core.common

######################
# Champion Endpoints #
######################

class BlockItem(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "{item} ({count})".format(item=self.item, count=self.count)

    @property
    def count(self):
        return self.data.count

    @property
    def item(self):
        return cassiopeia.riotapi.get_item(self.data.id)


class Block(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Block Item"

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    @cassiopeia.type.core.common.lazyproperty
    def items(self):
        return [BlockItem(item) for item in self.data.items]

    @property
    def rec_math(self):
        return self.data.recMath

    @property
    def type(self):
        return self.data.type


class SpellVariables(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Spell Variables"

    @property
    def coefficients(self):
        return self.data.coeff

    @property
    def dynamic(self):
        return self.data.dyn

    @property
    def key(self):
        return self.data.key

    @property
    def link(self):
        return self.data.link

    @property
    def ranks_ith(self):
        return self.data.ranksWith


class LevelTip(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Level Tip"

    @property
    def effects(self):
        return self.data.effect

    @property
    def labels(self):
        return self.data.label


class ChampionStats(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Champion Stats"

    # float # Armor
    @property
    def armor(self):
        return self.data.armor

    # float # Armor per level 
    @property
    def armor_per_level(self):
        return self.data.armorperlevel

    # float # Attack damage
    @property
    def attack_damage(self):
        return self.data.attackdamage

    # float # Attack damage per level
    @property
    def attack_damage_per_level(self):
        return self.data.attackdamageperlevel

    # float # Attack range
    @property
    def attack_range(self):
        return self.data.attackrange

    # float # Attack speed offset
    @property
    def attack_speed(self):
        return self.data.attackspeedoffset

    # float # Attack speed per level
    @property
    def attack_speed_per_level(self):
        return self.data.attackspeedperlevel

    # float # Crit chance
    @property
    def crit(self):
        return self.data.crit

    # float # Crit change per level
    @property
    def crit_per_level(self):
        return self.data.critperlevel

    # float # Health
    @property
    def health(self):
        return self.data.hp

    # float # Health per level
    @property
    def health_per_level(self):
        return self.data.hpperlevel

    # float # Health regen
    @property
    def health_regen(self):
        return self.data.hpregen

    # float # Health regen per level
    @property
    def health_regen_per_level(self):
        return self.data.hpregenperlevel

    # float # Movespeed
    @property
    def movespeed(self):
        return self.data.movespeed

    # float # Mana
    @property
    def mana(self):
        return self.data.mp

    # float # Mana per level
    @property
    def mana_per_level(self):
        return self.data.mpperlevel

    # float # Mana regen
    @property
    def mana_regen(self):
        return self.data.mpregen

    # float # Mana regen per level
    @property
    def mana_regen_per_level(self):
        return self.data.mpregenperlevel

    # float # Magic resist
    @property
    def magic_resist(self):
        return self.data.spellblock

    # float # Magic resist per level
    @property
    def magic_resist_per_level(self):
        return self.data.spellblockperlevel


class Skin(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    @property
    def id(self):
        return self.data.id

    @property
    def name(self):
        return self.data.name

    @property
    def number(self):
        return self.data.num


class RecommendedItems(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        "Recommended Items for {champion} on {mode}".format(champion=self.data.champion, mode=self.mode)

    def __iter__(self):
        return iter(self.blocks)

    def __len__(self):
        return len(self.blocks)

    def __getitem__(self, index):
        return self.blocks[index]

    @cassiopeia.type.core.common.lazyproperty
    def blocks(self):
        return [Block(block) for block in self.data.blocks]

    @property
    def champion(self):
        return cassiopeia.riotapi.get_champion_by_name(self.data.champion) if self.data.champion else None

    @property
    def map(self):
        return self.data.map

    @property
    def mode(self):
        return self.data.mode

    @property
    def priority(self):
        return self.data.priority

    @property
    def title(self):
        return self.data.title

    @property
    def type(self):
        return self.data.type


class Image(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Image ({link})".format(link=self.link)

    # str # Full link
    @property
    def link(self):
        return self.data.full

    # str # Group
    @property
    def group(self):
        return self.data.group

    # int # H
    @property
    def h(self):
        return self.data.h

    # str # Sprite
    @property
    def sprite(self):
        return self.data.sprite

    # int # W
    @property
    def w(self):
        return self.data.w

    # int # X
    @property
    def x(self):
        return self.data.x

    # int # Y
    @property
    def y(self):
        return self.data.y


class Passive(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    @property
    def description(self):
        return self.data.description

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    @property
    def name(self):
        return self.data.name

    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription


class ChampionInfo(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Champion Information"

    # int # Attack rating
    @property
    def physical(self):
        return self.data.attack

    # int # Defense rating
    @property
    def defense(self):
        return self.data.defense

    # int # Difficulty rating
    @property
    def difficulty(self):
        return self.data.difficulty

    # int # Magic rating
    @property
    def magic(self):
        return self.data.magic


class Spell(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    # list<Image> # Alternate images
    @cassiopeia.type.core.common.lazyproperty
    def alternate_images(self):
        return [Image(img) for img in self.data.altimages]

    # list<float> # Cooldown
    @property
    def cooldowns(self):
        return self.data.cooldown

    # str # Cooldown burn
    @property
    def cooldown_burn(self):
        return self.data.cooldownBurn

    # list<int> # Cost
    @property
    def costs(self):
        return self.data.cost

    # str # Cost burn
    @property
    def cost_burn(self):
        return self.data.costBurn

    # str # Cost type
    @property
    def cost_type(self):
        return self.data.costType

    # str # Description
    @property
    def description(self):
        return self.data.description

    # list<list<float>> # Effects
    @property
    def effects(self):
        return self.data.effect

    # list<str> # Effect burn
    @property
    def effect_burn(self):
        return self.data.effectBurn

    # Image # Image
    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    # str # Key
    @property
    def key(self):
        return self.data.key

    # LevelTip # Level tip
    @cassiopeia.type.core.common.lazyproperty
    def level_tip(self):
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    # int # Max rank
    @property
    def max_rank(self):
        return self.data.maxrank

    # str # Name
    @property
    def name(self):
        return self.data.name

    # list<int> or "self" # Range
    @property
    def range(self):
        return self.data.range

    # str # Range burn
    @property
    def range_burn(self):
        return self.data.rangeBurn

    # str # Resource
    @property
    def resource(self):
        return self.data.resource

    # str # Sanitized description
    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription

    # str # Sanitized tooltip
    @property
    def sanitized_tooltip(self):
        return self.data.sanitizedTooltip

    # str # Tooltip
    @property
    def tooltip(self):
        return self.data.tooltip

    # list<SpellVariables> # Vars
    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        return [SpellVariables(svars) for svars in self.data.vars]

    def __replace_variables(self, text, level, rank):
        if(level < 1 or level > 18):
            raise ValueError("Not a valid champion level")
        if(rank < 1 or rank > self.max_rank):
            raise ValueError("Not a valid spell rank")

        i = 1
        for effect in self.effects:
            if(effect):
                text = text.replace("{{{{ e{i} }}}}".format(i=i), str(effect[rank - 1]))
                i += 1

        for svar in self.variables:
            val = svar.coefficients[0]
            if(len(svar.coefficients) == self.max_rank):
                val = svar.coefficients[rank - 1]
            elif(svar.coefficients == 18):
                val = svar.coefficients[level - 1]
            replacement = str(val)

            if(svar.link == "attackdamage"):
                replacement = replacement + " AD"
            elif(svar.link == "spelldamage"):
                replacement = replacement + " AP"

            text = text.replace("{{{{ {key} }}}}".format(key=svar.key), replacement)

        return text

    @cassiopeia.type.core.common.immutablemethod
    def tooltip_for_level(self, level, rank):
        return self.__replace_variables(self.tooltip, level, rank)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level, rank):
        return self.__replace_variables(self.sanitized_tooltip, level, rank)


class Champion(cassiopeia.type.core.common.CassiopeiaObject):
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
        return self.data.allytips

    @property
    def blurb(self):
        return self.data.blurb

    @property
    def enemy_tips(self):
        return self.data.enemytips

    @property
    def id(self):
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    @cassiopeia.type.core.common.lazyproperty
    def info(self):
        return ChampionInfo(self.data.info) if self.data.info else None

    @property
    def key(self):
        return self.data.key

    @property
    def lore(self):
        return self.data.lore

    @property
    def name(self):
        return self.data.name

    @property
    def resource(self):
        return self.data.partype

    @cassiopeia.type.core.common.lazyproperty
    def passive(self):
        return Passive(self.data.passive) if self.data.passive else None

    @cassiopeia.type.core.common.lazyproperty
    def recommended_items(self):
        return [RecommendedItems(rec) for rec in self.data.recommended]

    @cassiopeia.type.core.common.lazyproperty
    def skins(self):
        return [Skin(skin) for skin in self.data.skins]

    @cassiopeia.type.core.common.lazyproperty
    def spells(self):
        return [Spell(spell) for spell in self.data.spells]

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        return ChampionStats(self.data.stats) if self.data.stats else None

    @property
    def tags(self):
        return self.data.tags

    @property
    def title(self):
        return self.data.title

##################
# Item Endpoints #
##################

class MetaData(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Meta Data"

    # bool # Is a rune
    @property
    def rune(self):
        return self.data.isRune

    # str # Tier
    @property
    def tier(self):
        return self.data.tier

    # str # Type
    @property
    def type(self):
        return self.data.type


class Gold(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "{price} gold".format(price=self.total)

    # int # Base price
    @property
    def base(self):
        return self.data.base

    # bool # Is purchasable
    @property
    def purchasable(self):
        return self.data.purchasable

    # int # Sell price
    @property
    def sell(self):
        return self.data.sell

    # int # Total price
    @property
    def total(self):
        return self.data.total


class ItemStats(cassiopeia.type.core.common.CassiopeiaObject):
    def __init__(self, data, scraped_stats={}):
        super().__init__(data)
        self.__scraped_stats = scraped_stats

    def __str__(self):
        return "Item Stats"

    @property
    def armor(self):
        return self.data.FlatArmorMod

    @property
    def attack_speed(self):
        return self.data.FlatAttackSpeedMod

    @property
    def block(self):
        return self.data.FlatBlockMod

    @property
    def percent_block(self):
        return self.data.PercentBlockMod

    @property
    def crit_chance(self):
        return self.data.FlatCritChanceMod + self.data.PercentCritChanceMod

    @property
    def crit_damage(self):
        return self.data.FlatCritDamageMod

    @property
    def xp_bonus(self):
        return self.data.FlatEXPBonus

    @property
    def energy(self):
        return self.data.FlatEnergyPoolMod

    @property
    def energy_regen(self):
        return self.data.FlatEnergyRegenMod

    @property
    def health(self):
        return self.data.FlatHPPoolMod

    @property
    def health_regen(self):
        return self.data.FlatHPRegenMod

    @property
    def mana(self):
        return self.data.FlatMPPoolMod

    @property
    def mana_regen(self):
        return self.data.FlatMPRegenMod

    @property
    def ability_power(self):
        return self.data.FlatMagicDamageMod

    @property
    def movespeed(self):
        return self.data.FlatMovementSpeedMod

    @property
    def attack_damage(self):
        return self.data.FlatPhysicalDamageMod

    @property
    def magic_resist(self):
        return self.data.FlatSpellBlockMod

    @property
    def percent_armor(self):
        return self.data.PercentArmorMod

    @property
    def percent_attack_speed(self):
        return self.data.PercentAttackSpeedMod

    @property
    def percent_crit_damage(self):
        return self.data.PercentCritDamageMod

    @property
    def percent_xp_bonus(self):
        return self.data.PercentEXPBonus

    @property
    def percent_health(self):
        return self.data.PercentHPPoolMod

    @property
    def percent_health_regen(self):
        return self.data.PercentHPRegenMod

    @property
    def life_steal(self):
        return self.data.PercentLifeStealMod

    @property
    def percent_mana(self):
        return self.data.PercentMPPoolMod

    @property
    def percent_mana_regen(self):
        return self.data.PercentMPRegenMod

    @property
    def percent_ability_power(self):
        return self.data.PercentMagicDamageMod + self.__scraped_stats.get("percent_ability_power", 0.0)

    @property
    def percent_movespeed(self):
        return self.data.PercentMovementSpeedMod

    @property
    def percent_attack_damage(self):
        return self.data.PercentPhysicalDamageMod

    @property
    def percent_magic_resist(self):
        return self.data.PercentSpellBlockMod

    @property
    def spell_vamp(self):
        return self.data.PercentSpellVampMod

    @property
    def armor_per_level(self):
        return self.data.rFlatArmorModPerLevel

    @property
    def armor_pen(self):
        return self.data.rFlatArmorPenetrationMod + self.__scraped_stats.get("armor_pen", 0.0)

    @property
    def armor_pen_per_level(self):
        return self.data.rFlatArmorPenetrationModPerLevel

    @property
    def crit_chance_per_level(self):
        return self.data.rFlatCritChanceModPerLevel

    @property
    def crit_damage_per_level(self):
        return self.data.rFlatCritDamageModPerLevel

    @property
    def dodge(self):
        return self.data.rFlatDodgeMod + self.data.PercentDodgeMod

    @property
    def dodge_per_level(self):
        return self.data.rFlatDodgeModPerLevel

    @property
    def energy_per_level(self):
        return self.data.rFlatEnergyModPerLevel

    @property
    def energy_regen_per_level(self):
        return self.data.rFlatEnergyRegenModPerLevel

    @property
    def gold_per_ten(self):
        return self.data.rFlatGoldPer10Mod + self.__scraped_stats.get("gold_per_ten", 0.0)

    @property
    def health_per_level(self):
        return self.data.rFlatHPModPerLevel

    @property
    def health_regen_per_level(self):
        return self.data.rFlatHPRegenModPerLevel

    @property
    def mana_per_level(self):
        return self.data.rFlatMPModPerLevel

    @property
    def mana_regen_per_level(self):
        return self.data.rFlatMPRegenModPerLevel

    @property
    def ability_power_per_level(self):
        return self.data.rFlatMagicDamageModPerLevel

    @property
    def magic_pen(self):
        return self.data.rFlatMagicPenetrationMod + self.__scraped_stats.get("magic_pen", 0.0)

    @property
    def magic_pen_per_level(self):
        return self.data.rFlatMagicPenetrationModPerLevel

    @property
    def movespeed_per_level(self):
        return self.data.rFlatMovementSpeedModPerLevel

    @property
    def attack_damage_per_level(self):
        return self.data.rFlatPhysicalDamageModPerLevel

    @property
    def magic_resist_per_level(self):
        return self.data.rFlatSpellBlockModPerLevel

    @property
    def time_dead(self):
        return self.data.rFlatTimeDeadMod

    @property
    def time_dead_per_level(self):
        return self.data.rFlatTimeDeadModPerLevel

    @property
    def percent_armor_pen(self):
        return self.data.rPercentArmorPenetrationMod + self.__scraped_stats.get("percent_armor_pen", 0.0)

    @property
    def percent_armor_pen_per_level(self):
        return self.data.rPercentArmorPenetrationModPerLevel

    @property
    def percent_attack_speed_per_level(self):
        return self.data.rPercentAttackSpeedModPerLevel

    @property
    def cooldown_reduction(self):
        return self.data.rPercentCooldownMod + self.__scraped_stats.get("percent_cooldown_reduction", 0.0)

    @property
    def cooldown_reduction_per_level(self):
        return self.data.rPercentCooldownModPerLevel

    @property
    def percent_magic_pen(self):
        return self.data.rPercentMagicPenetrationMod + self.__scraped_stats.get("percent_magic_pen", 0.0)

    @property
    def percent_magic_pen_per_level(self):
        return self.data.rPercentMagicPenetrationModPerLevel

    @property
    def percent_movespeed_per_level(self):
        return self.data.rPercentMovementSpeedModPerLevel

    @property
    def percent_time_dead(self):
        return self.data.rPercentTimeDeadMod

    @property
    def percent_time_dead_per_level(self):
        return self.data.rPercentTimeDeadModPerLevel


class Item(cassiopeia.type.core.common.CassiopeiaObject):
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
    def colloq(self):
        return self.data.colloq

    @property
    def consume_on_full(self):
        return self.data.consumeOnFull

    @property
    def consumed(self):
        return self.data.consumed

    @property
    def depth(self):
        return self.data.depth

    @property
    def description(self):
        return self.data.description

    @property
    def components(self):
        return self.data.from_

    @cassiopeia.type.core.common.lazyproperty
    def gold(self):
        return Gold(self.data.gold) if self.data.gold else None

    @property
    def group(self):
        return self.data.group

    @property
    def hide_from_all(self):
        return self.data.hide_from_all

    @property
    def id(self):
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    @property
    def in_store(self):
        return self.data.inStore

    @property
    def component_for(self):
        return self.data.into

    @property
    def maps(self):
        return self.data.maps

    @property
    def name(self):
        return self.data.name

    @property
    def plaintext(self):
        return self.data.plaintext

    @property
    def required_champion(self):
        return cassiopeia.riotapi.get_champion_by_name(self.data.requiredChampion) if self.data.requiredChampion else None

    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        return MetaData(self.data.rune) if self.data.rune else None

    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription

    @property
    def special_recipe(self):
        return self.data.specialRecipe

    @property
    def stacks(self):
        return self.data.stacks

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        scraped_stats = {}
        for stat, regex in Item.__stat_patterns.items():
            match = re.search(regex, self.description)
            if(match):
                scraped_stats[stat] = float(match.group(1))
        return ItemStats(self.data.stats, scraped_stats) if self.data.stats else None

    @property
    def tags(self):
        return self.data.tags


class Group(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Group ({key})".format(key=self.key)

    @property
    def max_ownable(self):
        return self.data.MaxGroupOwnable

    @property
    def key(self):
        return self.data.key

################
# Map Endpoint #
################

class MapDetails(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    @property
    def map(self):
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def unpurchasable_items(self):
        return list(filter(None, cassiopeia.riotapi.get_items(self.data.unpurchasableItemList)))

#####################
# Mastery Endpoints #
#####################

class Mastery(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    # list<str> # Description
    @property
    def description(self):
        return self.data.description

    # int # ID
    @property
    def id(self):
        return self.data.id

    # Image # Image
    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    # str # Legal values: Defense, Offense, Utility
    @property
    def tree(self):
        return self.data.masteryTree

    # str # Name
    @property
    def name(self):
        return self.data.name

    # str # Prerequisites
    @property
    def prerequisites(self):
        return self.data.prereq

    # int # Ranks
    @property
    def ranks(self):
        return self.data.ranks

    # list<str> # Sanitized description
    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription

##################
# Realm Endpoint #
##################

class Realm(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return "Realm"

    # str # The base CDN url.
    @property
    def cdn(self):
        return self.data.cdn

    # str # Latest changed version of Dragon Magic's css file.
    @property
    def css(self):
        return self.data.css

    # str # Latest changed version of Dragon Magic.
    @property
    def dragon_magic(self):
        return self.data.dd

    # str # Default language for this realm.
    @property
    def language(self):
        return self.data.l

    # str # Legacy script mode for IE6 or older.
    @property
    def legacy(self):
        return self.data.lg

    # dict<str, str> # Latest changed version for each data type listed.
    @property
    def data_type_versions(self):
        return self.data.n

    # int # Special behavior number identifying the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0
    @property
    def profile_icon_id_max(self):
        return self.data.profileiconmax

    # str # Additional api data drawn from other sources that may be related to data dragon functionality.
    @property
    def store(self):
        return self.data.store

    # str # Current version of this file for this realm.
    @property
    def version(self):
        return self.data.v

##################
# Rune Endpoints #
##################

class Rune(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    # str # Colloq
    @property
    def colloq(self):
        return self.data.colloq

    # bool # Consume on full
    @property
    def consume_on_full(self):
        return self.data.consumeOnFull

    # bool # Consumed
    @property
    def consumed(self):
        return self.data.consumed

    # int # Depth
    @property
    def depth(self):
        return self.data.depth

    # str # Description
    @property
    def description(self):
        return self.data.description

    # list<str> # From
    @property
    def components(self):
        return self.data.from_

    # str # Group
    @property
    def group(self):
        return self.data.group

    # bool # Hide from all
    @property
    def hide_from_all(self):
        return self.data.hideFromAll

    # int # ID
    @property
    def id(self):
        return self.data.id

    # Image # Image
    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    # bool # In store
    @property
    def in_store(self):
        return self.data.inStore

    # list<str> # into
    @property
    def component_for(self):
        return self.data.into

    # dict<str, bool> # Maps
    @property
    def maps(self):
        return self.data.maps

    # str # Name
    @property
    def name(self):
        return self.data.name

    # str # Plain text
    @property
    def plaintext(self):
        return self.data.plaintext

    # Champion # Required champion
    @property
    def required_champion(self):
        return cassiopeia.riotapi.get_champion_by_name(self.data.requiredChampion) if self.data.requiredChampion else None

    # MetaData # Meta Data
    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        return MetaData(self.data.rune) if self.data.rune else None

    # str # Sanitized description
    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription

    # int # Special recipe
    @property
    def special_recipe(self):
        return self.data.specialRecipe

    # int # Stacks
    @property
    def stacks(self):
        return self.data.stacks

    # ItemStats # Stats
    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        return ItemStats(self.data.stats) if self.data.stats else None

    # list<str> # Tags
    @property
    def tags(self):
        return self.data.tags

############################
# Summoner Spell Endpoints #
############################

class SummonerSpell(cassiopeia.type.core.common.CassiopeiaObject):
    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    # list<float> # Cooldown
    @property
    def cooldowns(self):
        return self.data.cooldown

    # str # Cooldown burn
    @property
    def cooldown_burn(self):
        return self.data.cooldownBurn

    # list<int> # Cost
    @property
    def costs(self):
        return self.data.cost

    # str # Cost burn
    @property
    def cost_burn(self):
        return self.data.costBurn

    # str # Cost type
    @property
    def cost_type(self):
        return self.data.costType

    # str # Description
    @property
    def description(self):
        return self.data.description

    # list<list<float>> # Effects
    @property
    def effects(self):
        return self.data.effect

    # list<str> # Effect burn 
    @property
    def effect_burn(self):
        return self.data.effectBurn

    # int # ID
    @property
    def id(self):
        return self.data.id

    # Image # Image
    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        return Image(self.data.image) if self.data.image else None

    # str # Key
    @property
    def key(self):
        return self.data.key

    # LevelTip # Level tip
    @cassiopeia.type.core.common.lazyproperty
    def leveltip(self):
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    # int # Max rank
    @property
    def max_rank(self):
        return self.data.maxrank

    # list<str> # Modes
    @property
    def modes(self):
        return self.data.modes

    # str # Name
    @property
    def name(self):
        return self.data.name

    # list<int> or "self" # Range
    @property
    def range(self):
        return self.data.range

    # str # Range burn
    @property
    def range_burn(self):
        return self.data.rangeBurn

    # str # Resource
    @property
    def resource(self):
        return self.data.resource

    # str # Sanitized description
    @property
    def sanitized_description(self):
        return self.data.sanitizedDescription

    # str # Sanitized tooltip
    @property
    def sanitized_tooltip(self):
        return self.data.sanitizedTooltip

    # int # Summoner level
    @property
    def summoner_level(self):
        return self.data.summonerLevel

    # str # Tooltip
    @property
    def tooltip(self):
        return self.data.tooltip

    # list<SpellVariables> # Vars
    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        return [SpellVariables(svars) for svars in self.data.vars]

    def __replace_variables(self, text, level):
        if(level < 1 or level > 18):
            raise ValueError("Not a valid champion level")

        for svar in self.variables:
            val = svar.coefficients[level - 1] if svar.link == "@player.level" else svar.coefficients[0]
            print("REPLACING " + "{{{{{key}}}}}".format(key=svar.key) + " WITH " + str(val))
            text = text.replace("{{{{ {key} }}}}".format(key=svar.key), str(val))

        return text

    @cassiopeia.type.core.common.immutablemethod
    def tooltip_for_level(self, level):
        return self.__replace_variables(self.tooltip, level)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level):
        return self.__replace_variables(self.sanitized_tooltip, level)