import cassiopeia as cass
from cassiopeia.core import Summoner


def print_leagues(summoner_name: str, region: str):
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    # leagues = cass.get_leagues(summoner)
    leagues = summoner.leagues
    for league in leagues:
        print(league.name)

    print()
    print(leagues.fives.name)
    for entry in leagues.fives:
        print(entry.summoner.name, entry.league_points)


if __name__ == "__main__":
    print_leagues("Kalturi", "NA")
