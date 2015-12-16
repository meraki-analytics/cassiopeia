import os
from cassiopeia import riotapi
from cassiopeia.type.core.common import LoadPolicy


def main():
    # Setup riotapi
    riotapi.set_region("NA")
    riotapi.print_calls(False)
    key = os.environ["DEV_KEY"] # You can create an env var called "DEV_KEY" that holds your developer key.
    riotapi.set_api_key(key)
    riotapi.set_load_policy(LoadPolicy.lazy)

    summoner = riotapi.get_summoner_by_name("Dyrs") # SummonerID is 5908

    current_game = riotapi.get_current_game(summoner)
    if current_game is None:
        print("{0} is not in-game!".format(summoner))
    else:
        print("{0} is in-game!".format(summoner))


if __name__ == "__main__":
    main()
