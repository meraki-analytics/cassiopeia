import cassiopeia.dto.requests
import cassiopeia.core.requests
from cassiopeia.core.leagueapi import *
from cassiopeia.core.matchapi import *
from cassiopeia.core.matchhistoryapi import *
from cassiopeia.core.staticdataapi import *
from cassiopeia.core.statsapi import *
from cassiopeia.core.summonerapi import *

# @param key # str # The API key to use
def set_api_key(key):
    cassiopeia.dto.requests.api_key = key

# @param region # Region # The region to query against
def set_region(region):
    cassiopeia.dto.requests.region = region.value

# @param on # bool # Whether to print calls as they are made to the API
def print_calls(on):
    cassiopeia.dto.requests.print_calls = on

# @param calls_per_epoch # int # Number of calls allowed in each epoch
# @param seconds_per_epoch # int # Number of seconds per epoch
def set_rate_limit(calls_per_epoch, seconds_per_epoch):
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.SingleRateLimiter(calls_per_epoch, seconds_per_epoch)

# @param limits # list<tuple> # A list of rate limit pairs. A rate limit is (calls_per_epoch, seconds_per_epoch)
def set_rate_limits(limits):
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter(limits)

# @param url # str # The URL to use as a proxy (without port number or protocol)
# @param port # int # The port to connect to
def set_proxy(url, port=80):
    if(url):
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({"https": "https://{url}:{port}".format(url=url, port=port)})
        urllib.request.install_opener(urllib.request.build_opener(proxy))
    else:
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({})
        urllib.request.install_opener(urllib.request.build_opener(proxy))

# @param locale # str # The locale to use for returned text. Use get_languages() to find valid locales.
def set_locale(locale):
    cassiopeia.dto.staticdataapi._locale = locale

# @param policy # LoadPolicy # The load policy to use
def set_load_policy(policy):
    cassiopeia.core.requests.load_policy = policy

# @param store # DataStore # The data store to use
def set_data_store(store):
    cassiopeia.core.requests.data_store = store