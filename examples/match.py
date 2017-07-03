import cassiopeia as cass
from cassiopeia.core import Summoner


def print_summoner(name: str, id: int):
    me = Summoner(name="Kalturi", id=21359666)

    #matches = cass.get_matches(me)
    matches = me.matches
    match = matches[0]
    print(match.id)
    for p in match.participants:
        print(p.id, p.champion.name)


if __name__ == "__main__":
    print_summoner(name="Kalturi", id=21359666)

