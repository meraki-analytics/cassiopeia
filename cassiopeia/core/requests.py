import cassiopeia.type.core.common
import cassiopeia.type.api.store

load_policy = cassiopeia.type.core.common.LoadPolicy.lazy
data_store = cassiopeia.type.api.store.Cache()

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