import cassiopeia as cass
from cassiopeia.core import Summoner


def print_newest_match(name: str, account: int, id: int, region: str):

    # Notice how this function never makes a call to the summoner endpoint because we provide all the needed data!

    summoner = Summoner(name=name, account=account, id=id, region=region)

    # matches = cass.get_matches(summoner)
    match_history = summoner.match_history
    match = match_history[0]  # TODO This is triggering two match history loads for some reason...
    print('Match ID:', match.id)

    p = match.participants[name]
    print("\nSince the match was created from a matchref, we only know one participant:")
    #print(p.summoner.name, 'playing', p.champion.name)
    print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id)

    print("\nNow pull the full match data by iterating over all the participants:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon)

    print("\nIterate over all the participants again and note that the data is not repulled:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id, p.team.first_dragon)

    print("\nBlue team won?", match.blue_team.win)
    print("Red team won?", match.red_team.win)
    print("Participants on blue team:")
    for p in match.blue_team.participants:
        print(p.summoner.name)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", account=34718348, id=21359666, region="NA")
