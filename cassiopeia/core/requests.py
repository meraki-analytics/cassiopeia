import cassiopeia.type.core.common
import cassiopeia.type.api.store

load_policy = cassiopeia.type.core.common.LoadPolicy.eager
data_store = cassiopeia.type.api.store.Cache()

# @param method # function # The method to call
# @param max_size # int # The maximum size a list can be as the argument
# @param arg # * or list<*> # The argument or list of arguments
# @return # list<*> or dict<*> # The result of calling the method on the arg after splitting into max sized chunks
def call_with_ensured_size(method, max_size, arg):
    if(not isinstance(arg, list) or len(arg) <= max_size):
        return method(arg)

    results = method(arg[0:max_size])
    i = max_size

    if(isinstance(results, list)):
        while(i < len(arg)):
            sublist = arg[i:i+max_size]
            results = results + method(sublist)
            i += max_size
    elif(isinstance(results, dict)):
        while(i < len(arg)):
            sublist = arg[i:i+max_size]
            results.update(method(sublist))
            i += max_size
    return results