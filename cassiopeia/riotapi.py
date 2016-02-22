"""
This is the primary entry point for Cassiopeia. Accesses the LoL REST API (https://developer.riotgames.com/)and provides the results in easy-to-use Python objects.
"""

import urllib.request

import cassiopeia.dto.requests
import cassiopeia.type.api.rates
import cassiopeia.dto.staticdataapi
import cassiopeia.core.requests
import cassiopeia.type.core.common
import cassiopeia.type.api.store
from cassiopeia.core.championapi import *
from cassiopeia.core.championmasteryapi import *
from cassiopeia.core.currentgameapi import *
from cassiopeia.core.featuredgamesapi import *
from cassiopeia.core.gameapi import *
from cassiopeia.core.leagueapi import *
from cassiopeia.core.matchapi import *
from cassiopeia.core.matchlistapi import *
from cassiopeia.core.staticdataapi import *
from cassiopeia.core.statusapi import *
from cassiopeia.core.statsapi import *
from cassiopeia.core.summonerapi import *
from cassiopeia.core.teamapi import *
from cassiopeia.core.tournamentapi import *


def set_api_key(key):
    """
    Set your API key

    Args:
        key (str): the key to use
    """
    cassiopeia.dto.requests.api_key = key
    if not cassiopeia.dto.requests.rate_limiter:
        cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter((10, 10), (500, 600))


def set_tournament_api_key(key):
    """
    Set your tournament API key

    Args:
        key (str): the key to use
    """
    cassiopeia.dto.requests.tournament_api_key = key
    if not cassiopeia.dto.requests.tournament_rate_limiter:
        cassiopeia.dto.requests.tournament_rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter((10, 10), (500, 600))


def set_region(region):
    """
    Set the region to run API queries against

    Args:
        region (str | cassiopeia.type.core.common.Region): the region to query against
    """
    if not isinstance(region, cassiopeia.type.core.common.Region):
        region = cassiopeia.type.core.common.Region(region.lower())
    cassiopeia.dto.requests.region = region.value


def print_calls(on):
    """
    Sets whether to print calls to stdout as they are made

    Args:
        on (bool): the region to query against
    """
    cassiopeia.dto.requests.print_calls = on


def get_requests_count(tournament=False):
    """
    Returns the number of successful requests (no exceptions in the call) and total requests issued up to now

    Args:
        tournament (bool): get the request counts for the tournament requests

    Returns:
        tuple: A (successful calls, total calls) tuple
    """
    limiter = cassiopeia.dto.requests.tournament_rate_limiter if tournament else cassiopeia.dto.requests.rate_limiter
    return limiter.calls


def set_rate_limit(calls_per_epoch, seconds_per_epoch):
    """
    Sets the rate limit for cassiopeia to manage internally

    Args:
        calls_per_epoch (int): the number of calls allowed in each epoch
        seconds_per_epoch (int): the number of seconds per epoch
    """
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.SingleRateLimiter(calls_per_epoch, seconds_per_epoch)


def set_tournament_rate_limit(calls_per_epoch, seconds_per_epoch):
    """
    Sets the tournament rate limit for cassiopeia to manage internally

    Args:
        calls_per_epoch (int): the number of calls allowed in each epoch
        seconds_per_epoch (int): the number of seconds per epoch
    """
    cassiopeia.dto.requests.tournament_rate_limiter = cassiopeia.type.api.rates.SingleRateLimiter(calls_per_epoch, seconds_per_epoch)


def set_rate_limits(*limits):
    """
    Sets the rate limits for cassiopeia to manage internally

    Args:
        *limits (tuple...): the rate limits to apply. Rate limits are of the form (calls_per_epoch, seconds_per_epoch)
    """
    cassiopeia.dto.requests.rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter(*limits)


def set_tournament_rate_limits(*limits):
    """
    Sets the tournament rate limits for cassiopeia to manage internally

    Args:
        *limits (tuple...): the rate limits to apply. Rate limits are of the form (calls_per_epoch, seconds_per_epoch)
    """
    cassiopeia.dto.requests.tournament_rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter(*limits)


def set_proxy(url, port=80):
    """
    Sets a proxy server to tunnel requests to the Riot API through

    Args:
        url (str): the URL of the proxy server, without port number or protocol
        port (int): the port number to conntect to (default 80)
    """
    if url:
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({"https": "https://{url}:{port}".format(url=url, port=port)})
        urllib.request.install_opener(urllib.request.build_opener(cassiopeia.dto.requests.proxy))
    else:
        cassiopeia.dto.requests.proxy = urllib.request.ProxyHandler({})
        urllib.request.install_opener(urllib.request.build_opener(cassiopeia.dto.requests.proxy))


def set_locale(locale):
    """
    Sets the locale (language) to use for calls to the Riot API. Use get_languages() to find valid locales.

    Args:
        locale (str): the locale to use for calls to the API
    """
    cassiopeia.dto.staticdataapi._locale = locale


def set_load_policy(policy):
    """
    Sets the load policy to use. Keep your load policy in mind when making calls, as different policies are better for different applications.

    Args:
        policy (str | cassiopeia.type.core.common.LoadPolicy): the load policy to use for calls to the API
    """
    if not isinstance(policy, cassiopeia.type.core.common.LoadPolicy):
        policy = cassiopeia.type.core.common.LoadPolicy(policy.upper())
    cassiopeia.core.requests.load_policy = policy


def set_data_store(store):
    """
    Sets the data store to use for caching the results of API calls.

    Args:
        store (cassiopeia.type.api.store.DataStore): the data store to use for storing results
    """
    if not store:
        cassiopeia.core.requests.data_store = cassiopeia.type.api.store.VoidDataStore()
    else:
        cassiopeia.core.requests.data_store = store
