import cassiopeia as cass
from cassiopeia import Map

def test_cass():
    maps = cass.get_maps()
    for map in maps:
        print(map.name, map.id)

    map = Map(name="Summoner's Rift")
    print(map.id)

if __name__ == "__main__":
    test_cass()
