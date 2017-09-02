from typing import Set, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.container import SearchableDictionary
from merakicommons.cache import lazy_property

from datapipelines import NotFoundError

from ... import configuration
from .dto import ChampionGGDto, ChampionGGListDto
from ...data import Region, Role, Tier, Patch
from ...core.common import CoreData, CassiopeiaGhost, DataObjectList


class ChampionGGListData(DataObjectList):
    _dto_type = ChampionGGListDto
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]


class ChampionGGData(CoreData):
    _dto_type = ChampionGGDto
    _renamed = {"included_data": "champData", "win_rate": "winRate", "id": "championId", "play_rate": "playRate", "games_played": "gamesPlayed", "percent_role_played": "percentRolePlayed", "ban_rate": "banRate", "damage_composition": "damageComposition", "total_damage_taken": "totalDamageTaken", "wards_killed": "wardsKilled", "neutralMinionsKilledTeamJungle": "neutralMinionsKilledTeamJungle", "performance_score": "overallPerformanceScore", "neutralMinionsKilledEnemyJungle": "neutralMinionsKilledEnemyJungle", "gold_earned": "goldEarned", "wards_placed": "wardPlaced", "minions_killed": "minionsKilled", "total_healed": "totalHeal"}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def elo(self) -> str:
        return self._dto["elo"].split(",")

    @property
    def included_data(self) -> str:
        return self._dto["champData"].split(",")

    @property
    def patch(self) -> str:
        return self._dto["patch"]

    @property
    def id(self) -> str:
        return self._dto["championId"]

    @property
    def win_rate(self) -> str:
        return self._dto["winRate"]

    @property
    def play_rate(self) -> str:
        return self._dto["playRate"]

    @property
    def play_rate_by_role(self) -> str:
        return self._dto["percentRolePlayed"]

    @property
    def ban_rate(self) -> str:
        return self._dto["banRate"]

    @property
    def games_played(self) -> str:
        return self._dto["gamesPlayed"]

    @property
    def damage_composition(self) -> str:
        return self._dto["damageComposition"]

    @property
    def kills(self) -> str:
        return self._dto["kills"]

    @property
    def total_damage_taken(self) -> str:
        return self._dto["totalDamageTaken"]

    @property
    def wards_killed(self) -> str:
        return self._dto["wardsKilled"]

    @property
    def neutral_minions_killed_in_team_jungle(self) -> str:
        return self._dto["neutralMinionsKilledTeamJungle"]

    @property
    def assists(self) -> str:
        return self._dto["assists"]

    @property
    def performance_score(self) -> str:
        return self._dto["overallPerformanceScore"]

    @property
    def neutral_minions_killed_in_enemy_jungle(self) -> str:
        return self._dto["neutralMinionsKilledEnemyJungle"]

    @property
    def gold_earned(self) -> str:
        return self._dto["goldEarned"]

    @property
    def deaths(self) -> str:
        return self._dto["deaths"]

    @property
    def minions_killed(self) -> str:
        return self._dto["minionsKilled"]

    @property
    def total_healed(self) -> str:
        return self._dto["totalHeal"]


class ChampionGGStats(CassiopeiaGhost):
    _data_types = {ChampionGGData}
    _load_types = {ChampionGGData: ChampionGGListData}

    def __init__(self, *, id: int, patch: Patch, included_data: Set[str] = None, elo: Set[str] = None, region: Union[Region, str] = None):
        if region is None:
            region = configuration.settings.default_region
        if region is not None and not isinstance(region, Region):
            region = Region(region)
        if included_data is None:
            # I manually chose a selection of data to return by default; I chose this data because it's relatively small and provides some additional useful information.
            included_data = "kda,damage,minions,wards,overallPerformanceScore,goldEarned"
        if elo is None:
            elo = "PLATINUM_DIAMOND_MASTER_CHALLENGER"
        kwargs = {"region": region, "id": id, "patch": patch._patch, "elo": elo, "included_data": included_data}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"patch": self.patch._patch, "includedData": ",".join(self.included_data), "elo": "_".join(self.elo)}

    def __load_hook__(self, load_group: ChampionGGData, data: ChampionGGListData) -> None:
        def find_matching_attribute(datalist, attrname, attrvalue):
            for item in datalist:
                if getattr(item, attrname, None) == attrvalue:
                    return item
            raise NotFoundError("Could not find `{}={}` in {}".format(attrname, attrvalue, datalist))
        data = find_matching_attribute(data, "id", self.id)
        super().__load_hook__(load_group, data)

    @lazy_property
    def region(self) -> Region:
        return Region(self._data[ChampionGGData].region)

    @property
    def included_data(self) -> Set[str]:
        return self._data[ChampionGGData].included_data

    @property
    def elo(self) -> Set[str]:
        return self._data[ChampionGGData].elo

    @property
    def patch(self) -> Patch:
        return Patch.from_str(self._data[ChampionGGData].patch)

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def id(self) -> int:
        return self._data[ChampionGGData].id

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def win_rate(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].win_rate.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def play_rate(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].play_rate.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def play_rate_by_role(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].play_rate_by_role.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def ban_rate(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].ban_rate.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def games_played(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].games_played.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def damage_composition(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].damage_composition.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def kills(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].kills.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def total_damage_taken(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].total_damage_taken.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def wards_killed(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].wards_killed.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def neutral_minions_killed_in_team_jungle(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].neutral_minions_killed_in_team_jungle.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def assists(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].assists.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def performance_score(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].performance_score.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def neutral_minions_killed_in_enemy_jungle(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].neutral_minions_killed_in_enemy_jungle.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def gold_earned(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].gold_earned.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def deaths(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].deaths.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def minions_killed(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].minions_killed.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def total_healed(self) -> SearchableDictionary:
        return SearchableDictionary({Role(role): value for role, value in self._data[ChampionGGData].total_healed.items()})

    @CassiopeiaGhost.property(ChampionGGData)
    @ghost_load_on(KeyError)
    def championgg_metadata(self) -> dict:
        return {
            "elo": [Tier(tier) for tier in self._data[ChampionGGData].elo],
            "patch": self.patch
        }
