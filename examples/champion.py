import cassiopeia as cass
from cassiopeia.core import Champion

def test_cass():
    #annie = Champion(name="Annie", region="NA")
    annie = Champion(name="Annie")
    print(annie.name)
    print(annie.title)
    print(annie.title)
    for spell in annie.spells:
        print(spell.name, spell.keywords)

    print(annie.info.difficulty)
    print(annie.passive.name)
    #print(annie.recommended_itemsets[0].item_sets[0].items)
    print(annie.free_to_play)
    print(annie._Ghost__all_loaded)
    print(annie)

    print()

    #ziggs = cass.get_champion(region="NA", "Ziggs")
    ziggs = cass.get_champion("Ziggs")
    print(ziggs.name)
    print(ziggs.region)
    #print(ziggs.recommended_itemset[0].item_sets[0].items)
    print(ziggs.free_to_play)
    for spell in ziggs.spells:
        for var in spell.variables:
            print(spell.name, var)
    print(ziggs._Ghost__all_loaded)


if __name__ == "__main__":
    test_cass()
