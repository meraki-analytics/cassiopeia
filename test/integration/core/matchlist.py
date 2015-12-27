from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/matchlistapi tests...")
    test_match_list()


def test_match_list():
    int_test_handler.test_result(riotapi.get_match_list(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))
