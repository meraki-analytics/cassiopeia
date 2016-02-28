"""
This example is one of the simplest but most useful.

It creates a dictionary mapping of champion IDs to champion names,
and simply prints that dictionary.
"""

import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(True)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    champions = riotapi.get_champions()
    mapping = {champion.id: champion.name for champion in champions}

    print(mapping)

    print()

    # Annie's champion ID is 1, so this will print "Annie"
    print(mapping[1])


if __name__ == "__main__":
    main()
