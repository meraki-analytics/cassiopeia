import io
import os
import unittest
from unittest.mock import patch

from cassiopeia import cassiopeia
from .constants import LEAGUE_UUID, SUMMONER_NAME


class TestLeague(unittest.TestCase):
    def setUp(self):
        cassiopeia.apply_settings(cassiopeia.get_default_config())
        cassiopeia.set_riot_api_key(os.environ.get('RIOT_API_KEY'))

    def test_access_league_properties(self):
        lg = cassiopeia.League(id=LEAGUE_UUID)
        self.assertIsNotNone(lg.region)
        self.assertIsNotNone(lg.platform)
        self.assertEqual(lg.id, LEAGUE_UUID)
        self.assertIsNotNone(lg.tier)
        self.assertIsNotNone(lg.queue)
        self.assertIsNotNone(lg.name)
        self.assertIsNotNone(lg.entries)

    def test_access_league_entry_properties(self):
        entry = cassiopeia.League(id=LEAGUE_UUID).entries[0]
        self.assertIsNotNone(entry.region)
        self.assertIsNotNone(entry.platform)
        self.assertIsNotNone(entry.tier)
        self.assertIsNotNone(entry.division)
        # self.assertIsNotNone(entry.queue)
        self.assertIsNotNone(entry.hot_streak)
        self.assertIsNotNone(entry.wins)
        self.assertIsNotNone(entry.veteran)
        self.assertIsNotNone(entry.losses)
        self.assertIsNotNone(entry.summoner)
        self.assertIsNotNone(entry.fresh_blood)
        self.assertEqual(entry.league, cassiopeia.League(id=LEAGUE_UUID))
        self.assertIsNotNone(entry.league_points)
        self.assertIsNotNone(entry.inactive)
        # self.assertIsNotNone(entry.role)

    @patch('sys.stdout', new_callable=io.StringIO)
    def test_get_id_no_call_to_league(self, patched_log):
        s = cassiopeia.Summoner(name=SUMMONER_NAME)
        s.league_entries[0].league.id
        full_http_call_log = patched_log.getvalue()
        log_lines = full_http_call_log.splitlines()

        # check that there were 2 http calls: one to get summoner and one to get league entries
        self.assertEqual(len(log_lines), 2)
        get_summoner_call = log_lines[0]
        get_league_entries_call = log_lines[1]

        self.assertTrue('summoner/v4/summoners/by-name' in get_summoner_call)
        self.assertTrue('league/v4/entries/by-summoner' in get_league_entries_call)

        # check that league endpoint wasn't called to get id
        self.assertFalse('league/v4/leagues' in full_http_call_log)


if __name__ == "__main__":
    unittest.main()
