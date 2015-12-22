import os
import pytest


pytestmark = pytest.mark.skipif(not os.environ.get("RIOT_API_KEY"))
