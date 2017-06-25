import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"
    me = Summoner(name=name)

    match_id = 2530719537
    match = cass.get_match(match_id)
    print(match.id)
    print(match.creation)
    for p in match.participants:
        print(p.id, p.champion.name)
    return


if __name__ == "__main__":
    test_cass()
