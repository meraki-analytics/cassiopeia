from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/staticdataapi tests...")
    test_champion_by_id()
    test_champion_by_name()
    test_champions()
    test_champions_by_id()
    test_champions_by_name()
    test_item()
    test_items()
    test_language_strings()
    test_languages()
    test_map_information()
    test_mastery()
    test_masteries()
    test_realm()
    test_rune()
    test_runes()
    test_summoner_spell()
    test_summoner_spells()
    test_versions()


def test_champion_by_id():
    int_test_handler.test_result(riotapi.get_champion_by_id(int_test_handler.champion_id))


def test_champion_by_name():
    int_test_handler.test_result(riotapi.get_champion_by_name(int_test_handler.champion_name))


def test_champions():
    int_test_handler.test_result(riotapi.get_champions())


def test_champions_by_id():
    int_test_handler.test_result(riotapi.get_champions_by_id([int_test_handler.champion_id]))


def test_champions_by_name():
    int_test_handler.test_result(riotapi.get_champions_by_name([int_test_handler.champion_name]))


def test_item():
    int_test_handler.test_result(riotapi.get_item(int_test_handler.item_id))


def test_items():
    int_test_handler.test_result(riotapi.get_items())


def test_language_strings():
    int_test_handler.test_result(riotapi.get_language_strings())


def test_languages():
    int_test_handler.test_result(riotapi.get_languages())


def test_map_information():
    int_test_handler.test_result(riotapi.get_map_information())


def test_mastery():
    int_test_handler.test_result(riotapi.get_mastery(int_test_handler.mastery_id))


def test_masteries():
    int_test_handler.test_result(riotapi.get_masteries())


def test_realm():
    int_test_handler.test_result(riotapi.get_realm())


def test_rune():
    int_test_handler.test_result(riotapi.get_rune(int_test_handler.rune_id))


def test_runes():
    int_test_handler.test_result(riotapi.get_runes())


def test_summoner_spell():
    int_test_handler.test_result(riotapi.get_summoner_spell(int_test_handler.summoner_spell_id))


def test_summoner_spells():
    int_test_handler.test_result(riotapi.get_summoner_spells())


def test_versions():
    int_test_handler.test_result(riotapi.get_versions())
