import cassiopeia as cass
from cassiopeia import Champion, Champions


def get_champions():
    champions = Champions(region="NA")
    for champion in champions:
        print(champion.name, champion.id)

    # annie = Champion(name="Annie", region="NA")
    annie = Champion(name="Annie", region="NA")
    print(annie.name)
    print(annie.title)
    for spell in annie.spells:
        print(spell.name, spell.keywords)

    print(annie.info.difficulty)
    print(annie.passive.name)
    print({item.name: count for item, count in annie.recommended_itemsets[0].item_sets[0].items.items()})
    print(annie.free_to_play)
    
    print(annie.win_rates)


if __name__ == "__main__":
    get_champions()
