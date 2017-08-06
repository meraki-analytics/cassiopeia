import cassiopeia as cass
from cassiopeia import Summoner


def print_summoner(name: str, region: str):
    summoner = Summoner(name=name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)
    print("Account ID:", summoner.account.id)
    print("Level:", summoner.level)
    print("Revision date:", summoner.revision_date)
    print("Profile icon ID:", summoner.profile_icon.id)
    print("Profile icon name:", summoner.profile_icon.name)
    print("Profile icon URL:", summoner.profile_icon.url)
    print("Profile icon image:", summoner.profile_icon.image)

    # These are equivalent ways of obtaining a Summoner.
    # Note that the region defaults to NA.
    summoner = cass.get_summoner(name=name)
    print(summoner.id)
    #   summoner = cass.get_summoner(name=summoner.name)
    #   summoner = cass.get_summoner(id=summoner.id)
    #   summoner = cass.get_summoner(account_id=summoner.account.id)


if __name__ == "__main__":
    print_summoner("Kalturi", "NA")
