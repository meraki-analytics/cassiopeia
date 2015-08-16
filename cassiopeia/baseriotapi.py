"""
Accesses the LoL REST API (https://developer.riotgames.com/), returning Python objects matching the exact API spec.
"""

import cassiopeia.dto.requests
import cassiopeia.type.api.rates
import cassiopeia.dto.staticdataapi
from cassiopeia.dto.championapi import *
from cassiopeia.dto.currentgameapi import *
from cassiopeia.dto.featuredgamesapi import *
from cassiopeia.dto.gameapi import *
from cassiopeia.dto.leagueapi import *
from cassiopeia.dto.staticdataapi import *
from cassiopeia.dto.statusapi import *
from cassiopeia.dto.matchapi import *
from cassiopeia.dto.matchlistapi import *
from cassiopeia.dto.matchhistoryapi import *
from cassiopeia.dto.statsapi import *
from cassiopeia.dto.summonerapi import *
from cassiopeia.dto.teamapi import *

def set_api_key(key):
    """Set your API key

    key    str    the key to use
    """
    cassiopeia.dto.requests.api_key = key

def set_region(region):
    """Set the region to run API queries against

    region    str    the region to query against
    """
    cassiopeia.dto.requests.region = region

def print_calls(on):
    """Sets whether to print calls to stdout as they are made

    on    bool    the region to query against
    """
    cassiopeia.dto.requests.print_calls = on

def set_rate_limit(calls_per_epoch, seconds_per_epoch):
    """Sets the rate limit for cassiopeia to manage internally

    calls_per_epoch      int    the number of calls allowed in each epoch
    seconds_per_epoch    int    the number of seconds per epoch
    """
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.SingleRateLimiter(calls_per_epoch, seconds_per_epoch)

def set_rate_limits(*limits):
    """Sets the rate limits for cassiopeia to manage internally

    *limits    tuple...    the rate limits to apply. Rate limits are of the form (calls_per_epoch, seconds_per_epoch)
    """
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter(*limits)

def set_proxy(url, port=80):
    """Sets a proxy server to tunnel requests to the Riot API through

    url     str    the URL of the proxy server, without port number or protocol
    port    int    the port number to conntect to (default 80)
    """
    if(url):
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({"https": "https://{url}:{port}".format(url=url, port=port)})
        urllib.request.install_opener(urllib.request.build_opener(proxy))
    else:
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({})
        urllib.request.install_opener(urllib.request.build_opener(proxy))

def set_locale(locale):
    """Sets the locale (language) to use for calls to the Riot API. Use get_languages() to find valid locales.

    locale    str    the locale to use for calls to the API
    """
    cassiopeia.dto.staticdataapi._locale = locale