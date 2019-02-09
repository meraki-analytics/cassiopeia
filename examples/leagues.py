import cassiopeia as cass
from cassiopeia.data import Queue, Position
from cassiopeia.core import Summoner


def print_leagues(summoner_name: str, region: str):
    summoner = Summoner(name=summoner_name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)

    # positions = cass.get_league_positions(summoner, region=region)
    positions = summoner.league_positions
    if positions.fives.promos is not None:
        # If the summoner is in their promos, print some info
        print("Promos progress:", positions.fives.promos.progress)
        print("Promos wins", positions.fives.promos.wins)
        print("Promos losses:", positions.fives.promos.losses)
        print("Games not yet played in promos:", positions.fives.promos.not_played)
        print("Number of wins required to win promos:", positions.fives.promos.wins_required)
    else:
        print("The summoner is not in their promos.")

    print("Name of leagues this summoner is in:")
    for league in positions:
        print(league.name)
    print()

    leagues = summoner.leagues
    print(f"Listing all summoners in this league:")
    for entry in leagues.fives[Position.utility]:
        print(entry.summoner.name, entry.league_points, entry.tier, entry.division, entry.position)

    print()
    print("Master's League name:")
    masters = cass.get_master_league(queue=Queue.ranked_solo_fives, region=region)
    print(masters.name)

if __name__ == "__main__":
    print_leagues("Kalturi", "NA")
