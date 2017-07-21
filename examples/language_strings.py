import cassiopeia as cass
from cassiopeia.core import LanguageStrings


def get_language_strings():
    language_strings = cass.get_language_strings(region="NA")
    print(language_strings.strings)


if __name__ == "__main__":
    get_language_strings()
