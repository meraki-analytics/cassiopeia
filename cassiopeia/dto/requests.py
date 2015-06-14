import urllib.parse
import urllib.request
import urllib.error
import json

import cassiopeia.type.api.exception
import cassiopeia.type.api.rates

api_versions = {
    "champion": "v1.2",
    "league": "v2.5",
    "staticdata": "v1.2",
    "match": "v2.2",
    "matchhistory": "v2.2",
    "stats": "v1.3",
    "summoner": "v1.4"
}

api_key = ""
region = ""
do_print_calls = False
rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter([(10, 10), (500, 600)])

# @param request # str # The request string which follows /api/lol/{region}/
# @param params # dict<str, *> # The parameters to send with the request
# @param static # bool # Whether this is a call to a static (non-rate-limited) API
def get(request, params={}, static=False):
    if(not api_key):
        raise cassiopeia.type.api.exception.CassiopeiaException("API Key must be set before the API can be queried.")
    if(not region):
        raise cassiopeia.type.api.exception.CassiopeiaException("Region must be set before the API can be queried.")

    # Set server and rgn
    server = "global" if static else region.lower()
    rgn = ("static-data/{region}" if static else "{region}").format(region=region.lower())

    # Encode params
    params["api_key"] = api_key
    encoded_params = urllib.parse.urlencode(params)

    # Build and execute request
    url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=encoded_params)

    try:
        content = rate_limiter.call(executeRequest, url) if rate_limiter else executeRequest(url)
        return json.loads(content)
    except urllib.error.HTTPError as e:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if(e.code == 429 and rate_limiter):
            rate_limiter.reset_in(int(e.headers["Retry-After"]) + 1)
            return get(request, params, static)
        else:
            raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url))

# @param url # str # The full URL to send a GET request to
# @return # str # The content returned by the server
def executeRequest(url):
    if(do_print_calls):
        print(url)

    response = None
    try:
        response = urllib.request.urlopen(url)
        content = response.read().decode(encoding="UTF-8")
        return content
    finally:
        if(response): 
            response.close()

# @param key # str # The API key to use
def set_api_key(key):
    api_key = key

# @param region # str # The region to access with the API
def set_region(region):
    region = region

# @param on # bool # Whether to print calls as they are made to the API
def print_calls(on):
    do_print_calls = on

# @param calls_per_epoch # int # Number of calls allowed in each epoch
# @param seconds_per_epoch # int # Number of seconds per epoch
def set_rate_limit(calls_per_epoch, seconds_per_epoch):
    rate_limiter = cassiopeia.type.api.rates.SingleRateLimiter(calls_per_epoch, seconds_per_epoch)

# @param limits # list<tuple> # A list of rate limit pairs. A rate limit is (calls_per_epoch, seconds_per_epoch)
def set_rate_limits(limits):
    rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter(limits)

# @param url # str # The URL to use as a proxy (without port number or protocol)
# @param port # int # The port to connect to
def set_proxy(url, port=80):
    if(url):
        proxy = urllib.request.ProxyHandler({"https": "https://{url}:{port}".format(url=url, port=port)})
        urllib.request.install_opener(urllib.request.build_opener(proxy))
    else:
        proxy = urllib.request.ProxyHandler({})
        urllib.request.install_opener(urllib.request.build_opener(proxy))