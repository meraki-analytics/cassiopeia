import cassiopeia.type.core.common
import cassiopeia.type.api.store

load_policy = cassiopeia.type.core.common.LoadPolicy.eager
data_store = cassiopeia.type.api.store.Cache()


def call_with_ensured_size(method, max_size, arg):
    """
    Breaks a list of arguments up into chunks of a maximum size and calls the given method on each chunk

    Args:
        method (function): the method to call
        max_size (int): the maximum number of arguments to include in a single call
        arg (any | list<any>): the arguments to split up

    Returns:
        list<any> | dict<any>: the combined results of the function calls on each chunk
    """
    if not isinstance(arg, list) or len(arg) <= max_size:
        return method(arg)

    results = method(arg[0:max_size])
    i = max_size

    if isinstance(results, list):
        while(i < len(arg)):
            sublist = arg[i:i + max_size]
            results = results + method(sublist)
            i += max_size
    elif isinstance(results, dict):
        while(i < len(arg)):
            sublist = arg[i:i + max_size]
            results.update(method(sublist))
            i += max_size
    return results
