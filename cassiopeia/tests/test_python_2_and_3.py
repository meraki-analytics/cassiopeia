from unittest import TestCase


class Python2And3Tests(TestCase):

    def test_we_can_import_cass(self):
        from cassiopeia import riotapi
        riotapi.set_region("NA")

        assert True
