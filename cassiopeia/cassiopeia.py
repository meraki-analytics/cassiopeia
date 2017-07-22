from typing import List, Union
import datetime

from merakicommons.container import SearchableList

from .configuration import settings
from .data import PATCHES, Region
from .patches import Patch
from .core import Champion, Summoner, Account, ChampionMastery, Rune, Mastery, Item, RunePage, MasteryPage, Match, Map, SummonerSpell, Realms, ProfileIcon, LanguageStrings, CurrentMatch, ShardStatus
from .core.staticdata.version import VersionListData
from .core.staticdata.champion import ChampionListData
from .core.staticdata.rune import RuneListData
from .core.staticdata.mastery import MasteryListData
from .core.staticdata.item import ItemListData
from .core.staticdata.map import MapListData
from .core.staticdata.summonerspell import SummonerSpellListData
from .core.staticdata.profileicon import ProfileIconListData
from .core.staticdata.language import LanguagesData
from .core.championmastery import ChampionMasteryListData
from .core.runepage import RunePagesData
from .core.masterypage import MasteryPagesData
from .core.match import MatchListData
from .core.spectator import FeaturedGamesData
# TODO Add featured games


def get_matches(summoner: Union[Summoner, int, str], region: Union[Region, str] = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if isinstance(summoner, int):
        summoner = Summoner(id=summoner)
    elif isinstance(summoner, str):
        summoner = Summoner(name=summoner)
    matchlist = settings.pipeline.get(MatchListData, query={"accountId": summoner.account.id, "region": region, "platform": region.platform.value})
    return SearchableList([Match.from_match_reference(ref) for ref in matchlist])


def get_match(id, region: Union[Region, str] = None) -> Match:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    return Match(id=id, region=region)


def get_featured_matches(region: Union[Region, str] = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    matchlist = settings.pipeline.get(FeaturedGamesData, query={"region": region, "platform": region.platform.value})
    return SearchableList([CurrentMatch(match) for match in matchlist])


def get_current_match(summoner: Union[Summoner, int, str], region: Union[Region, str] = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if isinstance(summoner, int):
        summoner = Summoner(id=summoner)
    elif isinstance(summoner, str):
        summoner = Summoner(name=summoner)
    return CurrentMatch(summoner=summoner, region=region)


def get_champion_masteries(summoner: Union[Summoner, int, str], region: Union[Region, str] = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if isinstance(summoner, int):
        summoner = Summoner(id=summoner)
    elif isinstance(summoner, str):
        summoner = Summoner(name=summoner)
    cms = settings.pipeline.get(ChampionMasteryListData, query={"playerId": summoner.id, "region": region, "platform": region.platform.value})
    for i, cm in enumerate(cms):
        cms[i] = ChampionMastery(data=cm)
    return SearchableList(cms)


def get_champion_mastery(summoner: Union[Summoner, int, str], champion: Union[Champion, int, str], region: Union[Region, str] = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if isinstance(summoner, int):
        summoner = Summoner(id=summoner, region=region)
    elif isinstance(summoner, str):
        summoner = Summoner(name=summoner, region=region)
    if isinstance(champion, int):
        champion = Champion(id=champion, region=region)
    elif isinstance(champion, str):
        champion = Champion(name=str, region=region)
    return ChampionMastery(champion=champion, summoner=summoner, region=region)


def get_summoner(name: Union[str, int] = None, region: Union[Region, str] = None, *, id: int = None, account_id: int = None) -> Summoner:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if name:
        if isinstance(name, str):
            return Summoner(name=name, region=region)
        elif isinstance(name, int):
            raise NameError("specify `id=...` or `account_id=...`")
    elif id:
        return Summoner(id=id, region=region)
    elif account_id:
        return Summoner(account=Account(id=id), region=region)


def get_champion(key: Union[str, int], region: Union[Region, str] = None) -> Champion:
    if region is None:
        region = settings.default_region
    champions = get_champions(region)
    return champions[key]


def get_champions(region: Union[Region, str] = None) -> List[Champion]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    champions = settings.pipeline.get(ChampionListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, champion in enumerate(champions):
        champions[i] = Champion(data=champion)
    return SearchableList(champions)


def get_masteries(region: Union[Region, str] = None) -> List[Mastery]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    masteries = settings.pipeline.get(MasteryListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, mastery in enumerate(masteries):
        masteries[i] = Mastery(data=mastery)
    return SearchableList(masteries)


def get_runes(region: Union[Region, str] = None) -> List[Rune]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    runes = settings.pipeline.get(RuneListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, rune in enumerate(runes):
        runes[i] = Rune(data=rune)
    return SearchableList(runes)


def get_summoner_spells(region: Union[Region, str] = None) -> List[SummonerSpell]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    summoner_spells = settings.pipeline.get(SummonerSpellListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, summoner_spell in enumerate(summoner_spells):
        summoner_spells[i] = SummonerSpell(data=summoner_spell)
    return SearchableList(summoner_spells)


def get_items(region: Union[Region, str] = None) -> List[Item]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    items = settings.pipeline.get(ItemListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, item in enumerate(items):
        items[i] = Item(data=item)
    return SearchableList(items)


def get_mastery_pages(summoner: Summoner, region: Union[Region, str] = None) -> List[MasteryPage]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    mastery_pages = settings.pipeline.get(MasteryPagesData, query={"summonerId": summoner.id, "region": region, "platform": region.platform.value})
    for i, page in enumerate(mastery_pages):
        mastery_pages[i] = MasteryPage(data=page)
    return SearchableList(mastery_pages)


def get_rune_pages(summoner: Summoner, region: Union[Region, str] = None) -> List[RunePage]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    rune_pages = settings.pipeline.get(RunePagesData, query={"summonerId": summoner.id, "region": region, "platform": region.platform.value})
    for i, page in enumerate(rune_pages):
        rune_pages[i] = RunePage(data=page)
    return SearchableList(rune_pages)


def get_maps(region: Union[Region, str] = None) -> List[Map]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    maps = settings.pipeline.get(MapListData, query={"region": region, "platform": region.platform})
    return SearchableList([Map(map) for map in maps])


def get_profile_icons(region: Union[Region, str] = None) -> List[ProfileIcon]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    profile_icons = settings.pipeline.get(ProfileIconListData, query={"region": region, "platform": region.platform.value})
    return SearchableList([ProfileIcon(icon) for icon in profile_icons])


def get_realms(region: Union[Region, str] = None) -> Realms:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    return Realms(region=region)


def get_status(region: Union[Region, str] = None) -> ShardStatus:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    return ShardStatus(region=region)


def get_language_strings(region: Union[Region, str] = None) -> LanguageStrings:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    return LanguageStrings(region=region)


def get_languages(region: Union[Region, str] = None) -> List[str]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    languages = settings.pipeline.get(LanguagesData, query={"region": region, "platform": region.platform})
    return languages


def get_versions(region: Union[Region, str] = None) -> List[str]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    versions = settings.pipeline.get(VersionListData, query={"region": region, "platform": region.platform})
    return versions


def get_version(date: datetime.date = None, region: Union[Region, str] = None) -> Union[None, str]:
    if region is None:
        region = settings.default_region
    versions = get_versions(region)
    if date is None:
        return versions[0]
    else:
        patch = get_patch(date)
        for version in versions:
            if patch.majorminor in version:
                return version
    return None


def get_patch(date: datetime.date) -> Patch:
    for _date in PATCHES:
        if _date >= date:
            return PATCHES[_date]
    return PATCHES[next(reversed(PATCHES))]
