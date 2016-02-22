import cassiopeia.dto.statusapi
import cassiopeia.type.core.status


def get_shards():
    """
    Get the list of server shards

    Returns:
        list<Shard>: the shards
    """
    return [cassiopeia.type.core.status.Shard(shard) for shard in cassiopeia.dto.statusapi.get_shards()]


def get_shard():
    """
    Gets the status of the current region's shard

    Returns:
        ShardStatus: the status of the current region's shard
    """
    return cassiopeia.type.core.status.ShardStatus(cassiopeia.dto.statusapi.get_shard())
