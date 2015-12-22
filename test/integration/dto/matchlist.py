from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/matchlistapi tests...")
    test_match_list()


def test_match_list():
    int_test_handler.test_result(baseriotapi.get_match_list(int_test_handler.summoner_id))
