from cassiopeia import baseriotapi
from .. import int_test_handler


def test_all():
    print("dto/stats tests...")
    test_ranked_stats()
    test_stats()


def test_ranked_stats():
    int_test_handler.test_result(baseriotapi.get_ranked_stats(int_test_handler.summoner_id))


def test_stats():
    int_test_handler.test_result(baseriotapi.get_stats(int_test_handler.summoner_id))
