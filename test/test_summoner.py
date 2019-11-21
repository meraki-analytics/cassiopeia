import os
import unittest

import cassiopeia

from .constants import SUMMONER_NAME, UNKNOWN_SUMMONER_NAME


class TestSummoner(unittest.TestCase):
    def setUp(self):
        cassiopeia.apply_settings(cassiopeia.get_default_config())
        cassiopeia.set_riot_api_key(os.environ.get('RIOT_API_KEY'))
        cassiopeia.apply_settings({"global": {"default_region": "NA"}})

    def test_unknown_summoner(self):
        for e in cassiopeia.Summoner(name="Kalturi", region="NA").league_entries: print(e.league.name)
        self.assertFalse(cassiopeia.get_summoner(name=UNKNOWN_SUMMONER_NAME, region="NA").exists)

    def test_ranks(self):
        s = cassiopeia.Summoner(name=SUMMONER_NAME)
        ranks = s.ranks
        for key in ranks:
            self.assertIsInstance(key, cassiopeia.Queue)
            self.assertIsInstance(ranks[key], cassiopeia.data.Rank)

    def test_access_properties(self):
        s = cassiopeia.Summoner(name=SUMMONER_NAME)
        self.assertIsNotNone(s.region)
        self.assertIsNotNone(s.platform)
        self.assertIsNotNone(s.account_id)
        self.assertIsNotNone(s.puuid)
        self.assertIsNotNone(s.id)
        self.assertIsNotNone(s.name)
        self.assertIsNotNone(s.sanitized_name)
        self.assertIsNotNone(s.level)
        self.assertIsNotNone(s.profile_icon)
        self.assertIsNotNone(s.revision_date)
        self.assertIsNotNone(s.match_history_uri)
        self.assertIsNotNone(s.champion_masteries)
        self.assertIsNotNone(s.match_history)
        self.assertIsNotNone(s.league_entries)
        #self.assertIsNotNone(s.rank_last_season)

    def test_equality(self):
        from_name = cassiopeia.get_summoner(name=SUMMONER_NAME, region="NA")
        from_id = cassiopeia.get_summoner(id=from_name.id, region="NA")
        self.assertEqual(from_name.id, from_id.id)
        self.assertEqual(from_name.name, from_id.name)
        self.assertEqual(from_name, from_id)
        self.assertEqual(from_name.to_dict(), from_id.to_dict())


if __name__ == "__main__":
    unittest.main()
