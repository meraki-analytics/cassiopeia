import cassiopeia as cass
from cassiopeia import Locales


def get_locales():
    languages = cass.get_locales(region="NA")
    print(languages)
    print(languages[0])
    print(languages)


if __name__ == "__main__":
    get_locales()
