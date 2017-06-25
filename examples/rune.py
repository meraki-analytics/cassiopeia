import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    runes = cass.get_runes()
    for rune in runes:
        if rune.tier == 3:
            print(rune.name)
    return


if __name__ == "__main__":
    test_cass()
