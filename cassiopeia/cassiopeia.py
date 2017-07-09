from typing import List, Union
import datetime

from merakicommons.container import SearchableList

from .configuration import settings
from .data import PATCHES, Region
from .patches import Patch
from .core import VersionListData, Champion, ChampionData, ChampionListData, Summoner, Account, ChampionMastery, ChampionMasteryListData, Rune, RuneListData, Mastery, MasteryListData, Item, ItemListData, RunePage, RunePagesData, MasteryPage, MasteryPagesData, RunePage, MasteryPage, Match, MatchData, MatchListData
from .dto.staticdata.version import VersionListDto


def get_matches(summoner: Union[Summoner, int, str], region: Region = None):
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


def get_match(id, region: Region = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    return Match(id=id, region=region)


def get_champion_masteries(summoner: Union[Summoner, int, str], region: Region = None):
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


def get_champion_mastery(summoner: Union[Summoner, int, str], champion: Union[Champion, int, str], region: Region = None):
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if isinstance(summoner, int):
        summoner = Summoner(id=summoner)
    elif isinstance(summoner, str):
        summoner = Summoner(name=summoner)
    if isinstance(champion, int):
        champion = Champion(id=champion)
    elif isinstance(champion, str):
        champion = Champion(name=str)
    return ChampionMastery(champion=champion, summoner=summoner)


def get_summoner(name: Union[str, int] = None, region: Region = None, *, id: int = None, account_id: int = None) -> Summoner:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    if name:
        if isinstance(name, str):
            return Summoner(name=name)
        elif isinstance(name, int):
            raise NameError("specify `id=...` or `account_id=...`")
    elif id:
        return Summoner(id=id)
    elif account_id:
        return Summoner(account=Account(id=id))


def get_champion(key: Union[str, int], region: Region = None) -> Champion:
    if region is None:
        region = settings.default_region
    champions = get_champions(region)
    return champions[key]


def get_champions(region: Region = None) -> List[Champion]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    champions = settings.pipeline.get(ChampionListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, champion in enumerate(champions):
        champions[i] = Champion(data=champion)
    return SearchableList(champions)


def get_masteries(region: Region = None) -> List[Mastery]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    masteries = settings.pipeline.get(MasteryListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, mastery in enumerate(masteries):
        masteries[i] = Mastery(data=mastery)
    return SearchableList(masteries)


def get_runes(region: Region = None) -> List[Rune]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    runes = settings.pipeline.get(RuneListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, rune in enumerate(runes):
        runes[i] = Rune(data=rune)
    return SearchableList(runes)


def get_items(region: Region = None) -> List[Item]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    items = settings.pipeline.get(ItemListData, query={"region": region, "platform": region.platform.value, "tags": {"all"}})
    for i, item in enumerate(items):
        items[i] = Item(data=item)
    return SearchableList(items)


def get_mastery_pages(summoner: Summoner, region: Region = None) -> List[MasteryPage]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    mastery_pages = settings.pipeline.get(MasteryPagesData, query={"summonerId": summoner.id, "region": region, "platform": region.platform.value})
    for i, page in enumerate(mastery_pages):
        mastery_pages[i] = MasteryPage(data=page)
    return SearchableList(mastery_pages)


def get_rune_pages(summoner: Summoner, region: Region = None) -> List[RunePage]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    rune_pages = settings.pipeline.get(RunePagesData, query={"summonerId": summoner.id, "region": region, "platform": region.platform.value})
    for i, page in enumerate(rune_pages):
        rune_pages[i] = RunePage(data=page)
    return SearchableList(rune_pages)


def get_versions(region: Region = None) -> List[str]:
    if region is None:
        region = settings.default_region
    elif not isinstance(region, Region):
        region = Region(region)
    versions = settings.pipeline.get(VersionListData, query={"region": region, "platform": region.platform})
    return versions


def get_version(date: datetime.date = None, region: Region = None) -> Union[None, str]:
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
