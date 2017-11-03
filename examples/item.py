import cassiopeia as cass
from cassiopeia import Items, Item

def get_items():
    items = cass.get_items(region="NA")
    for item in items:
        print(item.name)
    items = cass.get_items(region="NA")
    print(items[10].name)
    dagger = Item(name="Dagger", region="NA")
    print(dagger.name, dagger.id)
    items = Items(region="NA")
    print(items[10].name)


if __name__ == "__main__":
    get_items()
