from unittest import TestCase

from cassiopeia import riotapi
from cassiopeia.type.api.exception import APIError


class Python2And3Tests(TestCase):

    def test_we_can_use_unicode(self):
        # We shouldn't check if str instead check if NOT Region
        riotapi.set_region(u"NA")
        assert True

    def test_super_imported_from_future(self):
        # Make sure we have from future.builtins.misc import super
        APIError("Some message", 123)
        assert True
