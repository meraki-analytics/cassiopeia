from cassiopeia import requests
from cassiopeia.type.api.rates import SingleRateLimiter, MultiRateLimiter
from cassiopeia.dto.championapi import *
from cassiopeia.dto.leagueapi import *
from cassiopeia.dto.staticdataapi import *
from cassiopeia.dto.matchapi import *
from cassiopeia.dto.matchhistoryapi import *
from cassiopeia.dto.statsapi import *
from cassiopeia.dto.summonerapi import *

# @param key # str # The API key to use
def set_api_key(key):
    requests.api_key = key

# @param region # str # The region to access with the API
def set_region(region):
    requests.region = region

# @param mirror # str # The mirror to use to acces the API
def set_mirror(mirror):
    requests.mirror = mirror

# @param on # bool # Whether to print calls as they are made to the API
def print_calls(on):
    requests.print_calls = on

# @param calls_per_epoch # int # Number of calls allowed in each epoch
# @param seconds_per_epoch # int # Number of seconds per epoch
def set_rate_limit(calls_per_epoch, seconds_per_epoch):
    requests.rate_limiter = SingleRateLimiter(calls_per_epoch, seconds_per_epoch)

# @param limits # list<tuple> # A list of rate limit pairs. A rate limit is (calls_per_epoch, seconds_per_epoch)
def set_rate_limit(limits):
    requests.rate_limiter = MultiRateLimiter(limits)