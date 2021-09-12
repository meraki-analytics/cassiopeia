from typing import Type, Mapping, Any, Iterable, TypeVar, Tuple, Callable, Generator
import datetime

from datapipelines import DataSource, DataSink, PipelineContext, validate_query, NotFoundError
from merakicommons.cache import Cache as CommonsCache

from . import uniquekeys
from ..core.staticdata.champion import ChampionData, ChampionListData, Champion, Champions
from ..core.staticdata.rune import RuneData, RuneListData, Rune, Runes
from ..core.staticdata.item import ItemData, ItemListData, Item, Items
from ..core.staticdata.summonerspell import SummonerSpellData, SummonerSpellListData, SummonerSpell, SummonerSpells
from ..core.staticdata.map import MapData, MapListData, Map, Maps
from ..core.staticdata.realm import RealmData, Realms
from ..core.staticdata.profileicon import ProfileIconData, ProfileIconListData, ProfileIcon, ProfileIcons
from ..core.staticdata.language import LanguagesData, Locales
from ..core.staticdata.languagestrings import LanguageStringsData, LanguageStrings
from ..core.staticdata.version import VersionListData, Versions
from ..core.championmastery import ChampionMasteryData, ChampionMasteryListData, ChampionMastery, ChampionMasteries
from ..core.league import MasterLeagueListData, GrandmasterLeagueListData, ChallengerLeagueListData, LeagueSummonerEntries, League, ChallengerLeague, GrandmasterLeague, MasterLeague, LeagueEntries
from ..core.match import MatchData, TimelineData, Match, Timeline
from ..core.summoner import SummonerData, Summoner
from ..core.status import ShardStatusData, ShardStatus
from ..core.spectator import CurrentGameInfoData, FeaturedGamesData, CurrentMatch, FeaturedMatches
from ..core.champion import ChampionRotationData, ChampionRotation

T = TypeVar("T")


default_expirations = {
    ChampionRotationData: datetime.timedelta(hours=6),
    Realms: datetime.timedelta(hours=6),
    Versions: datetime.timedelta(hours=6),
    Champion: datetime.timedelta(days=20),
    Rune: datetime.timedelta(days=20),
    Item: datetime.timedelta(days=20),
    SummonerSpell: datetime.timedelta(days=20),
    Map: datetime.timedelta(days=20),
    ProfileIcon: datetime.timedelta(days=20),
    Locales: datetime.timedelta(days=20),
    LanguageStrings: datetime.timedelta(days=20),
    SummonerSpells: datetime.timedelta(days=20),
    Items: datetime.timedelta(days=20),
    Champions: datetime.timedelta(days=20),
    Runes: datetime.timedelta(days=20),
    Maps: datetime.timedelta(days=20),
    ProfileIcons: datetime.timedelta(days=20),
    ChampionMastery: datetime.timedelta(days=7),
    ChampionMasteries: datetime.timedelta(days=7),
    LeagueSummonerEntries: datetime.timedelta(hours=6),
    League: datetime.timedelta(hours=6),
    ChallengerLeague: datetime.timedelta(hours=6),
    GrandmasterLeague: datetime.timedelta(hours=6),
    MasterLeague: datetime.timedelta(hours=6),
    Match: datetime.timedelta(days=3),
    Timeline: datetime.timedelta(days=1),
    Summoner: datetime.timedelta(days=1),
    ShardStatus: datetime.timedelta(hours=1),
    CurrentMatch: datetime.timedelta(hours=0.5),
    FeaturedMatches: datetime.timedelta(hours=0.5),
}


class Cache(DataSource, DataSink):
    def __init__(self, expirations: Mapping[type, float] = None) -> None:
        self._cache = CommonsCache()
        self._expirations = dict(expirations) if expirations is not None else default_expirations
        for key, value in list(self._expirations.items()):
            if isinstance(key, str):
                new_key = globals()[key]
                self._expirations[new_key] = self._expirations.pop(key)
                key = new_key
            if value != -1 and isinstance(value, datetime.timedelta):
                self._expirations[key] = value.seconds + 24 * 60 * 60 * value.days

    @DataSource.dispatch
    def get(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> T:
        pass

    @DataSource.dispatch
    def get_many(self, type: Type[T], query: Mapping[str, Any], context: PipelineContext = None) -> Iterable[T]:
        pass

    @DataSink.dispatch
    def put(self, type: Type[T], item: T, context: PipelineContext = None) -> None:
        pass

    @DataSink.dispatch
    def put_many(self, type: Type[T], items: Iterable[T], context: PipelineContext = None) -> None:
        pass

    def _get(self, type: Type[T], query: Mapping[str, Any], key_function: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None) -> T:
        keys = key_function(query)
        for key in keys:
            try:
                return self._cache.get(type, key)
            except KeyError:
                pass
        else:
            raise NotFoundError

    def _get_many(self, type: Type[T], query: Mapping[str, Any], key_generator: Callable[[Mapping[str, Any]], Any], context: PipelineContext = None) -> Generator[T, None, None]:
        for keys in key_generator(query):
            for key in keys:
                try:
                    yield self._cache.get(type, key)
                except KeyError:
                    pass
            else:
                raise NotFoundError

    @staticmethod
    def _put_many_generator(items: Iterable[T], key_function: Callable[[T], Any]) -> Generator[Tuple[Any, T], None, None]:
        for item in items:
            for key in key_function(item):
                yield key, item

    def _put(self, type: Type[T], item: T, key_function: Callable[[T], Any], context: PipelineContext = None) -> None:
        try:
            expire_seconds = self._expirations[type]
        except KeyError:
            expire_seconds = -1

        if expire_seconds != 0:
            keys = key_function(item)
            for key in keys:
                self._cache.put(type, key, item, expire_seconds)

    def _put_many(self, type: Type[T], items: Iterable[T], key_function: Callable[[T], Any], context: PipelineContext = None) -> None:
        expire_seconds = self._expirations.get(type, default_expirations[type])
        for key, item in Cache._put_many_generator(items, key_function):
            self._cache.put(type, key, item, expire_seconds)

    def clear(self, type: Type[T] = None):
        if type is None:
            for key in self._cache._data:
                self._cache._data[key].clear()
        else:
            self._cache._data[type].clear()

    def expire(self, type: Type[T] = None):
        self._cache.expire(type)


    #####################
    # Champion Rotation #
    #####################

    # Champion Rotation Data

    @get.register(ChampionRotationData)
    @validate_query(uniquekeys.validate_champion_rotation_query, uniquekeys.convert_region_to_platform)
    def get_champion_rotation(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionRotationData:
        return self._get(ChampionRotationData, query, uniquekeys.for_champion_rotation_query, context)

    @get_many.register(ChampionRotationData)
    @validate_query(uniquekeys.validate_many_champion_rotation_query, uniquekeys.convert_region_to_platform)
    def get_many_champion_rotation(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionRotationData, None, None]:
        return self._get_many(ChampionRotationData, query, uniquekeys.for_many_champion_rotation_query, context)

    @put.register(ChampionRotationData)
    def put_champion_rotation(self, item: ChampionRotationData, context: PipelineContext = None) -> None:
        self._put(ChampionRotationData, item, uniquekeys.for_champion_rotation, context=context)

    @put_many.register(ChampionRotationData)
    def put_many_champion_rotation(self, items: Iterable[ChampionRotationData], context: PipelineContext = None) -> None:
        self._put_many(ChampionRotationData, items, uniquekeys.for_many_champion_rotation, context=context)


    ########################
    # Champion Mastery API #
    ########################

    # Champion Mastery

    @get.register(ChampionMastery)
    @validate_query(uniquekeys.validate_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMastery:
        return self._get(ChampionMastery, query, uniquekeys.for_champion_mastery_query, context)

    @get_many.register(ChampionMastery)
    @validate_query(uniquekeys.validate_many_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_many_champion_mastery(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMastery, None, None]:
        return self._get_many(ChampionMastery, query, uniquekeys.for_many_champion_mastery_query, context)

    @put.register(ChampionMastery)
    def put_champion_mastery(self, item: ChampionMastery, context: PipelineContext = None) -> None:
        self._put(ChampionMastery, item, uniquekeys.for_champion_mastery, context=context)

    @put_many.register(ChampionMastery)
    def put_many_champion_mastery(self, items: Iterable[ChampionMastery], context: PipelineContext = None) -> None:
        self._put_many(ChampionMastery, items, uniquekeys.for_many_champion_mastery, context=context)

    @get.register(ChampionMasteryData)
    @validate_query(uniquekeys.validate_champion_mastery_query, uniquekeys.convert_region_to_platform)
    def get_champion_mastery_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMasteryData:
        result = self.get_champion_mastery(query=query, context=context)
        if result._data[ChampionMasteryData] is not None and result._Ghost__is_loaded(ChampionMasteryData):
            return result._data[ChampionMasteryData]
        else:
            raise NotFoundError

    # Champion Masteries

    @get.register(ChampionMasteries)
    @validate_query(uniquekeys.validate_champion_masteries_query, uniquekeys.convert_region_to_platform)
    def get_champion_masteries(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionMasteries:
        return self._get(ChampionMasteries, query, uniquekeys.for_champion_masteries_query, context)

    @get_many.register(ChampionMasteries)
    @validate_query(uniquekeys.validate_many_champion_masteries_query, uniquekeys.convert_region_to_platform)
    def get_many_champion_masteries(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChampionMasteries, None, None]:
        return self._get_many(ChampionMasteries, query, uniquekeys.for_many_champion_masteries_query, context)

    @put.register(ChampionMasteries)
    def put_champion_masteries(self, item: ChampionMasteries, context: PipelineContext = None) -> None:
        self._put(ChampionMasteries, item, uniquekeys.for_champion_masteries, context=context)
        for cm in item:
            self._put(ChampionMastery, cm, uniquekeys.for_champion_mastery, context=context)

    @put_many.register(ChampionMasteries)
    def put_many_champion_masteries(self, items: Iterable[ChampionMasteries], context: PipelineContext = None) -> None:
        self._put_many(ChampionMasteries, items, uniquekeys.for_champion_masteries, context=context)

    ##############
    # League API #
    ##############

    # LeagueSummonerEntries

    @get.register(LeagueSummonerEntries)
    @validate_query(uniquekeys.validate_league_entries_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner_entries(self, query: Mapping[str, Any], context: PipelineContext = None) -> LeagueSummonerEntries:
        return self._get(LeagueSummonerEntries, query, uniquekeys.for_league_summoner_entries_query, context)

    @get_many.register(LeagueSummonerEntries)
    @validate_query(uniquekeys.validate_many_league_entries_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner_entries(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LeagueSummonerEntries, None, None]:
        return self._get_many(LeagueSummonerEntries, query, uniquekeys.for_many_league_summoner_entries_query, context)

    @put.register(LeagueSummonerEntries)
    def put_league_summoner_entries(self, item: LeagueSummonerEntries, context: PipelineContext = None) -> None:
        self._put(LeagueSummonerEntries, item, uniquekeys.for_league_summoner_entries, context=context)

    @put_many.register(LeagueSummonerEntries)
    def put_many_league_summoner_entries(self, items: Iterable[LeagueSummonerEntries], context: PipelineContext = None) -> None:
        self._put_many(LeagueSummonerEntries, items, uniquekeys.for_league_summoner_entries, context=context)

    # Challenger

    @get.register(ChallengerLeague)
    @validate_query(uniquekeys.validate_challenger_league_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChallengerLeague:
        return self._get(ChallengerLeague, query, uniquekeys.for_challenger_league_query, context)

    @get_many.register(ChallengerLeague)
    @validate_query(uniquekeys.validate_many_challenger_league_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ChallengerLeague, None, None]:
        return self._get_many(ChallengerLeague, query, uniquekeys.for_many_challenger_league_query, context)

    @put.register(ChallengerLeague)
    def put_league_summoner(self, item: ChallengerLeague, context: PipelineContext = None) -> None:
        self._put(ChallengerLeague, item, uniquekeys.for_challenger_league, context=context)

    @put_many.register(ChallengerLeague)
    def put_many_league_summoner(self, items: Iterable[ChallengerLeague], context: PipelineContext = None) -> None:
        self._put_many(ChallengerLeague, items, uniquekeys.for_challenger_league, context=context)

    # Grandmaster

    @get.register(GrandmasterLeague)
    @validate_query(uniquekeys.validate_grandmaster_league_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> GrandmasterLeague:
        return self._get(GrandmasterLeague, query, uniquekeys.for_grandmaster_league_query, context)

    @get_many.register(GrandmasterLeague)
    @validate_query(uniquekeys.validate_many_grandmaster_league_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[GrandmasterLeague, None, None]:
        return self._get_many(GrandmasterLeague, query, uniquekeys.for_many_grandmaster_league_query, context)

    @put.register(GrandmasterLeague)
    def put_league_summoner(self, item: GrandmasterLeague, context: PipelineContext = None) -> None:
        self._put(GrandmasterLeague, item, uniquekeys.for_grandmaster_league, context=context)

    @put_many.register(GrandmasterLeague)
    def put_many_league_summoner(self, items: Iterable[GrandmasterLeague], context: PipelineContext = None) -> None:
        self._put_many(GrandmasterLeague, items, uniquekeys.for_grandmaster_league, context=context)

    # Master

    @get.register(MasterLeague)
    @validate_query(uniquekeys.validate_master_league_query, uniquekeys.convert_region_to_platform)
    def get_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> MasterLeague:
        return self._get(MasterLeague, query, uniquekeys.for_master_league_query, context)

    @get_many.register(MasterLeague)
    @validate_query(uniquekeys.validate_many_master_league_query, uniquekeys.convert_region_to_platform)
    def get_many_league_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[MasterLeague, None, None]:
        return self._get_many(MasterLeague, query, uniquekeys.for_many_master_league_query, context)

    @put.register(MasterLeague)
    def put_league_summoner(self, item: MasterLeague, context: PipelineContext = None) -> None:
        self._put(MasterLeague, item, uniquekeys.for_master_league, context=context)

    @put_many.register(MasterLeague)
    def put_many_league_summoner(self, items: Iterable[MasterLeague], context: PipelineContext = None) -> None:
        self._put_many(MasterLeague, items, uniquekeys.for_master_league, context=context)


    ###################
    # Static Data API #
    ###################

    # Champion

    @get.register(Champion)
    @validate_query(uniquekeys.validate_champion_query, uniquekeys.convert_region_to_platform)
    def get_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champion:
        return self._get(Champion, query, uniquekeys.for_champion_query, context)

    @get_many.register(Champion)
    @validate_query(uniquekeys.validate_many_champion_query, uniquekeys.convert_region_to_platform)
    def get_many_champion(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champion, None, None]:
        return self._get_many(Champion, query, uniquekeys.for_many_champion_query, context)

    @put.register(Champion)
    def put_champion(self, item: Champion, context: PipelineContext = None) -> None:
        self._put(Champion, item, uniquekeys.for_champion, context=context)

    @put_many.register(Champion)
    def put_many_champion(self, items: Iterable[Champion], context: PipelineContext = None) -> None:
        self._put_many(Champion, items, uniquekeys.for_champion, context=context)

    @get.register(ChampionData)
    @validate_query(uniquekeys.validate_champion_query, uniquekeys.convert_region_to_platform)
    def get_champion_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ChampionData:
        result = self.get_champion(query=query, context=context)
        if result._data[ChampionData] is not None and result._Ghost__is_loaded(ChampionData):
            return result._data[ChampionData]
        else:
            raise NotFoundError

    # Champions

    @get.register(Champions)
    @validate_query(uniquekeys.validate_champions_query, uniquekeys.convert_region_to_platform)
    def get_champions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Champions:
        return self._get(Champions, query, uniquekeys.for_champions_query, context)

    @get_many.register(Champions)
    @validate_query(uniquekeys.validate_many_champions_query, uniquekeys.convert_region_to_platform)
    def get_many_champions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Champions, None, None]:
        return self._get_many(Champions, query, uniquekeys.for_many_champions_query, context)

    @put.register(Champions)
    def put_champions(self, champions: Champions, context: PipelineContext = None) -> None:
        self._put(Champions, champions, uniquekeys.for_champions, context=context)
        for champion in champions:
            self._put(Champion, champion, uniquekeys.for_champion, context=context)

    @put_many.register(Champions)
    def put_many_champions(self, champions: Iterable[Champions], context: PipelineContext = None) -> None:
        self._put_many(Champions, champions, uniquekeys.for_champions, context=context)

    # Item

    @get.register(Item)
    @validate_query(uniquekeys.validate_item_query, uniquekeys.convert_region_to_platform)
    def get_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Item:
        return self._get(Item, query, uniquekeys.for_item_query, context)

    @get_many.register(Item)
    @validate_query(uniquekeys.validate_many_item_query, uniquekeys.convert_region_to_platform)
    def get_many_item(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Item, None, None]:
        return self._get_many(Item, query, uniquekeys.for_many_item_query, context)

    @put.register(Item)
    def put_item(self, item: Item, context: PipelineContext = None) -> None:
        self._put(Item, item, uniquekeys.for_item, context=context)

    @put_many.register(Item)
    def put_many_item(self, items: Iterable[Item], context: PipelineContext = None) -> None:
        self._put_many(Item, items, uniquekeys.for_item, context=context)

    @get.register(ItemData)
    @validate_query(uniquekeys.validate_item_query, uniquekeys.convert_region_to_platform)
    def get_item_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ItemData:
        result = self.get_item(query=query, context=context)
        if result._data[ItemData] is not None and result._Ghost__is_loaded(ItemData):
            return result._data[ItemData]
        else:
            raise NotFoundError

    # Items

    @get.register(Items)
    @validate_query(uniquekeys.validate_items_query, uniquekeys.convert_region_to_platform)
    def get_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Items:
        return self._get(Items, query, uniquekeys.for_items_query, context=context)

    @get_many.register(Items)
    @validate_query(uniquekeys.validate_many_items_query, uniquekeys.convert_region_to_platform)
    def get_many_items(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Items, None, None]:
        return self._get_many(Items, query, uniquekeys.for_many_items_query, context)

    @put.register(Items)
    def put_items(self, items: Items, context: PipelineContext = None) -> None:
        self._put(Items, items, uniquekeys.for_items, context=context)
        for item in items:
            self._put(Item, item, uniquekeys.for_item, context=context)

    @put_many.register(Items)
    def put_many_items(self, many_items: Iterable[Items], context: PipelineContext = None) -> None:
        self._put_many(Items, many_items, uniquekeys.for_items, context=context)

    # Language

    @get.register(Locales)
    @validate_query(uniquekeys.validate_languages_query, uniquekeys.convert_region_to_platform)
    def get_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Locales:
        return self._get(Locales, query, uniquekeys.for_languages_query, context)

    @get_many.register(Locales)
    @validate_query(uniquekeys.validate_many_languages_query, uniquekeys.convert_region_to_platform)
    def get_many_languages(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Locales, None, None]:
        return self._get_many(Locales, query, uniquekeys.for_many_languages_query, context)

    @put.register(Locales)
    def put_languages(self, item: Locales, context: PipelineContext = None) -> None:
        self._put(Locales, item, uniquekeys.for_languages, context=context)

    @put_many.register(Locales)
    def put_many_languages(self, items: Iterable[Locales], context: PipelineContext = None) -> None:
        self._put_many(Locales, items, uniquekeys.for_languages, context=context)

    # Language strings

    @get.register(LanguageStrings)
    @validate_query(uniquekeys.validate_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStrings:
        return self._get(LanguageStrings, query, uniquekeys.for_language_strings_query, context)

    @get_many.register(LanguageStrings)
    @validate_query(uniquekeys.validate_many_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_many_language_strings(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[LanguageStrings, None, None]:
        return self._get_many(LanguageStrings, query, uniquekeys.for_many_language_strings_query, context)

    @put.register(LanguageStrings)
    def put_language_strings(self, item: LanguageStrings, context: PipelineContext = None) -> None:
        self._put(LanguageStrings, item, uniquekeys.for_language_strings, context=context)

    @put_many.register(LanguageStrings)
    def put_many_language_strings(self, items: Iterable[LanguageStrings], context: PipelineContext = None) -> None:
        self._put_many(LanguageStrings, items, uniquekeys.for_language_strings, context=context)

    @get.register(LanguageStringsData)
    @validate_query(uniquekeys.validate_language_strings_query, uniquekeys.convert_region_to_platform)
    def get_language_strings_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> LanguageStringsData:
        result = self.get_language_strings(query=query, context=context)
        if result._data[LanguageStringsData] is not None and result._Ghost__is_loaded(LanguageStringsData):
            return result._data[LanguageStringsData]
        else:
            raise NotFoundError

    # Map

    @get.register(Map)
    @validate_query(uniquekeys.validate_map_query, uniquekeys.convert_region_to_platform)
    def get_map(self, query: Mapping[str, Any], context: PipelineContext = None) -> Map:
        return self._get(Map, query, uniquekeys.for_map_query, context)

    @get_many.register(Map)
    @validate_query(uniquekeys.validate_many_map_query, uniquekeys.convert_region_to_platform)
    def get_many_map(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Map, None, None]:
        return self._get_many(Map, query, uniquekeys.for_many_map_query, context)

    @put.register(Map)
    def put_map(self, item: Map, context: PipelineContext = None) -> None:
        self._put(Map, item, uniquekeys.for_map, context=context)

    @put_many.register(Map)
    def put_many_map(self, items: Iterable[Map], context: PipelineContext = None) -> None:
        self._put_many(Map, items, uniquekeys.for_map, context=context)

    @get.register(MapData)
    @validate_query(uniquekeys.validate_map_query, uniquekeys.convert_region_to_platform)
    def get_map_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> MapData:
        result = self.get_map(query=query, context=context)
        if result._data[MapData] is not None and result._Ghost__is_loaded(MapData):
            return result._data[MapData]
        else:
            raise NotFoundError

    # Maps

    @get.register(Maps)
    @validate_query(uniquekeys.validate_maps_query, uniquekeys.convert_region_to_platform)
    def get_maps(self, query: Mapping[str, Any], context: PipelineContext = None) -> Maps:
        return self._get(Maps, query, uniquekeys.for_maps_query, context)

    @get_many.register(Maps)
    @validate_query(uniquekeys.validate_many_maps_query, uniquekeys.convert_region_to_platform)
    def get_many_maps(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Maps, None, None]:
        return self._get_many(Maps, query, uniquekeys.for_many_maps_query, context)

    @put.register(Maps)
    def put_maps(self, item: Maps, context: PipelineContext = None) -> None:
        self._put(Maps, item, uniquekeys.for_maps, context=context)
        for map in item:
            self._put(Map, map, uniquekeys.for_map, context=context)

    @put_many.register(Maps)
    def put_many_maps(self, items: Iterable[Maps], context: PipelineContext = None) -> None:
        self._put_many(Maps, items, uniquekeys.for_maps, context=context)

    # Profile Icon

    @get.register(ProfileIcon)
    @validate_query(uniquekeys.validate_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcon:
        return self._get(ProfileIcon, query, uniquekeys.for_profile_icon_query, context)

    @get_many.register(ProfileIcon)
    @validate_query(uniquekeys.validate_many_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_many_profile_icon(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIcon, None, None]:
        return self._get_many(ProfileIcon, query, uniquekeys.for_many_profile_icon_query, context)

    @put.register(ProfileIcon)
    def put_profile_icon(self, item: ProfileIcon, context: PipelineContext = None) -> None:
        self._put(ProfileIcon, item, uniquekeys.for_profile_icon, context=context)

    @put_many.register(ProfileIcon)
    def put_many_profile_icon(self, items: Iterable[ProfileIcon], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcon, items, uniquekeys.for_profile_icon, context=context)

    @get.register(ProfileIconData)
    @validate_query(uniquekeys.validate_profile_icon_query, uniquekeys.convert_region_to_platform)
    def get_profile_icon_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIconData:
        result = self.get_profile_icon(query=query, context=context)
        if result._data[ProfileIconData] is not None and result._Ghost__is_loaded(ProfileIconData):
            return result._data[ProfileIconData]
        else:
            raise NotFoundError

    # Profile Icons

    @get.register(ProfileIcons)
    @validate_query(uniquekeys.validate_profile_icons_query, uniquekeys.convert_region_to_platform)
    def get_profile_icons(self, query: Mapping[str, Any], context: PipelineContext = None) -> ProfileIcons:
        return self._get(ProfileIcons, query, uniquekeys.for_profile_icons_query, context)

    @get_many.register(ProfileIcons)
    @validate_query(uniquekeys.validate_many_profile_icons_query, uniquekeys.convert_region_to_platform)
    def get_many_profile_icons(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ProfileIcons, None, None]:
        return self._get_many(ProfileIcons, query, uniquekeys.for_many_profile_icons_query, context)

    @put.register(ProfileIcons)
    def put_profile_icons(self, item: ProfileIcons, context: PipelineContext = None) -> None:
        self._put(ProfileIcons, item, uniquekeys.for_profile_icons, context=context)
        for profile_icon in item:
            self._put(ProfileIcon, profile_icon, uniquekeys.for_profile_icon, context=context)

    @put_many.register(ProfileIcons)
    def put_many_profile_icons(self, items: Iterable[ProfileIcons], context: PipelineContext = None) -> None:
        self._put_many(ProfileIcons, items, uniquekeys.for_profile_icons, context=context)

    # Realm

    @get.register(Realms)
    @validate_query(uniquekeys.validate_realms_query, uniquekeys.convert_region_to_platform)
    def get_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Realms:
        return self._get(Realms, query, uniquekeys.for_realms_query, context)

    @get_many.register(Realms)
    @validate_query(uniquekeys.validate_many_realms_query, uniquekeys.convert_region_to_platform)
    def get_many_realms(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Realms, None, None]:
        return self._get_many(Realms, query, uniquekeys.for_many_realms_query, context)

    @put.register(Realms)
    def put_realms(self, item: Realms, context: PipelineContext = None) -> None:
        self._put(Realms, item, uniquekeys.for_realms, context=context)

    @put_many.register(Realms)
    def put_many_realms(self, items: Iterable[Realms], context: PipelineContext = None) -> None:
        self._put_many(Realms, items, uniquekeys.for_realms, context=context)

    @get.register(RealmData)
    @validate_query(uniquekeys.validate_realms_query, uniquekeys.convert_region_to_platform)
    def get_realms_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> RealmData:
        result = self.get_realms(query=query, context=context)
        if result._data[RealmData] is not None and result._Ghost__is_loaded(RealmData):
            return result._data[RealmData]
        else:
            raise NotFoundError

    # Rune

    @get.register(Rune)
    @validate_query(uniquekeys.validate_rune_query, uniquekeys.convert_region_to_platform)
    def get_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Rune:
        return self._get(Rune, query, uniquekeys.for_rune_query, context)

    @get_many.register(Rune)
    @validate_query(uniquekeys.validate_many_rune_query, uniquekeys.convert_region_to_platform)
    def get_many_rune(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Rune, None, None]:
        return self._get_many(Rune, query, uniquekeys.for_many_rune_query, context)

    @put.register(Rune)
    def put_rune(self, item: Rune, context: PipelineContext = None) -> None:
        self._put(Rune, item, uniquekeys.for_rune, context=context)

    @put_many.register(Rune)
    def put_many_rune(self, items: Iterable[Rune], context: PipelineContext = None) -> None:
        self._put_many(Rune, items, uniquekeys.for_rune, context=context)

    @get.register(RuneData)
    @validate_query(uniquekeys.validate_rune_query, uniquekeys.convert_region_to_platform)
    def get_rune_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> RuneData:
        result = self.get_rune(query=query, context=context)
        if result._data[RuneData] is not None and result._Ghost__is_loaded(RuneData):
            return result._data[RuneData]
        else:
            raise NotFoundError

    # Runes

    @get.register(Runes)
    @validate_query(uniquekeys.validate_runes_query, uniquekeys.convert_region_to_platform)
    def get_runes(self, query: Mapping[str, Any], context: PipelineContext = None) -> Runes:
        return self._get(Runes, query, uniquekeys.for_runes_query, context)

    @get_many.register(Runes)
    @validate_query(uniquekeys.validate_many_runes_query, uniquekeys.convert_region_to_platform)
    def get_many_runes(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Runes, None, None]:
        return self._get_many(Runes, query, uniquekeys.for_many_runes_query, context)

    @put.register(Runes)
    def put_runes(self, item: Runes, context: PipelineContext = None) -> None:
        self._put(Runes, item, uniquekeys.for_runes, context=context)
        for rune in item:
            self._put(Rune, rune, uniquekeys.for_rune, context=context)

    @put_many.register(Runes)
    def put_many_runes(self, items: Iterable[Runes], context: PipelineContext = None) -> None:
        self._put_many(Runes, items, uniquekeys.for_runes, context=context)

    # Summoner Spell

    @get.register(SummonerSpell)
    @validate_query(uniquekeys.validate_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpell:
        return self._get(SummonerSpell, query, uniquekeys.for_summoner_spell_query, context)

    @get_many.register(SummonerSpell)
    @validate_query(uniquekeys.validate_many_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner_spell(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpell, None, None]:
        return self._get_many(SummonerSpell, query, uniquekeys.for_many_summoner_spell_query, context)

    @put.register(SummonerSpell)
    def put_summoner_spell(self, item: SummonerSpell, context: PipelineContext = None) -> None:
        self._put(SummonerSpell, item, uniquekeys.for_summoner_spell, context=context)

    @put_many.register(SummonerSpell)
    def put_many_summoner_spell(self, items: Iterable[SummonerSpell], context: PipelineContext = None) -> None:
        self._put_many(SummonerSpell, items, uniquekeys.for_summoner_spell, context=context)

    @get.register(SummonerSpellData)
    @validate_query(uniquekeys.validate_summoner_spell_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spell_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpellData:
        result = self.get_summoner_spell(query=query, context=context)
        if result._data[SummonerSpellData] is not None and result._Ghost__is_loaded(SummonerSpellData):
            return result._data[SummonerSpellData]
        else:
            raise NotFoundError

    # Summoner Spells

    @get.register(SummonerSpells)
    @validate_query(uniquekeys.validate_summoner_spells_query, uniquekeys.convert_region_to_platform)
    def get_summoner_spells(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerSpells:
        return self._get(SummonerSpells, query, uniquekeys.for_summoner_spells_query, context)

    @get_many.register(SummonerSpells)
    @validate_query(uniquekeys.validate_many_summoner_spells_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner_spells(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[SummonerSpells, None, None]:
        return self._get_many(SummonerSpells, query, uniquekeys.for_many_summoner_spells_query, context)

    @put.register(SummonerSpells)
    def put_summoner_spells(self, item: SummonerSpells, context: PipelineContext = None) -> None:
        self._put(SummonerSpells, item, uniquekeys.for_summoner_spells, context=context)
        for summoner_spell in item:
            self._put(SummonerSpell, summoner_spell, uniquekeys.for_summoner_spell, context=context)

    @put_many.register(SummonerSpells)
    def put_many_summoner_spells(self, items: Iterable[SummonerSpells], context: PipelineContext = None) -> None:
        self._put_many(SummonerSpells, items, uniquekeys.for_summoner_spells, context=context)

    # Versions

    @get.register(Versions)
    @validate_query(uniquekeys.validate_versions_query, uniquekeys.convert_region_to_platform)
    def get_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Versions:
        return self._get(Versions, query, uniquekeys.for_versions_query, context=context)

    @get_many.register(Versions)
    @validate_query(uniquekeys.validate_many_versions_query, uniquekeys.convert_region_to_platform)
    def get_many_versions(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Versions, None, None]:
        return self._get_many(Versions, query, uniquekeys.for_many_versions_query, context=context)

    @put.register(Versions)
    def put_versions(self, item: Versions, context: PipelineContext = None) -> None:
        self._put(Versions, item, uniquekeys.for_versions, context=context)

    @put_many.register(Versions)
    def put_many_versions(self, items: Iterable[Versions], context: PipelineContext = None) -> None:
        self._put_many(Versions, items, uniquekeys.for_versions, context=context)

    ##############
    # Status API #
    ##############

    @get.register(ShardStatus)
    @validate_query(uniquekeys.validate_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> ShardStatus:
        return self._get(ShardStatus, query, uniquekeys.for_shard_status_query, context)

    @get_many.register(ShardStatus)
    @validate_query(uniquekeys.validate_many_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_many_shard_status(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[ShardStatus, None, None]:
        return self._get_many(ShardStatus, query, uniquekeys.for_many_shard_status_query, context)

    @put.register(ShardStatus)
    def put_shard_status(self, item: ShardStatus, context: PipelineContext = None) -> None:
        self._put(ShardStatus, item, uniquekeys.for_shard_status, context=context)

    @put_many.register(ShardStatus)
    def put_many_shard_status(self, items: Iterable[ShardStatus], context: PipelineContext = None) -> None:
        self._put_many(ShardStatus, items, uniquekeys.for_shard_status, context=context)

    @get.register(ShardStatusData)
    @validate_query(uniquekeys.validate_shard_status_query, uniquekeys.convert_region_to_platform)
    def get_shard_status_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> ShardStatusData:
        result = self.get_shard_status(query=query, context=context)
        if result._data[ShardStatusData] is not None and result._Ghost__is_loaded(ShardStatusData):
            return result._data[ShardStatusData]
        else:
            raise NotFoundError

    #############
    # Match API #
    #############

    @get.register(Match)
    @validate_query(uniquekeys.validate_match_query, uniquekeys.convert_to_continent)
    def get_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Match:
        return self._get(Match, query, uniquekeys.for_match_query, context)

    @get_many.register(Match)
    @validate_query(uniquekeys.validate_many_match_query, uniquekeys.convert_to_continent)
    def get_many_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Match, None, None]:
        return self._get_many(Match, query, uniquekeys.for_many_match_query, context)

    @put.register(Match)
    def put_match(self, item: Match, context: PipelineContext = None) -> None:
        self._put(Match, item, uniquekeys.for_match, context=context)

    @put_many.register(Match)
    def put_many_match(self, items: Iterable[Match], context: PipelineContext = None) -> None:
        self._put_many(Match, items, uniquekeys.for_match, context=context)

    @get.register(MatchData)
    @validate_query(uniquekeys.validate_match_query, uniquekeys.convert_to_continent)
    def get_match_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> MatchData:
        result = self.get_match(query=query, context=context)
        if result._data[MatchData] is not None and result._Ghost__is_loaded(MatchData):
            return result._data[MatchData]
        else:
            raise NotFoundError

    # Timeline

    @get.register(Timeline)
    @validate_query(uniquekeys.validate_match_timeline_query, uniquekeys.convert_to_continent)
    def get_match_timeline(self, query: Mapping[str, Any], context: PipelineContext = None) -> Timeline:
        return self._get(Timeline, query, uniquekeys.for_match_timeline_query, context)

    @get_many.register(Timeline)
    @validate_query(uniquekeys.validate_many_match_timeline_query, uniquekeys.convert_to_continent)
    def get_many_match_timeline(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Timeline, None, None]:
        return self._get_many(Timeline, query, uniquekeys.for_many_match_timeline_query, context)

    @put.register(Timeline)
    def put_match_timeline(self, item: Timeline, context: PipelineContext = None) -> None:
        self._put(Timeline, item, uniquekeys.for_match_timeline, context=context)

    @put_many.register(Timeline)
    def put_many_match_timeline(self, items: Iterable[Timeline], context: PipelineContext = None) -> None:
        self._put_many(Timeline, items, uniquekeys.for_match_timeline, context=context)

    @get.register(TimelineData)
    @validate_query(uniquekeys.validate_match_timeline_query, uniquekeys.convert_to_continent)
    def get_match_timeline_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> TimelineData:
        result = self.get_match_timeline(query=query, context=context)
        if result._data[TimelineData] is not None and result._Ghost__is_loaded(TimelineData):
            return result._data[TimelineData]
        else:
            raise NotFoundError

    #################
    # Spectator API #
    #################

    # Current Match

    @get.register(CurrentMatch)
    @validate_query(uniquekeys.validate_current_match_query, uniquekeys.convert_region_to_platform)
    def get_current_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> CurrentMatch:
        return self._get(CurrentMatch, query, uniquekeys.for_current_match_query, context)

    @get_many.register(CurrentMatch)
    @validate_query(uniquekeys.validate_many_current_match_query, uniquekeys.convert_region_to_platform)
    def get_many_current_match(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[CurrentMatch, None, None]:
        return self._get_many(CurrentMatch, query, uniquekeys.for_many_current_match_query, context)

    @put.register(CurrentMatch)
    def put_current_match(self, item: CurrentMatch, context: PipelineContext = None) -> None:
        self._put(CurrentMatch, item, uniquekeys.for_current_match, context=context)

    @put_many.register(CurrentMatch)
    def put_many_current_match(self, items: Iterable[CurrentMatch], context: PipelineContext = None) -> None:
        self._put_many(CurrentMatch, items, uniquekeys.for_current_match, context=context)

    @get.register(CurrentGameInfoData)
    @validate_query(uniquekeys.validate_current_match_query, uniquekeys.convert_region_to_platform)
    def get_current_match_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> CurrentGameInfoData:
        result = self.get_current_match(query=query, context=context)
        if result._data[CurrentGameInfoData] is not None and result._Ghost__is_loaded(CurrentGameInfoData):
            return result._data[CurrentGameInfoData]
        else:
            raise NotFoundError

    # Featured Matches

    @get.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> FeaturedMatches:
        return self._get(FeaturedMatches, query, uniquekeys.for_featured_matches_query, context)

    @get_many.register(FeaturedMatches)
    @validate_query(uniquekeys.validate_many_featured_matches_query, uniquekeys.convert_region_to_platform)
    def get_many_featured_matches(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[FeaturedMatches, None, None]:
        return self._get_many(FeaturedMatches, query, uniquekeys.for_many_featured_matches_query, context)

    @put.register(FeaturedMatches)
    def put_featured_matches(self, item: FeaturedMatches, context: PipelineContext = None) -> None:
        self._put(FeaturedMatches, item, uniquekeys.for_featured_matches, context=context)

    @put_many.register(FeaturedMatches)
    def put_many_featured_matches(self, items: Iterable[FeaturedMatches], context: PipelineContext = None) -> None:
        self._put_many(FeaturedMatches, items, uniquekeys.for_featured_matches, context=context)

    ################
    # Summoner API #
    ################

    @get.register(Summoner)
    @validate_query(uniquekeys.validate_summoner_query, uniquekeys.convert_region_to_platform)
    def get_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Summoner:
        return self._get(Summoner, query, uniquekeys.for_summoner_query, context)

    @get_many.register(Summoner)
    @validate_query(uniquekeys.validate_many_summoner_query, uniquekeys.convert_region_to_platform)
    def get_many_summoner(self, query: Mapping[str, Any], context: PipelineContext = None) -> Generator[Summoner, None, None]:
        return self._get_many(Summoner, query, uniquekeys.for_many_summoner_query, context)

    @put.register(Summoner)
    def put_summoner(self, item: Summoner, context: PipelineContext = None) -> None:
        self._put(Summoner, item, uniquekeys.for_summoner, context=context)

    @put_many.register(Summoner)
    def put_many_summoner(self, items: Iterable[Summoner], context: PipelineContext = None) -> None:
        self._put_many(Summoner, items, uniquekeys.for_summoner, context=context)

    @get.register(SummonerData)
    @validate_query(uniquekeys.validate_summoner_query, uniquekeys.convert_region_to_platform)
    def get_summoner_data(self, query: Mapping[str, Any], context: PipelineContext = None) -> SummonerData:
        result = self.get_summoner(query=query, context=context)
        if result._data[SummonerData] is not None and result._Ghost__is_loaded(SummonerData):
            return result._data[SummonerData]
        else:
            raise NotFoundError
