import os
import pytest


def pytest_runtest_setup(item):
    # Skip all these tests if we don't have RIOT_API_KEY env var
    if not os.environ.get("RIOT_API_KEY"):
        pytest.skip('No RIOT_API_KEY env var found')
