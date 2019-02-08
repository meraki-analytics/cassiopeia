import cassiopeia as cass
from cassiopeia import Runes, Rune


def print_keystone_runes():
    for rune in cass.get_runes(region="NA").keystones:
        print(rune.name)


if __name__ == "__main__":
    print_keystone_runes()
