from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/summoner tests...")
    test_summoner_by_name()
    test_summoners_by_name()
    test_summoner_by_id()
    test_summoners_by_id()
    test_mastery_pages()
    test_summoner_name()
    test_summoner_names()
    test_rune_pages()


def test_summoner_by_name():
    int_test_handler.test_result(riotapi.get_summoner_by_name(int_test_handler.summoner_name))


def test_summoners_by_name():
    int_test_handler.test_result(riotapi.get_summoners_by_name([int_test_handler.summoner_name]))


def test_summoner_by_id():
    int_test_handler.test_result(riotapi.get_summoner_by_id(int_test_handler.summoner_id))


def test_summoners_by_id():
    int_test_handler.test_result(riotapi.get_summoners_by_id([int_test_handler.summoner_id]))


def test_mastery_pages():
    int_test_handler.test_result(riotapi.get_mastery_pages(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))


def test_summoner_name():
    int_test_handler.test_result(riotapi.get_summoner_name(int_test_handler.summoner_id))


def test_summoner_names():
    int_test_handler.test_result(riotapi.get_summoner_names([int_test_handler.summoner_id]))


def test_rune_pages():
    int_test_handler.test_result(riotapi.get_rune_pages(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))
