import cassiopeia as cass
from cassiopeia import SummonerSpell
from cassiopeia.data import GameMode

def test_cass():
    sspells = cass.get_summoner_spells()
    for sspell in sspells:
        #if "Disabled" not in sspell.name:
        if set(sspell.modes) & {GameMode.classic, GameMode.aram, GameMode.poro_king, GameMode.ascension}:
            print(sspell.name)
            try:
                print(sspell.tooltip)
            except:
                print("FAILURE")
                print(sspell._data.values()[0])
            print()

    sspell = SummonerSpell(name="Ghost")
    print(sspell.tooltip)

if __name__ == "__main__":
    test_cass()
