"""
This example pulls Dyrus' summoner information and then makes a current game
request to see if he is in game or not.
"""

import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"]  # You can create an env var called "DEV_KEY" that holds your developer key. It will be loaded here.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    summoner = riotapi.get_summoner_by_name("Dyrs")  # SummonerID is 5908
    # dyrus = riotapi.get_summoner_by_id(5908)  # You could use this as well

    current_game = riotapi.get_current_game(summoner)
    if current_game is None:
        print("{0} is not in-game!".format(summoner))
    else:
        print("{0} is in-game!".format(summoner))


if __name__ == "__main__":
    main()
