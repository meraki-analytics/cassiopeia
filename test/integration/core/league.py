from cassiopeia import riotapi
from .. import int_test_handler


def test_all():
    print("core/leagueapi tests...")
    test_leagues_by_summoner()
    test_league_entries_by_summoner()
    test_leagues_by_team()
    test_league_entries_by_team()
    test_challenger()
    test_master()


def test_leagues_by_summoner():
    int_test_handler.test_result(riotapi.get_leagues_by_summoner(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))


def test_league_entries_by_summoner():
    int_test_handler.test_result(riotapi.get_league_entries_by_summoner(riotapi.get_summoner_by_id(int_test_handler.summoner_id)))


def test_leagues_by_team():
    int_test_handler.test_result(riotapi.get_leagues_by_team(riotapi.get_team(int_test_handler.team_id)))


def test_league_entries_by_team():
    int_test_handler.test_result(riotapi.get_league_entries_by_team(riotapi.get_team(int_test_handler.team_id)))


def test_challenger():
    int_test_handler.test_result(riotapi.get_challenger())


def test_master():
    int_test_handler.test_result(riotapi.get_master())
