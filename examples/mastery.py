import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    masteries = cass.get_masteries()
    for mastery in masteries:
        print(mastery.name)


if __name__ == "__main__":
    test_cass()
