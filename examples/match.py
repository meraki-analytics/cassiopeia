import cassiopeia as cass
from cassiopeia.core import Summoner


def print_newest_match(name: str, region: str):
    summoner = Summoner(name=name, region=region)

    # matches = cass.get_matches(summoner)
    matches = summoner.matches
    match = matches[0]
    print('Match ID:', match.id)
    for p in match.participants:
        print(p.name, 'playing', p.champion.name)


if __name__ == "__main__":
    print_newest_match(name="Kalturi", region="NA")
