from typing import Dict, List, Set, Union, Mapping, Any
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, Map
from ..datadragon import DataDragonImage
from ..common import DataObject, CassiopeiaObject, CassiopeiaGhost, Ghost
from .version import VersionListData
from ...dto.staticdata import item as dto


#ItemListDto - This object contains item list data.
#data    Map[string, ItemDto]
#version string
#tree    List[ItemTreeDto]
#groups  List[GroupDto]
#type    string
class ItemListData(list):
    _dto_type = dto.ItemListDto


##############
# Data Types #
##############


#ItemTreeDto - This object contains item tree data.
#header  string
#tags    List[string]

#InventoryDataStatsDto - This object contains stats for inventory (e.g., runes and items).
#PercentCritDamageMod    double
#PercentSpellBlockMod    double
#PercentHPRegenMod   double
#PercentMovementSpeedMod double
#FlatSpellBlockMod   double
#FlatCritDamageMod   double
#FlatEnergyPoolMod   double
#PercentLifeStealMod double
#FlatMPPoolMod   double
#FlatMovementSpeedMod    double
#PercentAttackSpeedMod   double
#FlatBlockMod    double
#PercentBlockMod double
#FlatEnergyRegenMod  double
#PercentSpellVampMod double
#FlatMPRegenMod  double
#PercentDodgeMod double
#FlatAttackSpeedMod  double
#FlatArmorMod    double
#FlatHPRegenMod  double
#PercentMagicDamageMod   double
#PercentMPPoolMod    double
#FlatMagicDamageMod  double
#PercentMPRegenMod   double
#PercentPhysicalDamageMod    double
#FlatPhysicalDamageMod   double
#PercentHPPoolMod    double
#PercentArmorMod double
#PercentCritChanceMod    double
#PercentEXPBonus double
#FlatHPPoolMod   double
#FlatCritChanceMod   double
#FlatEXPBonus    double



class SpriteData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def height(self) -> int:
        return self._dto["h"]


class ImageData(DataObject):
    _renamed = {"height": "h", "width": "w"}

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def full(self) -> str:
        return self._dto["full"]

    @property
    def group(self) -> str:
        return self._dto["group"]

    @property
    def height(self) -> int:
        return self._dto["h"]

    @property
    def width(self) -> int:
        return self._dto["w"]

    @property
    def y(self) -> int:
        return self._dto["y"]

    @property
    def x(self) -> int:
        return self._dto["x"]

    @property
    def sprite(self) -> str:
        return self._dto["sprite"]


class ItemStatsData(DataObject):
    pass


class GoldData(DataObject):
    @property
    def sell(self) -> int:
        return self._dto["sell"]

    @property
    def total(self) -> int:
        return self._dto["total"]

    @property
    def base(self) -> int:
        return self._dto["base"]

    @property
    def purchaseable(self) -> bool:
        return self._dto["purchaseable"]


class ItemData(DataObject):
    _dto_type = dto.ItemDto
    _renamed = {"hide": "hideFromAll", "in_store": "inStore", "builds_into": "into", "builds_from": "from", "keywords": "colloq", "champion": "requiredChampion", "consume_on_full": "consumeOnFull", "sanitized_description": "sanitizedDescription", "tier": "depth", "max_stacks": "stacks"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def version(self) -> str:
        return self._dto["version"]

    @property
    def locale(self) -> str:
        return self._dto["locale"]

    @property
    def item_data(self) -> Set[str]:
        return self._dto["itemData"]

    @property
    def gold(self) -> GoldData:
        return self._dto["gold"]

    @property
    def plaintext(self) -> str:
        return self._dto["plaintext"]

    @property
    def hide(self) -> bool:
        return self._dto["hideFromAll"]

    @property
    def in_store(self) -> bool:
        return self._dto["inStore"]

    @property
    def builds_into(self) -> List[int]:  # TODO Convert str to int in transformer
        return self._dto["into"]

    @property
    def builds_from(self) -> List[int]:  # TODO Convert str to int in transformer
        return self._dto["from"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def stats(self) -> ItemStatsData:
        return ItemStatsData(self._dto["stats"])

    @property
    def keywords(self) -> List[str]:  # TODO Convert from str to List[str]
        return self._dto["colloq"]

    @property
    def maps(self) -> List[Map]:  # TODO Convert from Dict to List
        """List of maps where this item is available."""
        return self._dto["maps"]

    #@property
    #def special_recipe(self) -> int:
    #    return self._dto["specialRecipe"]

    @property
    def image(self) -> ImageData:
        return ImageData(self._dto["image"])

    @property
    def description(self) -> str:
        return self._dto["description"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]

    @property
    def effect(self) -> Mapping[str, str]:
        return self._dto["effect"]

    @property
    def champion(self) -> int:
        return self._dto["requiredChampion"]

    @property
    def group(self) -> str:
        return self._dto["group"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def consume_on_full(self) -> bool:
        return self._dto["consumeOnFull"]

    @property
    def consumed(self) -> bool:
        return self._dto["consumed"]

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def tier(self) -> int:
        return self._dto["depth"]

    @property
    def max_stacks(self) -> int:
        return self._dto["stacks"]


##############
# Core Types #
##############


class Sprite(CassiopeiaObject):
    _data_types = {SpriteData}
    _extension = "png"

    @property
    def version(self) -> str:
        return self._data[SpriteData].version

    @property
    def sprite(self) -> str:
        return self._data[SpriteData].sprite

    @property
    def y(self) -> int:
        return self._data[SpriteData].y

    @property
    def x(self) -> int:
        return self._data[SpriteData].x

    @property
    def width(self) -> int:
        return self._data[SpriteData].width

    @property
    def height(self) -> int:
        return self._data[SpriteData].height

    @property
    def url(self) -> str:
        sprite = self.sprite
        if "." in sprite:
            sprite, self._extension = sprite.split(".")
        # There are not multiple images for different regions; this one works for all regions, so we don't need it
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/sprite/{sprite}.{ext}".format(version=self.version, sprite=sprite, ext=self._extension)

    @lazy_property
    def image(self) -> PILImage:
        return settings.pipeline.get(PILImage, query={"url": self.url})


class Image(CassiopeiaObject):
    _data_types = {ImageData}
    _extension = "png"

    @property
    def version(self) -> str:
        return self._data[ImageData].version

    @property
    def full(self) -> str:
        return self._data[ImageData].full

    @property
    def group(self) -> str:
        return self._data[ImageData].group

    @property
    def url(self) -> str:
        if "." in self.full:
            full, self._extension = self.full.split(".")
        # There are not multiple images for different regions; this one works for all regions, so we don't need it
        return "http://ddragon.leagueoflegends.com/cdn/{version}/img/{group}/{full}.{ext}".format(version=self.version, group=self.group, full=full, ext=self._extension)

    @lazy_property
    def sprite(self) -> Sprite:
        sprite = Sprite(w=self._data[ImageData].width,
                      h=self._data[ImageData].height,
                      x=self._data[ImageData].x,
                      y=self._data[ImageData].y,
                      sprite=self._data[ImageData].sprite,
                      version=self._data[ImageData].version)
        return sprite


class ItemStats(CassiopeiaObject):  # TODO
    _data_types = {ItemStatsData}


class Gold(CassiopeiaObject):
    _data_types = {GoldData}

    @property
    def sell(self) -> int:
        return self._data[GoldData].sell

    @property
    def total(self) -> int:
        return self._data[GoldData].total

    @property
    def base(self) -> int:
        return self._data[GoldData].base

    @property
    def purchaseable(self) -> bool:
        return self._data[GoldData].purchaseable


@searchable({str: ["name"], int: ["id"]})
class Item(CassiopeiaGhost):
    _data_types = {ItemData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    # What do we do about params like this that can exist in both data objects?
    # They will be set on both data objects always, so we can choose either one to return.
    @lazy_property
    def region(self) -> Region:
        """The region for this champion."""
        return Region(self._data[ItemData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this champion."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this champion."""
        try:
            return self._data[ChampionData].version
        except AttributeError:
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
            self(version=version)
            return self._data[ItemData].version

    @property
    def locale(self) -> str:
        """The locale for this champion."""
        return self._data[ItemData].locale

    @property
    def item_data(self) -> Set[str]:
        """A set of tags to return additonal information for this item when it's loaded."""
        return self._data[ItemData].item_data

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The item's ID."""
        return self._data[ItemData].id

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def gold(self) -> Gold:
        return self._data[ItemData].gold

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def plaintext(self) -> str:
        return self._data[ItemData].plaintext

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def hide(self) -> bool:
        return self._data[ItemData].hide

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def in_store(self) -> bool:
        return self._data[ItemData].in_store

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def builds_into(self) -> List["Item"]:
        return self._data[ItemData].builds_into

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def builds_from(self) -> List["Item"]:
        return self._data[ItemData].builds_from

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def stats(self) -> ItemStats:
        return self._data[ItemData].stats

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def kewords(self) -> List[str]:
        return self._data[ItemData].keywords

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def maps(self) -> List[Map]:
        return self._data[ItemData].maps

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def image_data(self) -> ImageData:
        return self._data[ItemData].image_data

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def description(self) -> str:
        return self._data[ItemData].description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def tags(self) -> List[str]:
        return self._data[ItemData].tags

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def effect(self) -> Mapping[str, str]:
        return self._data[ItemData].effect

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def champion(self) -> "Champion":
        return self._data[ItemData].champion

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def group(self) -> str:
        return self._data[ItemData].group

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[ItemData].name

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def consume_on_full(self) -> bool:
        return self._data[ItemData].consume_on_full

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def consumed(self) -> bool:
        return self._data[ItemData].consumed

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def sanitized_description(self) -> str:
        return self._data[ItemData].sanitized_description

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def tier(self) -> int:
        return self._data[ItemData].tier

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def max_stacks(self) -> int:
        return self._data[ItemData].max_stacks

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    def special_recipe(self) -> int:
        return self._data[ItemData].special_recipe

    @CassiopeiaGhost.property(ItemData)
    @ghost_load_on(KeyError)
    @lazy
    def image_info(self) -> Image:
        """The image information for this champion."""
        return Image(self._data[ChampionData].image, version=self.version)

    @lazy_property
    def image(self) -> PILImage:
        """The image icon for this champion."""
        return settings.pipeline.get(PILImage, query={"url": self.image_info.url})

    @lazy_property
    def sprite(self) -> Sprite:
        """The sprite that contains this champion's image icon."""
        return self.image_info.sprite.image
