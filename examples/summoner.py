import cassiopeia as cass
from cassiopeia.core import Summoner

def test_cass():
    name = "Kalturi"

    me = Summoner(name=name)
    print("Name:", me.name)
    print("Id:", me.id)
    print("Account id:", me.account.id)
    print("Level:", me.level)
    print("Revision date:", me.revision_date)
    print("Profile icon id:", me.profile_icon.id)
    print("Profile icon name:", me.profile_icon.name)
    print("Profile icon url:", me.profile_icon.url)
    print("Profile icon image:", me.profile_icon.image)
    name = me.name
    id = me.id
    account_id = me.account.id
    me = cass.get_summoner(name)
    me = cass.get_summoner(name=name)
    me = cass.get_summoner(id=id)
    me = cass.get_summoner(account_id=account_id)
    return


if __name__ == "__main__":
    test_cass()
