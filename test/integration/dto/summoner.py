from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/summoner tests...")
    test_summoners_by_name()
    test_summoners_by_id()
    test_summoner_masteries()
    test_summoner_names()
    test_summoner_runes()


def test_summoners_by_name():
    int_test_handler.test_result(baseriotapi.get_summoners_by_name(int_test_handler.summoner_name))


def test_summoners_by_id():
    int_test_handler.test_result(baseriotapi.get_summoners_by_id(int_test_handler.summoner_id))


def test_summoner_masteries():
    int_test_handler.test_result(baseriotapi.get_summoner_masteries(int_test_handler.summoner_id))


def test_summoner_names():
    int_test_handler.test_result(baseriotapi.get_summoner_names(int_test_handler.summoner_id))


def test_summoner_runes():
    int_test_handler.test_result(baseriotapi.get_summoner_runes(int_test_handler.summoner_id))
