import cassiopeia as cass
from cassiopeia.core import LanguagesData


def get_languages():
    languages = cass.get_languages(region="NA")
    print(languages)


if __name__ == "__main__":
    get_languages()
