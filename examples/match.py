import cassiopeia as cass
from cassiopeia.core import Summoner


def print_newest_match(name: str, account: int, id: int, region: str):
    summoner = Summoner(name=name, account=account, id=id, region=region)

    # matches = cass.get_matches(summoner)
    matches = summoner.matches
    match = matches[0]
    print('Match ID:', match.id)

    p = next(match.participants)
    print("\nSince the match was created from a matchref, we only know one participant:")
    #print(p.summoner.name, 'playing', p.champion.name)
    print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id)
    # TODO: The above print statement makes a call to the summoner endpoint for the provided summoner. However, it shouldn't because all the data for that summoner was provided. This won't be an issue when the cache is in place, but it means we are losing data during a transaction. Can/should that be fixed?

    print("\nNow pull the full match data by iterating over all the participants:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id)

    print("\nIterate over all the participants again and note that the data is not repulled:")
    for p in match.participants:
        #print(p.summoner.name, 'playing', p.champion.name)
        print(p.id, p.summoner.region, p.summoner.account.id, p.summoner.name, p.summoner.id, p.champion.id)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", account=34718348, id=21359666, region="NA")
