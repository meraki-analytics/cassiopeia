import cassiopeia as cass
from cassiopeia.core import LanguagesData


def get_shard():
    languages = cass.get_languages(region="NA")
    languages = LanguagesData(region="NA")
    print(languages)


if __name__ == "__main__":
    get_shard()
