import cassiopeia as cass
from cassiopeia.core import Locales


def get_languages():
    languages = cass.get_languages(region="NA")
    print(languages)
    print(languages[0])
    print(languages)


if __name__ == "__main__":
    get_languages()
