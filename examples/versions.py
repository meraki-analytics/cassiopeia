import cassiopeia as cass


def get_versions():
    versions = cass.get_versions(region="NA")
    print(versions)


if __name__ == "__main__":
    get_versions()
