import cassiopeia as cass
from cassiopeia.core import Summoner
from  cassiopeia import settings

def get_items():
    name = "Kalturi"

    items = cass.get_items()
    for item in items:
        print(item.name)


if __name__ == "__main__":
    get_items()
