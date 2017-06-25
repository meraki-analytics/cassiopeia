import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    items = cass.get_items()
    for item in items:
        try:
            item.tier
        except:
            try:
                print(item.name)
            except:
                pass
    return


if __name__ == "__main__":
    test_cass()
