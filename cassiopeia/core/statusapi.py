import cassiopeia.dto.statusapi
import cassiopeia.type.core.status

# @return # list<cassiopeia.type.core.status.Shard> # The shards
def get_shards():
    return [cassiopeia.type.core.status.Shard(shard) for shard in cassiopeia.dto.statusapi.get_shards()]

# @return # cassiopeia.type.core.status.ShardStatus # The shard for the current region
def get_shard():
    return cassiopeia.type.core.status.ShardStatus(cassiopeia.dto.statusapi.get_shard())