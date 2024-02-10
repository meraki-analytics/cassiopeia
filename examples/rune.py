import cassiopeia as cass
from cassiopeia import Runes, Rune


def print_keystone_runes():
    print("Keystone runes:")
    for rune in cass.get_runes(region="NA").keystones:
        print(rune.name)


def print_runes():
    print("All runes:")
    for rune in cass.get_runes(region="NA"):
        print(f"{rune.name} id: {rune.id} tier: {rune.tier}")


def print_precision_runes():
    print("Precision runes:")
    for rune in cass.get_runes(region="NA").precision:
        print(rune.name, rune.id, rune.path.name)


if __name__ == "__main__":
    print_keystone_runes()
    print_runes()
    print_precision_runes()
