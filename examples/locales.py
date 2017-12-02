import cassiopeia as cass
from cassiopeia import Locales


def get_locales():
    locales = cass.get_locales(region="NA")
    print(locales)
    for locale in locales:
        print(locale)
    print(locales)


if __name__ == "__main__":
    get_locales()
