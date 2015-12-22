from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/team tests...")
    test_teams_by_summoner()
    test_teams()


def test_teams_by_summoner():
    int_test_handler.test_result(riotapi.get_teams_by_summoner(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))


def test_teams():
    int_test_handler.test_result(riotapi.get_teams([int_test_handler.team_id]))
