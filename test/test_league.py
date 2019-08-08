import os
import unittest

from cassiopeia import cassiopeia
from .constants import LEAGUE_UUID, UNKNOWN_SUMMONER_NAME


class TestLeague(unittest.TestCase):
    def setUp(self):
        cassiopeia.apply_settings(cassiopeia.get_default_config())
        cassiopeia.set_riot_api_key(os.environ.get('RIOT_API_KEY'))
        cassiopeia.apply_settings({"global": {"default_region": "NA"}})

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
        self.assertIsNotNone(entry.league_id)
        self.assertIsNotNone(entry.queue)
        self.assertIsNotNone(entry.name)
        self.assertIsNotNone(entry.tier)
        self.assertIsNotNone(entry.division)
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


if __name__ == "__main__":
    unittest.main()
