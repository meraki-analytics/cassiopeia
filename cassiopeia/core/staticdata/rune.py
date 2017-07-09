from typing import Dict, List, Set, Union, Mapping, Any
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ...configuration import settings
from ...data import Region, Platform, RuneType
from ..datadragon import DataDragonImage
from ..common import DataObject, CassiopeiaObject, CassiopeiaGhost, Ghost
from .version import VersionListData
from ...dto.staticdata import rune as dto


class RuneListData(list):
    _dto_type = dto.RuneListDto
    #data    Map[string, RuneDto]    
    #version string
    #type    string


##############
# Data Types #
##############


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


class MetadataData(DataObject):
    _renamed = {"is_rune": "isRune"}

    # TODO Convert the type in the transformer from str to int
    @property
    def tier(self) -> int:
        return int(self._dto["tier"])

    @property
    def type(self) -> str:
        return self._dto["type"]

    @property
    def is_rune(self) -> bool:
        return self._dto["is_rune"]


class RuneStatsData(DataObject):
    pass
#RuneStatsDto - This object contains stats for runes. 
#PercentTimeDeadModPerLevel  double  
#PercentArmorPenetrationModPerLevel  double  
#PercentCritDamageMod    double  
#PercentSpellBlockMod    double  
#PercentHPRegenMod   double  
#PercentMovementSpeedMod double  
#FlatSpellBlockMod   double  
#FlatEnergyRegenModPerLevel  double  
#FlatEnergyPoolMod   double  
#FlatMagicPenetrationModPerLevel double  
#PercentLifeStealMod double  
#FlatMPPoolMod   double  
#PercentCooldownMod  double  
#PercentMagicPenetrationMod  double  
#FlatArmorPenetrationModPerLevel double  
#FlatMovementSpeedMod    double  
#FlatTimeDeadModPerLevel double  
#FlatArmorModPerLevel    double  
#PercentAttackSpeedMod   double  
#FlatDodgeModPerLevel    double  
#PercentMagicDamageMod   double  
#PercentBlockMod double  
#FlatDodgeMod    double  
#FlatEnergyRegenMod  double  
#FlatHPModPerLevel   double  
#PercentAttackSpeedModPerLevel   double  
#PercentSpellVampMod double  
#FlatMPRegenMod  double  
#PercentHPPoolMod    double  
#PercentDodgeMod double  
#FlatAttackSpeedMod  double  
#FlatArmorMod    double  
#FlatMagicDamageModPerLevel  double  
#FlatHPRegenMod  double  
#PercentPhysicalDamageMod    double  
#FlatCritChanceModPerLevel   double  
#FlatSpellBlockModPerLevel   double  
#PercentTimeDeadMod  double  
#FlatBlockMod    double  
#PercentMPPoolMod    double  
#FlatMagicDamageMod  double  
#PercentMPRegenMod   double  
#PercentMovementSpeedModPerLevel double  
#PercentCooldownModPerLevel  double  
#FlatMPModPerLevel   double  
#FlatEnergyModPerLevel   double  
#FlatPhysicalDamageMod   double  
#FlatHPRegenModPerLevel  double  
#FlatCritDamageMod   double  
#PercentArmorMod double  
#FlatMagicPenetrationMod double  
#PercentCritChanceMod    double  
#FlatPhysicalDamageModPerLevel   double  
#PercentArmorPenetrationMod  double  
#PercentEXPBonus double  
#FlatMPRegenModPerLevel  double  
#PercentMagicPenetrationModPerLevel  double  
#FlatTimeDeadMod double  
#FlatMovementSpeedModPerLevel    double  
#FlatGoldPer10Mod    double  
#FlatArmorPenetrationMod double  
#FlatCritDamageModPerLevel   double  
#FlatHPPoolMod   double  
#FlatCritChanceMod   double  
#FlatEXPBonus    double  


class RuneData(DataObject):
    _dto_type = dto.RuneDto
    _renamed = {"metadata": "rune", "sanitized_description": "sanitizedDescription"}

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
    def metadata(self) -> MetadataData:
        return MetadataData(self._dto["rune"])

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def stats(self) -> RuneStatsData:
        return self._dto["stats"]

    @property
    def image_data(self) -> str:
        return self._dto["image"]

    @property
    def tags(self) -> List[str]:
        return self._dto["tags"]

    @property
    def sanitized_description(self) -> str:
        return self._dto["sanitizedDescription"]

    @property
    def description(self) -> str:
        return self._dto["description"]


##############
# Core Types #
##############


@searchable({str: ["sprite", "url"]})
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


@searchable({str: ["full", "url"]})
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


class RuneStats(CassiopeiaObject):  # TODO
    pass


@searchable({str: ["name", "tags", "type", "region", "platform", "locale"], int: ["id"], RuneType: ["type"], Region: ["region"], Platform: ["platform"]})
class Rune(CassiopeiaGhost):
    _data_types = {RuneData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

    @lazy_property
    def region(self) -> Region:
        """The region for this rune."""
        return Region(self._data[RuneData].region)

    @lazy_property
    def platform(self) -> Platform:
        """The platform for this rune."""
        return self.region.platform

    @property
    def version(self) -> str:
        """The version for this rune."""
        try:
            return self._data[RuneData].version
        except AttributeError:
            versions = settings.pipeline.get(VersionListData, query={"region": self.region, "platform": self.region.platform})
            version = versions[-1]
            self(version=version)
            return self._data[RuneData].version

    @property
    def locale(self) -> str:
        """The locale for this rune."""
        return self._data[RuneData].locale

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def tier(self) -> int:
        return self._data[RuneData].metadata.tier

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def type(self) -> RuneType:
        return RuneType(self._data[RuneData].metadata.type)

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        """The rune's name."""
        return self._data[RuneData].name

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        """The rune's ID."""
        return self._data[RuneData].id

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def description(self) -> int:
        """The rune's description."""
        return self._data[RuneData].description

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def sanitized_description(self) -> int:
        """The rune's sanitized description."""
        return self._data[RuneData].sanitized_description

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def stats(self) -> RuneStats:
        return RuneStats(self._data[RuneData].stats)

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    def tags(self) -> List[str]:
        return self._data[RuneData].id

    @CassiopeiaGhost.property(RuneData)
    @ghost_load_on(KeyError)
    @lazy
    def image_info(self) -> Image:
        """The image information for this rune."""
        return Image(self._data[RuneData].image, version=self.version)

    @lazy_property
    def image(self) -> PILImage:
        """The image icon for this rune."""
        return settings.pipeline.get(PILImage, query={"url": self.image_info.url})

    @lazy_property
    def sprite(self) -> Sprite:
        """The sprite that contains this rune's image icon."""
        return self.image_info.sprite.image
