from unittest import TestCase

from cassiopeia import riotapi


class Python2And3Tests(TestCase):

    def test_we_can_use_unicode(self):
        riotapi.set_region(u"NA")
        assert True
