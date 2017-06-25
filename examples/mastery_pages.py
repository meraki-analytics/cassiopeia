import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    me = Summoner(name=name, id=21359666)
    print("Name:", me.name)
    print("Id:", me.id)

    #pages = cass.get_mastery_pages(me)
    pages = me.mastery_pages
    for page in pages:
        print(page.name)
    page = pages[0]
    for mastery, count in page.masteries.items():
        print(mastery.name, count)
    return


if __name__ == "__main__":
    test_cass()
