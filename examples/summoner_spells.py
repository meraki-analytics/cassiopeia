import cassiopeia as cass
from cassiopeia import SummonerSpell
from cassiopeia.data import GameMode

def get_summoner_spells():
    sspells = cass.get_summoner_spells()
    for sspell in sspells:
        #if "Disabled" not in sspell.name:
        if set(sspell.modes) & {GameMode.classic, GameMode.aram, GameMode.poro_king, GameMode.ascension}:
            print("Name:", sspell.name)
            print("Description:", sspell.description)
            print()

    sspell = SummonerSpell(name="Ghost")
    print(sspell.description)

if __name__ == "__main__":
    get_summoner_spells()
