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
        """
        Returns:
            int: how many of this item are in the block
        """
        return self.data.count

    @property
    def item(self):
        """
        Returns:
            Item: the item itself
        """
        return cassiopeia.riotapi.get_item(self.data.id)


@cassiopeia.type.core.common.inheritdocs
class Item(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Item

    __stat_patterns = {
        "percent_base_attack_damage": "\\+(\\d+)% Base Attack Damage",
        "percent_cooldown_reduction": "\\+(\\d+) *% Cooldown Reduction",
        "armor_pen": "\\+(\\d+) <a href='FlatArmorPen'>Armor Penetration</a>",
        "percent_bonus_armor_pen": "\\+(\\d+)% <a href='BonusArmorPen'>Bonus Armor Penetration</a>",
        "magic_pen": "\\+(\\d+) <a href='FlatMagicPen'>Magic Penetration</a>",
        "percent_magic_pen": "\\+(\\d+)% <a href='TotalMagicPen'>Magic Penetration</a>",
        "gold_per_ten": "\\+(\\d+) *Gold per 10 seconds",
        "percent_ability_power": "Increases Ability Power by (\\d+)%",
        "life_steal": "(?:Dealing physical damage heals for (\\d+)% of the damage dealt)|(?:\\+(\\d+)% Life Steal)",
        "spell_vamp": "(?:\\+(\\d+)% <a href='SpellVamp'>Spell Vamp</a>)|(?:Your spells and abilities heal you for (\\d+)% of the damage dealt)",
        "percent_base_mana_regen": "\\+(\\d+)% Base Mana Regen",
        "percent_base_health_regen": "\\+(\\d+)% Base Health Regen",
        "percent_bonus_health": "\\+(\\d+)% Bonus Health",
        "percent_movespeed": "\\+(\\d+)% Movement Speed",
        "tenacity": "Tenacity:</unique> Reduces the duration of stuns, slows, taunts, fears, silences, blinds, polymorphs, and immobilizes by (\\d+)%"
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
        """
        Returns:
            str: a string formatted list of search keywords for this item in the shop
        """
        return self.data.colloq

    @property
    def consume_on_full(self):
        """
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.consumeOnFull

    @property
    def consumable(self):
        """
        Returns:
            bool: whether the item is a consumable
        """
        return self.data.consumed

    @property
    def tier(self):
        """
        Returns:
            str: what tier the item is
        """
        return self.data.depth

    @property
    def description(self):
        """
        Returns:
            str: the description of the item
        """
        return self.data.description

    @property
    def effect(self):
        """
        Returns:
            dict<str, bool>: the item's effects
        """
        return self.data.effect

    @property
    def components(self):
        """
        Returns:
            list<Item>: the components for this item
        """
        return cassiopeia.riotapi.get_items([int(id_) for id_ in self.data.from_])

    @cassiopeia.type.core.common.lazyproperty
    def gold(self):
        """
        Returns:
            Gold: price information for this item
        """
        return Gold(self.data.gold) if self.data.gold else None

    @property
    def group(self):
        """
        Returns:
            str: the group for this item
        """
        return self.data.group

    @property
    def hide(self):
        """
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.hide_from_all

    @property
    def id(self):
        """
        Returns:
            int: the ID of this item
        """
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this item
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def in_store(self):
        """
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.inStore

    @property
    def component_of(self):
        """
        Returns:
            list<Item>: the items this one is a component of
        """
        return cassiopeia.riotapi.get_items([int(id_) for id_ in self.data.into])

    @property
    def maps(self):
        """
        Returns:
            dict<Map, bool>: a listing of whether this item is available on each map
        """
        return {cassiopeia.type.core.common.Map(int(id_)): allowed for id_, allowed in self.data.maps.items()}

    @property
    def name(self):
        """
        Returns:
            str: the name of this item
        """
        return self.data.name

    @property
    def blurb(self):
        """
        Returns:
            str: the blurb for this item
        """
        return self.data.plaintext

    @property
    def required_champion(self):
        """
        Returns:
            Champion: the required champion for this item
        """
        return cassiopeia.riotapi.get_champion_by_name(self.data.requiredChampion) if self.data.requiredChampion else None

    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        """
        Returns:
            MetaData: meta data about this item
        """
        return MetaData(self.data.rune) if self.data.rune else None

    @property
    def sanitized_description(self):
        """
        Returns:
            str: the sanitized description of this item
        """
        return self.data.sanitizedDescription

    @property
    def special_recipe(self):
        """
        Returns:
            int: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.specialRecipe

    @property
    def stacks(self):
        """
        Returns:
            int: the number of stacks this item can have
        """
        return self.data.stacks

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            ItemStats: the stats for this item
        """
        scraped_stats = {}
        for stat, regex in Item.__stat_patterns.items():
            match = re.search(regex, self.description)
            if match:
                value = [match.group(i) for i in range(1, re.compile(regex).groups + 1) if match.group(i) is not None]
                value = sum([float(v) for v in value])
                scraped_stats[stat] = value
        if scraped_stats and self.data.stats is None:
            self.data.stats = cassiopeia.type.dto.staticdata.BasicDataStats({})
        return ItemStats(self.data.stats, scraped_stats) if self.data.stats else None

    @property
    def tags(self):
        """
        Returns:
            list<str>: this item's tags for sorting items
        """
        return self.data.tags

    # Left out these: attack_range, percent_time_dead, percent_time_dead_per_level, time_dead, time_dead_per_level, gold_per_ten, starting_gold, percent_xp_bonus, xp_bonus
    __item_categories = {
        "Defense": {
            "Health": ["base_health", "health", "percent_health", "percent_bonus_health", "health_regen", "base_health_regen", "health_regen_per_level", "bonus_health_regen", "percent_health_regen", "percent_base_health_regen", "health_per_level", "base_health_regen", "bonus_health"],
            "Armor": ["armor", "bonus_armor", "armor_per_level", "base_armor", "percent_armor"],
            "Magic Resist": ["magic_resist_per_level", "base_magic_resist", "magic_resist", "percent_magic_resist", "bonus_magic_resist"],
            "Tenacity": ["tenacity"],
            "Other": ["dodge_chance", "dodge_chance_per_level", "block", "percent_block", "tenacity"]
        },
        "Attack": {
            "Damage": ["bonus_attack_damage", "attack_damage", "base_attack_damage", "percent_attack_damage", "percent_total_damage_increase", "attack_damage_per_level"],
            "Critical Strike": ["percent_critical_strike_damage", "critical_strike_chance_per_level", "critical_strike_damage", "critical_strike_damage_per_level", "critical_strike_chance", "critical_strike_chance_per_level"],
            "Attack Speed": ["percent_attack_speed", "attack_speed", "bonus_attack_speed", "attack_speed_per_level", "base_attack_speed", "percent_attack_speed_per_level"],
            "Life Steal": ["life_steal"],
            "Other": ["armor_penetration", "percent_armor_penetration", "percent_bonus_armor_penetration", "armor_penetration_per_level", "percent_armor_penetration_per_level", "magic_penetration", "percent_magic_penetration", "magic_penetration_per_level", "percent_magic_pen_per_level"]
        },
        "Magic": {
            "Ability Power": ["ability_power", "ability_power_per_level", "percent_ability_power"],
            "Cooldown Reduction": ["item_cooldown_reduction", "cooldown_reduction_per_level", "cooldown_reduction"],
            "Spell Vamp": ["spell_vamp"],
            "Mana": ["base_mana", "bonus_mana", "energy_per_level", "energy", "mana_per_level", "mana", "percent_mana", "base_mana_regen"],
            "Mana Regen": ["base_mana_regen", "bonus_mana_regen", "mana_regen_per_level", "percent_mana_regen", "percent_base_mana_regen", "mana_regen", "energy_regen", "energy_regen_per_level"],
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
        """
        Returns:
            list<str>: the shop categories that this item belongs to
        """
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
        """
        Returns:
            list<SetItem>: the items in this item set
        """
        return [SetItem(item) for item in self.data.items]

    @property
    def rec_math(self):
        """
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
        """
        return self.data.recMath

    @property
    def type(self):
        """
        Returns:
            str: what type the item set is (e.g. starting items)
        """
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class SpellVariables(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.SpellVars

    def __str__(self):
        return "Spell Variables"

    @property
    def coefficients(self):
        """
        Returns:
            list<float>: the coefficients for determining spell scaling
        """
        return self.data.coeff

    @property
    def dynamic(self):
        """
        Returns:
            str: whether the spell variables are dynamic
        """
        return self.data.dyn

    @property
    def key(self):
        """
        Returns:
            str: this spell's identifying key
        """
        return self.data.key

    @property
    def link(self):
        """
        Returns:
            str: the link to the image. See https://developer.riotgames.com/docs/static-data for more information.
        """
        return self.data.link

    @property
    def ranks_with(self):
        """
        Returns:
            str: what these variables rank with
        """
        return self.data.ranksWith


@cassiopeia.type.core.common.inheritdocs
class LevelTip(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.LevelTip

    def __str__(self):
        return "Level Tip"

    @property
    def effects(self):
        """
        Returns:
            list<list<float>>: the level-by-level replacements for {{ e# }} tags in other values
        """
        return self.data.effect

    @property
    def labels(self):
        """
        Returns:
            list<str>: the labels for the changes in effects
        """
        return self.data.label


@cassiopeia.type.core.common.inheritdocs
class ChampionStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Stats

    def __str__(self):
        return "Champion Stats"

    @property
    def armor(self):
        """
        Returns:
            float: armor
        """
        return self.data.armor

    @property
    def armor_per_level(self):
        """
        Returns:
            float: armor per level
        """
        return self.data.armorperlevel

    @property
    def attack_damage(self):
        """
        Returns:
            float: attack damage
        """
        return self.data.attackdamage

    @property
    def attack_damage_per_level(self):
        """
        Returns:
            float: attack damage per level
        """
        return self.data.attackdamageperlevel

    @property
    def attack_range(self):
        """
        Returns:
            float: attack range
        """
        return self.data.attackrange

    @property
    def attack_speed(self):
        """
        Returns:
            float: attack speed
        """
        return 0.625 / (1.0 + self.data.attackspeedoffset)

    @property
    def percent_attack_speed_per_level(self):
        """
        Returns:
            float: attack speed per level
        """
        return self.data.attackspeedperlevel / 100

    @property
    def critical_strike_chance(self):
        """
        Returns:
            float: crititical strike chance
        """
        return self.data.crit

    @property
    def critical_strike_chance_per_level(self):
        """
        Returns:
            float: crititical strike chance per level
        """
        return self.data.critperlevel

    @property
    def health(self):
        """
        Returns:
            float: health
        """
        return self.data.hp

    @property
    def health_per_level(self):
        """
        Returns:
            float: health per level
        """
        return self.data.hpperlevel

    @property
    def health_regen(self):
        """
        Returns:
            float: health regen
        """
        return self.data.hpregen

    @property
    def health_regen_per_level(self):
        """
        Returns:
            float: health regen per level
        """
        return self.data.hpregenperlevel

    @property
    def movespeed(self):
        """
        Returns:
            float: movespeed
        """
        return self.data.movespeed

    @property
    def mana(self):
        """
        Returns:
            float: mana
        """
        return self.data.mp

    @property
    def mana_per_level(self):
        """
        Returns:
            float: mana per level
        """
        return self.data.mpperlevel

    @property
    def mana_regen(self):
        """
        Returns:
            float: mana regen
        """
        return self.data.mpregen

    @property
    def mana_regen_per_level(self):
        """
        Returns:
            float: mana regen per level
        """
        return self.data.mpregenperlevel

    @property
    def magic_resist(self):
        """
        Returns:
            float: magic resist
        """
        return self.data.spellblock

    @property
    def magic_resist_per_level(self):
        """
        Returns:
            float: magic resist per level
        """
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
        """
        Returns:
            str: the link to the splash art for this skin
        """
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/splash/{0}_{1}.jpg".format(self.__key, self.number)

    @property
    def loading(self):
        """
        Returns:
            str: the link to the loading art for this skin
        """
        return "http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{0}_{1}.jpg".format(self.__key, self.number)

    @property
    def id(self):
        """
        Returns:
            int: the ID of this skin
        """
        return self.data.id

    @property
    def name(self):
        """
        Returns:
            str: the name of this skin
        """
        return self.data.name

    @property
    def number(self):
        """
        Returns:
            int: where in the skin order this skin comes
        """
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
        """
        Returns:
            list<ItemSet>: the sets of items that make up this reommended page
        """
        return [ItemSet(block) for block in self.data.blocks]

    @property
    def champion(self):
        """
        Returns:
            Champion: the champion these recommendations are for
        """
        return cassiopeia.riotapi.get_champion_by_name(self.data.champion) if self.data.champion else None

    @property
    def map(self):
        """
        Returns:
            str: the name of the map these recommendations are for
        """
        return self.data.map

    @property
    def mode(self):
        """
        Returns:
            GameMode: the game mode these recommendations are for
        """
        return cassiopeia.type.core.common.GameMode(self.data.mode) if self.data.mode else None

    @property
    def priority(self):
        """
        Returns:
            bool: whether this is a priority recommendation
        """
        return self.data.priority

    @property
    def name(self):
        """
        Returns:
            str: the name of this item
        """
        return self.data.title

    @property
    def type(self):
        """
        Returns:
            str: the type of recommended items
        """
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class Image(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Image

    def __str__(self):
        return "Image ({link})".format(link=self.link)

    @property
    def link(self):
        """
        Returns:
            str: the link to the image. See https://developer.riotgames.com/docs/static-data for more information.
        """
        return self.data.full

    @property
    def group(self):
        """
        Returns:
            int: how many of this item are in the block
        """
        return self.data.group

    @property
    def height(self):
        """
        Returns:
            int: the height of the image
        """
        return self.data.h

    @property
    def sprite(self):
        """
        Returns:
            str: the sprite image link. See https://developer.riotgames.com/docs/static-data for more information.
        """
        return self.data.sprite

    @property
    def width(self):
        """
        Returns:
            int: the width of the image
        """
        return self.data.w

    @property
    def x(self):
        """
        Returns:
            int: the x offset of the image
        """
        return self.data.x

    @property
    def y(self):
        """
        Returns:
            int: the y offset of the image
        """
        return self.data.y


@cassiopeia.type.core.common.inheritdocs
class Passive(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Passive

    def __str__(self):
        return self.name

    @property
    def description(self):
        """
        Returns:
            str: the description of the passive
        """
        return self.data.description

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this passive
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def name(self):
        """
        Returns:
            str: the name of this passive
        """
        return self.data.name

    @property
    def sanitized_description(self):
        """
        Returns:
            str: the sanitized description of this passive
        """
        return self.data.sanitizedDescription


@cassiopeia.type.core.common.inheritdocs
class ChampionInfo(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Info

    def __str__(self):
        return "Champion Information"

    @property
    def physical(self):
        """
        Returns:
            int: physical damage output rating (out of 10)
        """
        return self.data.attack

    @property
    def defense(self):
        """
        Returns:
            int: defensive rating (out of 10)
        """
        return self.data.defense

    @property
    def difficulty(self):
        """
        Returns:
            int: difficulty rating (out of 10)
        """
        return self.data.difficulty

    @property
    def magic(self):
        """
        Returns:
            int: magic damage output rating (out of 10)
        """
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
        """
        Returns:
            list<Image>: the alternate images for this spell
        """
        return [Image(img) for img in self.data.altimages]

    @property
    def cooldowns(self):
        """
        Returns:
            list<float>: the cooldowns of this spell level-by-level
        """
        return self.data.cooldown

    @property
    def cooldown_burn(self):
        """
        Returns:
            str: a string formatted list of the spell's cooldowns by level
        """
        return self.data.cooldownBurn

    @property
    def costs(self):
        """
        Returns:
            list<int>: the cost of the spell level-by-level
        """
        return self.data.cost

    @property
    def cost_burn(self):
        """
        Returns:
            str: a string formatted list of the spell's cost by level
        """
        return self.data.costBurn

    @property
    def cost_type(self):
        """
        Returns:
            str: what the spell costs to use (e.g. mana or energy)
        """
        return self.data.costType

    @property
    def description(self):
        """
        Returns:
            str: the description of the spell
        """
        return self.data.description

    @property
    def effects(self):
        """
        Returns:
            list<list<float>>: the level-by-level replacements for {{ e# }} tags in other values
        """
        return self.data.effect

    @property
    def effect_burn(self):
        """
        Returns:
            list<str>: the string formatted replacements for {{ e# }} tags in other values by level
        """
        return self.data.effectBurn

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this spell
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def key(self):
        """
        Returns:
            str: this spell's identifying key
        """
        return self.data.key

    @cassiopeia.type.core.common.lazyproperty
    def level_tip(self):
        """
        Returns:
            LevelTip: the level-up tips for this spell
        """
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    @property
    def max_rank(self):
        """
        Returns:
            int: the maximum level for this spell
        """
        return self.data.maxrank

    @property
    def name(self):
        """
        Returns:
            str: the name of this spell
        """
        return self.data.name

    @property
    def range(self):
        """
        Returns:
            self | list<int>: the level-by-level range of this spell
        """
        return self.data.range

    @property
    def range_burn(self):
        """
        Returns:
            str: the string formatted range of this spell by level
        """
        return self.data.rangeBurn

    @property
    def resource(self):
        """
        Returns:
            str: what resource this spell uses
        """
        return self.data.resource

    @property
    def sanitized_description(self):
        """
        Returns:
            str: the sanitized description of this spell
        """
        return self.data.sanitizedDescription

    @property
    def sanitized_tooltip(self):
        """
        Returns:
            str: the sanitized tooltip for this spell
        """
        return self.data.sanitizedTooltip

    @property
    def tooltip(self):
        """
        Returns:
            str: the tooltip for this spell
        """
        return self.data.tooltip

    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        """
        Returns:
            SpellVariables: the variables that determine this spell's damage
        """
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

        Args:
            level (int): the level of the champion
            rank (int): the rank of this spell

        Returns:
            int: how many of this item are in the block
        """
        return self.__replace_variables(self.tooltip, level, rank)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level, rank):
        """Gets the sanitized tooltip for this spell for a specific level/rank

        Args:
            level (int): the level of the champion
            rank (int): the rank of this spell

        Returns:
            str: the sanitized tooltip for this spell for the specified level and rank
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
        """
        Returns:
            list<str>: the set of tips for allies of this champion
        """
        return self.data.allytips

    @property
    def blurb(self):
        """
        Returns:
            list<SetItem>: the items in this item set
        """
        return self.data.blurb

    @property
    def enemy_tips(self):
        """
        Returns:
            list<str>: the set of tips for enemies of this champion
        """
        return self.data.enemytips

    @property
    def id(self):
        """
        Returns:
            int: the ID of this champion
        """
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this champion
        """
        return Image(self.data.image) if self.data.image else None

    @cassiopeia.type.core.common.lazyproperty
    def info(self):
        """
        Returns:
            ChampionInfo: ratings of what this champion is good/bad at
        """
        return ChampionInfo(self.data.info) if self.data.info else None

    @property
    def key(self):
        """
        Returns:
            str: this champion's identifying key
        """
        return self.data.key

    @property
    def lore(self):
        """
        Returns:
            str: this champion's lore
        """
        return self.data.lore

    @property
    def name(self):
        """
        Returns:
            str: the name of this champion
        """
        return self.data.name

    @property
    def resource(self):
        """
        Returns:
            list<SetItem>: the items in this item set
        """
        return self.data.partype

    @cassiopeia.type.core.common.lazyproperty
    def passive(self):
        """
        Returns:
            Passive: this champion's passive
        """
        return Passive(self.data.passive) if self.data.passive else None

    @cassiopeia.type.core.common.lazyproperty
    def recommended_items(self):
        """
        Returns:
            list<RecommendedItems>: item recommendations for this champion
        """
        return [RecommendedItems(rec) for rec in self.data.recommended]

    @cassiopeia.type.core.common.lazyproperty
    def skins(self):
        """
        Returns:
            list<Skin>: this champion's skins
        """
        return [Skin(skin, self.key) for skin in self.data.skins]

    @cassiopeia.type.core.common.lazyproperty
    def spells(self):
        """
        Returns:
            list<Spell>: this champion's spells
        """
        return [Spell(spell) for spell in self.data.spells]

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            ChampionStats: the stats for this champion
        """
        return ChampionStats(self.data.stats) if self.data.stats else None

    @property
    def tags(self):
        """
        Returns:
            list<str>: this champions's tags for sorting champions
        """
        return self.data.tags

    @property
    def title(self):
        """
        Returns:
            str: this champion's title
        """
        return self.data.title

    @cassiopeia.type.core.common.immutablemethod
    def status(self):
        """
        Returns:
            list<SetItem>: the items in this item set
        """
        return cassiopeia.riotapi.get_champion_status(self)

    @cassiopeia.type.core.common.immutablemethod
    def mastery_level(self, summoner):
        """Gets the ChampionMastery object for the specified summoner
        Args:
            summoner (Summoner): the summoner to get champion mastery for
        Returns:
            bool: well, we don't know what this one is. let us know if you figure it out.
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
        """
        Returns:
            bool: whether the item is a rune
        """
        return self.data.isRune

    @property
    def tier(self):
        """
        Returns:
            str: what tier the item is
        """
        return self.data.tier

    @property
    def type(self):
        """
        Returns:
            str: the type of meta data
        """
        return self.data.type


@cassiopeia.type.core.common.inheritdocs
class Gold(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.Gold

    def __str__(self):
        return "{price} gold".format(price=self.total)

    @property
    def base(self):
        """
        Returns:
            int: the base price of the item
        """
        return self.data.base

    @property
    def purchasable(self):
        """
        Returns:
            bool: whether the item can be bought
        """
        return self.data.purchasable

    @property
    def sell(self):
        """
        Returns:
            int: the sell price of the item
        """
        return self.data.sell

    @property
    def total(self):
        """
        Returns:
            int: the total price of the item
        """
        return self.data.total


@cassiopeia.type.core.common.inheritdocs
class ItemStats(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.staticdata.BasicDataStats

    __stats = set()
    for tag, tags in Item._Item__item_categories.items():
        for tag, stats in tags.items():
            for stat in stats:
                __stats.add(stat)

    def __init__(self, data, scraped_stats={}):
        super().__init__(data)
        for k, v in scraped_stats.items():
            if ("percent" in k or "spell_vamp" in k or "life_steal" in k or "tenacity" in k) and v > 1.0:
                scraped_stats[k] = v / 100.0
        self.__scraped_stats = scraped_stats

    def __str__(self):
        stats = {}
        for stat in ItemStats._ItemStats__stats:
            value = getattr(self, stat, 0.0)
            if value != 0.0:
                stats[stat] = value
        return str(stats)

    @property
    def armor(self):
        """
        Returns:
            float: armor
        """
        return self.data.FlatArmorMod

    @property
    def attack_speed(self):
        """
        Returns:
            float: attack speed
        """
        return self.data.FlatAttackSpeedMod

    @property
    def block(self):
        """
        Returns:
            float: blocked damage per attack
        """
        return self.data.FlatBlockMod

    @property
    def percent_block(self):
        """
        Returns:
            float: percent blocked damage per attack
        """
        return self.data.PercentBlockMod

    @property
    def critical_strike_chance(self):
        """
        Returns:
            float: critical strike chance
        """
        return self.data.FlatCritChanceMod + self.data.PercentCritChanceMod

    @property
    def critical_strike_damage(self):
        """
        Returns:
            float: critical strike damage modification
        """
        return self.data.FlatCritDamageMod

    @property
    def xp_bonus(self):
        """
        Returns:
            float: experience bonus
        """
        return self.data.FlatEXPBonus

    @property
    def energy(self):
        """
        Returns:
            float: energy
        """
        return self.data.FlatEnergyPoolMod

    @property
    def energy_regen(self):
        """
        Returns:
            float: energy regen
        """
        return self.data.FlatEnergyRegenMod

    @property
    def health(self):
        """
        Returns:
            flaot: health
        """
        return self.data.FlatHPPoolMod

    @property
    def health_regen(self):
        """
        Returns:
            float: health regen
        """
        return self.data.FlatHPRegenMod

    @property
    def mana(self):
        """
        Returns:
            float: mana
        """
        return self.data.FlatMPPoolMod

    @property
    def mana_regen(self):
        """
        Returns:
            float mana regen
        """
        return self.data.FlatMPRegenMod

    @property
    def ability_power(self):
        """
        Returns:
            float: ability power
        """
        return self.data.FlatMagicDamageMod

    @property
    def movespeed(self):
        """
        Returns:
            float: movespeed
        """
        return self.data.FlatMovementSpeedMod

    @property
    def attack_damage(self):
        """
        Returns:
            float: attack damage
        """
        return self.data.FlatPhysicalDamageMod

    @property
    def magic_resist(self):
        """
        Returns:
            float: magic resist
        """
        return self.data.FlatSpellBlockMod

    @property
    def tenacity(self):
        """
        Returns:
            float: tenacity
        """
        return self.__scraped_stats.get("tenacity", 0.0)

    @property
    def percent_armor(self):
        """
        Returns:
            float: percent armor
        """
        return self.data.PercentArmorMod

    @property
    def percent_attack_speed(self):
        """
        Returns:
            float: percent attack speed
        """
        return self.data.PercentAttackSpeedMod

    @property
    def percent_critical_strike_damage(self):
        """
        Returns:
            float: percent critical strike damage modification
        """
        return self.data.PercentCritDamageMod

    @property
    def percent_xp_bonus(self):
        """
        Returns:
            float: percent experience bonus
        """
        return self.data.PercentEXPBonus

    @property
    def percent_health(self):
        """
        Returns:
            float: percent health
        """
        return self.data.PercentHPPoolMod

    @property
    def percent_bonus_health(self):
        """
        Returns:
            float: percent bonus health
        """
        return self.__scraped_stats.get("percent_bonus_health", 0.0)

    @property
    def percent_health_regen(self):
        """
        Returns:
            float: percent health regen
        """
        return self.data.PercentHPRegenMod

    @property
    def percent_base_health_regen(self):
        """
        Returns:
            float: percent base health regen
        """
        return self.__scraped_stats.get("percent_base_health_regen", 0.0)

    @property
    def life_steal(self):
        """
        Returns:
            float: life steal
        """
        return self.data.PercentLifeStealMod + self.__scraped_stats.get("life_steal", 0.0)

    @property
    def percent_mana(self):
        """
        Returns:
            float: percent mana
        """
        return self.data.PercentMPPoolMod

    @property
    def percent_mana_regen(self):
        """
        Returns:
            float: percent mana regen
        """
        return self.data.PercentMPRegenMod

    @property
    def percent_base_mana_regen(self):
        """
        Returns:
            float: percent base mana regen
        """
        return self.__scraped_stats.get("base_mana_regen", 0.0) + self.__scraped_stats.get("percent_base_mana_regen", 0.0)

    @property
    def percent_ability_power(self):
        """
        Returns:
            float: percent ability power
        """
        return self.data.PercentMagicDamageMod + self.__scraped_stats.get("percent_ability_power", 0.0)

    @property
    def percent_movespeed(self):
        """
        Returns:
            float: percent movespeed
        """
        return self.data.PercentMovementSpeedMod + self.__scraped_stats.get("percent_movespeed", 0.0)

    @property
    def percent_attack_damage(self):
        """
        Returns:
            float: percent attack damage
        """
        return self.data.PercentPhysicalDamageMod

    @property
    def percent_base_attack_damage(self):
        """
        Returns:
            float: percent attack damage
        """
        return self.__scraped_stats.get("percent_base_attack_damage", 0.0)

    @property
    def percent_magic_resist(self):
        """
        Returns:
            float: percent magic resist
        """
        return self.data.PercentSpellBlockMod

    @property
    def spell_vamp(self):
        """
        Returns:
            float: spell vamp
        """
        return self.data.PercentSpellVampMod + self.__scraped_stats.get("spell_vamp", 0.0)

    @property
    def armor_per_level(self):
        """
        Returns:
            float: armor per level
        """
        return self.data.rFlatArmorModPerLevel

    @property
    def armor_penetration(self):
        """
        Returns:
            float: armor penetration
        """
        return self.data.rFlatArmorPenetrationMod + self.__scraped_stats.get("armor_pen", 0.0)

    @property
    def armor_penetration_per_level(self):
        """
        Returns:
            float: armor penetration per level
        """
        return self.data.rFlatArmorPenetrationModPerLevel

    @property
    def critical_strike_chance_per_level(self):
        """
        Returns:
            float: critical strike chance per level
        """
        return self.data.rFlatCritChanceModPerLevel

    @property
    def critical_strike_damage_per_level(self):
        """
        Returns:
            float: critical strike damage per level
        """
        return self.data.rFlatCritDamageModPerLevel

    @property
    def dodge_chance(self):
        """
        Returns:
            float: dodge chance
        """
        return self.data.rFlatDodgeMod + self.data.PercentDodgeMod

    @property
    def dodge_chance_per_level(self):
        """
        Returns:
            float: dodge change per level
        """
        return self.data.rFlatDodgeModPerLevel

    @property
    def energy_per_level(self):
        """
        Returns:
            float: energy per level
        """
        return self.data.rFlatEnergyModPerLevel

    @property
    def energy_regen_per_level(self):
        """
        Returns:
            float: energy regen per level
        """
        return self.data.rFlatEnergyRegenModPerLevel

    @property
    def gold_per_ten(self):
        """
        Returns:
            float: gold per 10 seconds
        """
        return self.data.rFlatGoldPer10Mod + self.__scraped_stats.get("gold_per_ten", 0.0)

    @property
    def health_per_level(self):
        """
        Returns:
            float: health per level
        """
        return self.data.rFlatHPModPerLevel

    @property
    def health_regen_per_level(self):
        """
        Returns:
            float: health regen per level
        """
        return self.data.rFlatHPRegenModPerLevel

    @property
    def mana_per_level(self):
        """
        Returns:
            float: armor per level
        """
        return self.data.rFlatMPModPerLevel

    @property
    def mana_regen_per_level(self):
        """
        Returns:
            float: mana regen per level
        """
        return self.data.rFlatMPRegenModPerLevel

    @property
    def ability_power_per_level(self):
        """
        Returns:
            float: ability power per level
        """
        return self.data.rFlatMagicDamageModPerLevel

    @property
    def magic_penetration(self):
        """
        Returns:
            float: magic penetration
        """
        return self.data.rFlatMagicPenetrationMod + self.__scraped_stats.get("magic_pen", 0.0)

    @property
    def magic_penetration_per_level(self):
        """
        Returns:
            float: magic penetration per level
        """
        return self.data.rFlatMagicPenetrationModPerLevel

    @property
    def movespeed_per_level(self):
        """
        Returns:
            float: movespeed per level
        """
        return self.data.rFlatMovementSpeedModPerLevel

    @property
    def attack_damage_per_level(self):
        """
        Returns:
            float attack damage per level
        """
        return self.data.rFlatPhysicalDamageModPerLevel

    @property
    def magic_resist_per_level(self):
        """
        Returns:
            float: magic resist per level
        """
        return self.data.rFlatSpellBlockModPerLevel

    @property
    def time_dead(self):
        """
        Returns:
            float: time dead modification
        """
        return abs(self.data.rFlatTimeDeadMod)

    @property
    def time_dead_per_level(self):
        """
        Returns:
            float: time dead modification per level
        """
        return abs(self.data.rFlatTimeDeadModPerLevel)

    @property
    def percent_armor_penetration(self):
        """
        Returns:
            float: percent armor pentration
        """
        return self.data.rPercentArmorPenetrationMod + self.__scraped_stats.get("percent_armor_pen", 0.0)

    @property
    def percent_armor_penetration_per_level(self):
        """
        Returns:
            float: percent armor penetration per level
        """
        return self.data.rPercentArmorPenetrationModPerLevel

    @property
    def percent_bonus_armor_penetration(self):
        """
        Returns:
            float: percent armor pentration
        """
        return self.__scraped_stats.get("percent_bonus_armor_pen", 0.0)

    @property
    def percent_attack_speed_per_level(self):
        """
        Returns:
            float: percent attack speed per level
        """
        return self.data.rPercentAttackSpeedModPerLevel

    @property
    def cooldown_reduction(self):
        """
        Returns:
            float: cooldown reduction
        """
        return abs(self.data.rPercentCooldownMod + self.__scraped_stats.get("percent_cooldown_reduction", 0.0))

    @property
    def cooldown_reduction_per_level(self):
        """
        Returns:
            float: cooldown reduction per level
        """
        return abs(self.data.rPercentCooldownModPerLevel)

    @property
    def percent_magic_penetration(self):
        """
        Returns:
            float: percent magic penetration
        """
        return self.data.rPercentMagicPenetrationMod + self.__scraped_stats.get("percent_magic_pen", 0.0)

    @property
    def percent_magic_pen_per_level(self):
        """
        Returns:
            float: percent magic penetration per level
        """
        return self.data.rPercentMagicPenetrationModPerLevel

    @property
    def percent_movespeed_per_level(self):
        """
        Returns:
            float: percent movespeed per level
        """
        return self.data.rPercentMovementSpeedModPerLevel

    @property
    def percent_time_dead(self):
        """
        Returns:
            float: percent time dead modification
        """
        return abs(self.data.rPercentTimeDeadMod)

    @property
    def percent_time_dead_per_level(self):
        """
        Returns:
            float: percent time dead modification per level
        """
        return abs(self.data.rPercentTimeDeadModPerLevel)


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
        """
        Returns:
            Image: the image of this map
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def map_id(self):
        """
        Returns:
            int: the ID of this map
        """
        return self.data.mapId

    @property
    def map(self):
        """
        Returns:
            Map: the type of this map
        """
        return cassiopeia.type.core.common.Map(self.data.mapId) if self.data.mapId else None

    @cassiopeia.type.core.common.lazyproperty
    def unpurchasable_items(self):
        """
        Returns:
            list<Item>: the items that can't be bought on this map
        """
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
        """
        Returns:
            list<str>: descriptions of this mastery by rank
        """
        return self.data.description

    @property
    def id(self):
        """
        Returns:
            int: the ID of this mastery
        """
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this mastery
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def tree(self):
        """
        Returns:
            str: which mastery tree this mastery belongs to
        """
        return cassiopeia.type.core.common.MasteryType(self.data.masteryTree)

    @property
    def name(self):
        """
        Returns:
            str: the name of this mastery
        """
        return self.data.name.strip()

    @property
    def prerequisite(self):
        """
        Returns:
            Mastery: the prerequisite for this mastery
        """
        return cassiopeia.riotapi.get_mastery(int(self.data.prereq)) if int(self.data.prereq) else None

    @property
    def max_rank(self):
        """
        Returns:
            int: the max rank for this mastery
        """
        return self.data.ranks

    @property
    def sanitized_descriptions(self):
        """
        Returns:
            list<str>: sanitized descriptions of this mastery by rank
        """
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
        """
        Returns:
            str: the base CDN url
        """
        return self.data.cdn

    @property
    def css(self):
        """
        Returns:
            str: the latest version of the Dragon Magic's css file
        """
        return self.data.css

    @property
    def dragon_magic(self):
        """
        Returns:
            str: the lastest version of Dragon Magic
        """
        return self.data.dd

    @property
    def language(self):
        """
        Returns:
            str: the default locale for this realm
        """
        return self.data.l

    @property
    def legacy(self):
        """
        Returns:
            str: the legacy script mode for IE6 or older
        """
        return self.data.lg

    @property
    def data_type_versions(self):
        """
        Returns:
            dict<str, str>: the latest versions for listed data types
        """
        return self.data.n

    @property
    def profile_icon_id_max(self):
        """
        Returns:
            int: the largest profileicon id that can be used under 500.0 Any profileicon that is requested between this number and 500 should be mapped to 0.0.
        """
        return self.data.profileiconmax

    @property
    def store(self):
        """
        Returns:
            str: additional api data drawn from other sources that may be related to data dragon functionality
        """
        return self.data.store

    @property
    def version(self):
        """
        Returns:
            str: the current version of this file
        """
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
        """
        Returns:
            str: the description of the rune
        """
        return self.data.description

    @property
    def id(self):
        """
        Returns:
            int: the ID of this rune
        """
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this rune
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def name(self):
        """
        Returns:
            str: the name of this rune
        """
        return self.data.name

    @cassiopeia.type.core.common.lazyproperty
    def meta_data(self):
        """
        Returns:
            MetaData: meta data about this rune
        """
        return MetaData(self.data.rune) if self.data.rune else None

    @property
    def sanitized_description(self):
        """
        Returns:
            str: the sanitized description of this rune
        """
        return self.data.sanitizedDescription

    @cassiopeia.type.core.common.lazyproperty
    def stats(self):
        """
        Returns:
            ItemStats: the stats for this rune
        """
        return ItemStats(self.data.stats) if self.data.stats else None

    @property
    def tags(self):
        """
        Returns:
            list<str>: this rune's tags for sorting runes
        """
        return self.data.tags

    @property
    def rune_type(self):
        """
        Returns:
            str: what type of rune this is
        """
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
        """
        Returns:
            list<float>: the cooldowns of this spell level-by-level
        """
        return self.data.cooldown

    @property
    def cooldown_burn(self):
        """
        Returns:
            str: formatted list of the spell's cooldowns by level
        """
        return self.data.cooldownBurn

    @property
    def costs(self):
        """
        Returns:
            list<int>: the cost of the spell level-by-level
        """
        return self.data.cost

    @property
    def cost_burn(self):
        """
        Returns:
            str: formatted list of the spell's cost by level
        """
        return self.data.costBurn

    @property
    def cost_type(self):
        """
        Returns:
            str: what the spell costs to use (e.g. mana or energy)
        """
        return self.data.costType

    @property
    def description(self):
        """
        Returns:
            str: the description of the summoner spell
        """
        return self.data.description

    @property
    def effects(self):
        """
        Returns:
            list<list<float>>: the level-by-level replacements for {{ e# }} tags in other values
        """
        return self.data.effect

    @property
    def effect_burn(self):
        """
        Returns:
            list<str>: the string formatted replacements for {{ e# }} tags in other values by level
        """
        return self.data.effectBurn

    @property
    def id(self):
        """
        Returns:
            int: the ID of this summoner spell
        """
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def image(self):
        """
        Returns:
            Image: the image of this summoner spell
        """
        return Image(self.data.image) if self.data.image else None

    @property
    def key(self):
        """
        Returns:
            str: this summoner spell's identifying key
        """
        return self.data.key

    @cassiopeia.type.core.common.lazyproperty
    def leveltip(self):
        """
        Returns:
            LevelTip: the level-up tips for this spell
        """
        return LevelTip(self.data.leveltip) if self.data.leveltip else None

    @property
    def max_rank(self):
        """
        Returns:
            the maximum level for this spell
        """
        return self.data.maxrank

    @property
    def modes(self):
        """
        Returns:
            list<GameMode>: the game modes that this spell is allowed on
        """
        return [cassiopeia.type.core.common.GameMode(mode) for mode in self.data.modes]

    @property
    def name(self):
        """
        Returns:
            str: the name of this spell
        """
        return self.data.name

    @property
    def range(self):
        """
        Returns:
            list<int>: the level-by-level range of this spell
        """
        return self.data.range

    @property
    def range_burn(self):
        """
        Returns:
            str: formatted range of this spell by level
        """
        return self.data.rangeBurn

    @property
    def resource(self):
        """
        Returns:
            str: what resource this spell uses
        """
        return self.data.resource

    @property
    def sanitized_description(self):
        """
        Returns:
            str: the sanitized description of this summoner spell
        """
        return self.data.sanitizedDescription

    @property
    def sanitized_tooltip(self):
        """
        Returns:
            str: the sanitized tooltip for this summoner spell
        """
        return self.data.sanitizedTooltip

    @property
    def summoner_level(self):
        """
        Returns:
            int: the summoner level required to use this spell
        """
        return self.data.summonerLevel

    @property
    def tooltip(self):
        """
        Returns:
            str: the tooltip for this spell
        """
        return self.data.tooltip

    @cassiopeia.type.core.common.lazyproperty
    def variables(self):
        """
        Returns:
            SpellVariables: the variables that determine this spell's effects
        """
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

        Args:
            level (int): the level of the champion

        Returns:
            str: the tooltip for that rank/level
        """
        return self.__replace_variables(self.tooltip, level)

    @cassiopeia.type.core.common.immutablemethod
    def sanitized_tooltip_for_level(self, level):
        """Gets the sanitized tooltip for this spell for a specific level

        Args:
            level (int): the level of the champion

        Returns:
            str: the sanitized tooltip for this summoner spell for the provided level
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
