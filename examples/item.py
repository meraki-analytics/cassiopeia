import cassiopeia as cass
from cassiopeia.core import Summoner
from  cassiopeia import settings

def test_items():
    name = "Kalturi"

    items = cass.get_items()
    for item in items:
        print(item.name)


if __name__ == "__main__":
    test_items()
