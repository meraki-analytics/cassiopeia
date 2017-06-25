import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    me = Summoner(name=name, id=21359666)
    print("Name:", me.name)
    print("Id:", me.id)

    #pages = cass.get_rune_pages(me)
    pages = me.rune_pages
    for page in pages:
        print(page.name)
    page = pages[0]
    for rune, count in page.runes.items():
        print(rune.name, count)
    return


if __name__ == "__main__":
    test_cass()
