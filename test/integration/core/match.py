from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/matchapi tests...")
    test_match()
    test_matches()


def test_match():
    int_test_handler.test_result(riotapi.get_match(int_test_handler.match_id))


def test_matches():
    int_test_handler.test_result(riotapi.get_matches([int_test_handler.match_id]))
