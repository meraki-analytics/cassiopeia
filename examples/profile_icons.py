import cassiopeia as cass
from cassiopeia import ProfileIcons


def get_items():
    profile_icons = cass.get_profile_icons(region="NA")
    for pi in profile_icons:
        print(pi.name)


if __name__ == "__main__":
    get_items()
