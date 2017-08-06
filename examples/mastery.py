import cassiopeia as cass
from cassiopeia import Masteries, Mastery


def print_masteries():
    for mastery in cass.get_masteries():
        print(mastery.name)


if __name__ == "__main__":
    print_masteries()
