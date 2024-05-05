import cassiopeia as cass
from cassiopeia import Items, Item


def get_items():
    # Print all items
    items = cass.get_items(region="NA")  # Alternatively:  items = Items(region="NA")
    for item in items:
        print(item.name, item.id)
    print()

    # Specify a specific item by name
    dagger = Item(name="Dagger", region="NA")
    print(dagger.name, dagger.id)


if __name__ == "__main__":
    get_items()
