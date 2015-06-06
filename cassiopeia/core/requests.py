from cassiopeia.dto.requests import set_api_key, print_calls, set_rate_limit, set_rate_limits, set_proxy
import cassiopeia.dto.requests
import cassiopeia.type.core.common
import cassiopeia.type.api.store

load_policy = cassiopeia.type.core.common.LoadPolicy.lazy
data_store = cassiopeia.type.api.store.Cache()

# @param policy # LoadPolicy # The load policy to use
def set_load_policy(policy):
    load_policy = policy

# @param store # DataStore # The data store to use
def set_data_store(store):
    data_store = store

# @param region # Region # The region to query against
def set_region(region):
    cassiopeia.dto.requests.set_region(region.value)

# @param method # function # The method to call
# @param max_size # int # The maximum size a list can be as the argument
# @param arg # * or list<*> # The argument or list of arguments
# @return # list<*> # The result of calling the method on the arg after splitting into max sized chunks
def call_with_ensured_size(method, max_size, arg):
    if(not isinstance(arg, list) or len(arg) <= max_size):
        return method(arg)

    results = []
    i = 0
    while(i < len(arg)):
        sublist = arg[i:i+max_size]
        results.append(method(sublist))
        i += max_size
    return results