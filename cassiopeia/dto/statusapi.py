import cassiopeia.dto.requests
import cassiopeia.type.dto.status


def get_shards():
    """
    https://developer.riotgames.com/api/methods#!/908/3143

    Returns:
        list<Shard>: the shards (unfortunately neither Crystal nor Kirby's)
    """
    request = "http://status.leagueoflegends.com/shards"
    return [cassiopeia.type.dto.status.Shard(shard) for shard in cassiopeia.dto.requests.get(request, static=True, include_base=False)]


def get_shard():
    """
    https://developer.riotgames.com/api/methods#!/908/3142

    Returns:
        ShardStatus: the status of the current region's shard
    """
    request = "http://status.leagueoflegends.com/shards/{region}".format(region=cassiopeia.dto.requests.region)
    return cassiopeia.type.dto.status.ShardStatus(cassiopeia.dto.requests.get(request, static=True, include_base=False))
