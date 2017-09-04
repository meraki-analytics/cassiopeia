import cassiopeia as cass
from cassiopeia import Map, Maps


def get_maps():
    maps = cass.get_maps(region="NA")
    for map in maps:
        print(map.name, map.id)

    map = Map(name="Summoner's Rift", region="NA")
    print(map.id)


if __name__ == "__main__":
    get_maps()
