import cassiopeia as cass
from cassiopeia import Account, Summoner, Match
from cassiopeia.data import Queue
from collections import Counter


def print_newest_match(name: str, tagline: str, region: str):

    # Notice how this function never makes a call to the summoner endpoint because we provide all the needed data!

    account = Account(name=name, tagline=tagline, region=region)
    summoner = account.summoner

    # A MatchHistory is a lazy list, meaning it's elements only get loaded as-needed.

    match_history = cass.get_match_history(
        continent=summoner.region.continent,
        puuid=summoner.puuid,
        queue=Queue.ranked_solo_fives,
    )
    # match_history = summoner.match_history

    match = match_history[0]
    print("Match ID:", match.id)

    print("\nNow pull the full match data by iterating over all the participants:")
    for p in match.participants:
        p.summoner.load()
        print(f"{p.account.name} with ID {p.summoner.id} played {p.champion.name}")
    print()
    print("Iterate over all the participants again and note the data is not repulled:")
    for p in match.participants:
        print(f"{p.account.name} with ID {p.summoner.id} played {p.champion.name}")
    print()

    print("Blue team won?", match.blue_team.win)
    print("Red team won?", match.red_team.win)
    print()

    print("Participants on blue team:")
    for p in match.blue_team.participants:
        print(f"{p.account.name}: {p.champion.name}")
    print()

    print("Keystone and stat runes for each player:")
    for p in match.participants:
        print(
            f"{p.champion.name}: {p.runes.keystone.name}, ({', '.join([r.name for r in p.stat_runes])})"
        )


if __name__ == "__main__":
    print_newest_match(name="Kalturi", tagline="NA1", region="NA")
