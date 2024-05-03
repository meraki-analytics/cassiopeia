import cassiopeia as cass
from cassiopeia import Account


def print_summoner(name: str, tagline: str, region: str):
    account = Account(
        # puuid="ba4FMWMmGaz-FFY2WWj6YZ5MsG12CoRGeeWz9PVmGuQMZ1LRklyg3x5UTkgaPivKcvMA3A6VEhhiVw",
        name=name,
        tagline=tagline,
        region=region,
    )
    summoner = account.summoner
    print("Name:", account.name_with_tagline)
    print("ID:", summoner.id)
    print("Account ID:", summoner.account_id)
    print("Level:", summoner.level)
    print("Revision date:", summoner.revision_date)
    print("Profile icon ID:", summoner.profile_icon.id)
    print("Profile icon name:", summoner.profile_icon.name)
    print("Profile icon URL:", summoner.profile_icon.url)
    print("Profile icon image:", summoner.profile_icon.image)


if __name__ == "__main__":
    print_summoner("BadM0j08", "Style", "NA")
