import os
import unittest

import cassiopeia

class TestItems(unittest.TestCase):
    def setUp(self):
        cassiopeia.apply_settings(cassiopeia.get_default_config())
        cassiopeia.set_riot_api_key(os.environ.get('RIOT_API_KEY'))

    def test_items_from_different_versions(self):
        versions = [cassiopeia.Versions()[0], "6.5.1"]

        for version in versions:
            with self.subTest(version=version):
                items = cassiopeia.Items(version=version)
                self.assertIsNotNone(items.region)
                self.assertIsNotNone(items.version)

                item = items[0]
                self.assertIsNotNone(item.id)


