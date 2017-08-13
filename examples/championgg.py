import cassiopeia as cass
from cassiopeia import Champion
from cassiopeia.dto.championgg import GGChampionListDto
from cassiopeia.configuration import settings
from cassiopeia.data import Platform


def get_champions():
    annie = Champion(name="Annie", id=1, region="NA")
    print(annie.name)

    print(annie.win_rate)
    print(annie.play_rate)


if __name__ == "__main__":
    get_champions()