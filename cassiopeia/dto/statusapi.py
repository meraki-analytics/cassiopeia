import cassiopeia.dto.requests
import cassiopeia.type.dto.status

# @return # list<cassiopeia.type.dto.status.Shard> # The shards. Unfortunately neither Crystal nor Kirby's.
def get_shards():
    request = "http://status.leagueoflegends.com/shards"
    return [cassiopeia.type.dto.status.Shard(shard) for shard in cassiopeia.dto.requests.get(request, static=True, include_base=False)]

# @return # cassiopeia.type.dto.status.ShardStatus # The shard for the current region
def get_shard():
    request = "http://status.leagueoflegends.com/shards/{region}".format(region=cassiopeia.dto.requests.region.lower())
    return cassiopeia.type.dto.status.ShardStatus(cassiopeia.dto.requests.get(request, static=True, include_base=False))