from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/stats tests...")
    test_ranked_stats()
    test_stats()


def test_ranked_stats():
    int_test_handler.test_result(riotapi.get_ranked_stats(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))


def test_stats():
    int_test_handler.test_result(riotapi.get_stats(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))
