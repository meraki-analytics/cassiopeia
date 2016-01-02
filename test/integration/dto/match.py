from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/matchapi tests...")
    test_match()


def test_match():
    int_test_handler.test_result(baseriotapi.get_match(int_test_handler.match_id))
