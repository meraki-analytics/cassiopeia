import cassiopeia as cass
from cassiopeia import Summoner


def print_summoner(name: str, region: str):
    summoner = Summoner(name=name, region=region)
    print("Name:", summoner.name)
    print("ID:", summoner.id)
    print("Account ID:", summoner.account_id)
    print("Level:", summoner.level)
    print("Revision date:", summoner.revision_date)
    print("Profile icon ID:", summoner.profile_icon.id)
    print("Profile icon name:", summoner.profile_icon.name)
    print("Profile icon URL:", summoner.profile_icon.url)
    print("Profile icon image:", summoner.profile_icon.image)


if __name__ == "__main__":
    print_summoner("Kalturi", "NA")
