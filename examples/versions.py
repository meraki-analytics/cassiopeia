import cassiopeia as cass


def get_versions():
    versions = cass.get_versions(region="NA")
    print(versions[0])
    print(versions.region)

    versions = cass.get_versions(region="NA")
    print(versions[0])

    realms = cass.get_realms(region="NA")
    print(realms.latest_versions)

if __name__ == "__main__":
    get_versions()
