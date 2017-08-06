import cassiopeia as cass

def get_items():
    items = cass.get_items()
    for item in items:
        print(item.name)
    items = cass.get_items()
    print(items[10].name)


if __name__ == "__main__":
    get_items()
