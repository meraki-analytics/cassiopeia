import cassiopeia as cass
from cassiopeia import ShardStatus


def get_shard():
    status = cass.get_status(region="NA")
    status = ShardStatus(region="NA")
    print(status.name)


if __name__ == "__main__":
    get_shard()
