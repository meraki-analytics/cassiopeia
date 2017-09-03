import cassiopeia as cass
from cassiopeia import Summoner

def get_cass():
    me = Summoner(name="Kalturi", id=21359666, region="NA")
    print("Name:", me.name)
    print("Id:", me.id)

    #pages = cass.get_mastery_pages(me)
    pages = me.mastery_pages
    for page in pages:
        print(page.name)
    page = pages[0]
    for mastery, count in page.masteries.items():
        print(mastery.name, count)


if __name__ == "__main__":
    get_cass()
