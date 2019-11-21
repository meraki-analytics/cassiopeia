from collections import Counter
import random

import cassiopeia as cass
from cassiopeia import Season, Queue, Summoner, Match, Champion, Champions, ChampionMastery, Item, Items, LanguageStrings, Map, Locales, Runes, Rune, ShardStatus, FeaturedMatches, SummonerSpell, SummonerSpells, GameMode, VerificationString, Role

import os, pytest

def test_versions():
    versions = cass.get_versions(region="NA")
    versions[0]
    versions.region
    versions = cass.get_versions(region="NA")
    versions[0]


def test_realms():
    realms = cass.get_realms(region="NA")
    realms.latest_versions


def test_match():
    name = "Kalturi"
    region = "NA"

    summoner = Summoner(name=name, region=region)

    match_history = cass.get_match_history(summoner, queues={Queue.ranked_solo_fives})
    match_history = summoner.match_history
    match_history(seasons={Season.season_7}, queues={Queue.ranked_solo_fives})

    champion_id_to_name_mapping = {champion.id: champion.name for champion in cass.get_champions(region=region)}
    played_champions = Counter()
    for match in match_history:
        champion_id = match.participants[summoner.name].champion.id
        champion_name = champion_id_to_name_mapping[champion_id]
        played_champions[champion_name] += 1

    for champion_name, count in played_champions.most_common(10):
        champion_name, count

    match = match_history[0]
    match.id

    p = match.participants[summoner]
    p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id

    for p in match.participants:
        p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon

    for p in match.participants:
        p.id, p.summoner.region, p.summoner.account_id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon

    match.blue_team.win
    match.red_team.win
    for p in match.blue_team.participants:
        p.summoner.name


def test_champions():
    champions = Champions(region="NA")
    for champion in champions:
        champion.name, champion.id

    annie = Champion(name="Annie", region="NA")
    annie.name
    annie.title
    for spell in annie.spells:
        spell.name, spell.keywords

    annie.info.difficulty
    annie.passive.name
    {item.name: count for item, count in annie.recommended_itemsets[0].item_sets[0].items.items()}
    annie.free_to_play
    annie._Ghost__all_loaded

    ziggs = cass.get_champion("Ziggs", region="NA")
    ziggs.name
    ziggs.region
    {item.name: count for item, count in ziggs.recommended_itemsets[0].item_sets[0].items.items()}
    ziggs.free_to_play
    for spell in ziggs.spells:
        for var in spell.variables:
            spell.name, var
    ziggs._Ghost__all_loaded


def test_championmastery():
    me = Summoner(name="Kalturi", region="NA")
    karma = Champion(name="Karma", id=43, region="NA")
    cm = ChampionMastery(champion=karma, summoner=me, region="NA")
    cm = cass.get_champion_mastery(champion=karma, summoner=me, region="NA")
    'Champion ID:', cm.champion.id
    'Mastery points:', cm.points
    'Mastery Level:', cm.level
    'Points until next level:', cm.points_until_next_level

    cms = cass.get_champion_masteries(summoner=me, region="NA")
    cms = me.champion_masteries
    cms[0].points
    cms["Karma"].points  # Does a ton of calls without a cache

    "{} has mastery level 6 or higher on:".format(me.name)
    pro = cms.filter(lambda cm: cm.level >= 6)
    [cm.champion.name for cm in pro]


def test_items():
    dagger = Item(name="Dagger", region="NA")
    dagger.name
    dagger.id
    items = cass.get_items(region="NA")
    for item in items:
        item.name
    items = cass.get_items(region="NA")
    items[10].name
    dagger = Item(name="Dagger", region="NA")
    dagger.name, dagger.id
    items = Items(region="NA")
    items[10].name


def test_languagestrings():
    language_strings = cass.get_language_strings(region="NA")
    assert len(language_strings.strings) > 0

def test_leagues():
    summoner_name = "Kalturi"
    region = "NA"
    summoner = Summoner(name=summoner_name, region=region)
    "Name:", summoner.name
    "ID:", summoner.id

    # entries = cass.get_league_entries(summoner, region=region)
    entries = summoner.league_entries
    if entries.fives.promos is not None:
        # If the summoner is in their promos, print some info
        "Promos progress:", entries.fives.promos.progress
        "Promos wins", entries.fives.promos.wins
        "Promos losses:", entries.fives.promos.losses
        "Games not yet played in promos:", entries.fives.promos.not_played
        "Number of wins required to win promos:", entries.fives.promos.wins_required
    else:
        "The summoner is not in their promos."

    "Name and id of fives leagues this summoner is in:"
    entries.fives.league.name
    entries.fives.league.id
    f"Listing all summoners in {entries.fives.league.id}"
    for entry in entries.fives.league.entries:
        entry.summoner.name, entry.league_points, entries.fives.league.tier, entry.division

    "Challenger League name and id:"
    challenger = cass.get_challenger_league(queue=Queue.ranked_solo_fives, region=region)
    # challenger.name
    challenger.id

    "Grandmaster League name and id:"
    grandmaster = cass.get_grandmaster_league(queue=Queue.ranked_solo_fives, region=region)
    # grandmaster.name
    grandmaster.id

    "Master League name and id:"
    master = cass.get_master_league(queue=Queue.ranked_solo_fives, region=region)
    # master.name
    master.id

def test_locales():
    locales = cass.get_locales(region="NA")
    for locale in locales:
        locale
    assert len(locales) > 10


def test_maps():
    maps = cass.get_maps(region="NA")
    for map in maps:
        map.name, map.id

    map = Map(name="Summoner's Rift", region="NA")
    map.id


def test_profileicons():
    profile_icons = cass.get_profile_icons(region="NA")
    for pi in profile_icons:
        pi.name, pi.id
    profile_icons[10].name


def test_readme():
    summoner = cass.get_summoner(name="Kalturi", region="NA")
    "{name} is a level {level} summoner on the {region} server.".format(name=summoner.name, level=summoner.level, region=summoner.region)
    champions = cass.get_champions(region="NA")
    random_champion = random.choice(champions)
    "He enjoys playing champions such as {name}.".format(name=random_champion.name)

    challenger_league = cass.get_challenger_league(queue=cass.Queue.ranked_solo_fives, region="NA")
    best_na = challenger_league[0].summoner
    "He's not as good as {name} at League, but probably a better python programmer!".format(name=best_na.name)


def test_runes():
    for rune in cass.get_runes(region="NA").keystones:
        rune.name, rune.id, rune.path, rune.tier
        assert rune.is_keystone


def test_shards():
    status = cass.get_status(region="NA")
    status = ShardStatus(region="NA")
    status.name


def test_spectator():
    featured_matches = cass.get_featured_matches(region="NA")
    for match in featured_matches:
        match.region, match.id

    match = featured_matches[0]
    a_summoner_name = match.blue_team.participants[0].summoner.name
    match.queue
    summoner = Summoner(name=a_summoner_name, region=match.region)
    current_match = summoner.current_match
    current_match.map.name

    for participant in current_match.blue_team.participants:
        participant.summoner.name


def test_summoner():
    name = "Kalturi"
    region = "NA"
    summoner = Summoner(name=name, region=region)
    "Name:", summoner.name
    "ID:", summoner.id
    "Account ID:", summoner.account_id
    "Level:", summoner.level
    "Revision date:", summoner.revision_date
    "Profile icon ID:", summoner.profile_icon.id
    "Profile icon name:", summoner.profile_icon.name
    "Profile icon URL:", summoner.profile_icon.url
    "Profile icon image:", summoner.profile_icon.image


def test_summonerspells():
    sspells = cass.get_summoner_spells(region="NA")
    for sspell in sspells:
        if set(sspell.modes) & {GameMode.classic, GameMode.aram, GameMode.poro_king, GameMode.ascension}:
            "Name:", sspell.name
            "Description:", sspell.description

    sspell = SummonerSpell(name="Ghost", region="NA")
    sspell.description


def test_timeline():
    name = "Kalturi"
    region = "NA"
    summoner = Summoner(name=name, region=region)
    match_history = summoner.match_history
    match = match_history[0]
    'Match ID:', match.id

    match.timeline.frame_interval
    for frame in match.timeline.frames:
        for event in frame.events:
            event.type

    for p in match.participants:
        for event in p.timeline.events:
            event.type
