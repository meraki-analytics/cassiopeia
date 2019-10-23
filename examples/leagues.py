import cassiopeia as cass
from cassiopeia.data import Queue, Position
from cassiopeia.core import Summoner


def print_leagues(summoner_name: str, region: str):
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    # entries = cass.get_league_entries(summoner, region=region)
    entries = summoner.league_entries
    if entries.fives.promos is not None:
        # If the summoner is in their promos, print some info
        print("Promos progress:", entries.fives.promos.progress)
        print("Promos wins", entries.fives.promos.wins)
        print("Promos losses:", entries.fives.promos.losses)
        print("Games not yet played in promos:", entries.fives.promos.not_played)
        print("Number of wins required to win promos:", entries.fives.promos.wins_required)
    else:
        print("The summoner is not in their promos.")

    print("Name of leagues this summoner is in:")
    for entry in entries:
        print(entry.league.name)
    print()

    print(f"Listing all summoners in this league:")
    for position, entry in enumerate(entries.fives.league.entries):
        print(entry.summoner.name, entry.league_points, entry.tier, entry.division, position)

    print()
    print("Master's League name:")
    masters = cass.get_master_league(queue=Queue.ranked_solo_fives, region=region)
    print(masters.name)

if __name__ == "__main__":
    print_leagues("Kalturi", "NA")
