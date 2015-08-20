"""
Handles making HTTP requests to the REST API and converting the results into a usable format
"""

import urllib.parse
import urllib.request
import urllib.error
import json

import cassiopeia.type.api.exception
import cassiopeia.type.api.rates

api_versions = {
    "champion": "v1.2",
    "currentgame": "v1.0",
    "featuredgames": "v1.0",
    "game": "v1.3",
    "league": "v2.5",
    "staticdata": "v1.2",
    "status": "v1.0",
    "match": "v2.2",
    "matchhistory": "v2.2",
    "matchlist": "v2.2",
    "stats": "v1.3",
    "summoner": "v1.4",
    "team": "v2.4"
}

api_key = ""
region = ""
print_calls = False
rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter((10, 10), (500, 600))

def get(request, params={}, static=False, include_base=True):
    """Makes a rate-limited HTTP request to the Riot API and returns the result

    request         str               the request string
    params          dict<str, any>    the parameters to send with the request (default {})
    static          bool              whether this is a call to a static (non-rate-limited) API
    include_base    bool              whether to prepend https://{server}.api.pvp.net/api/lol/{region}/ to the request

    return          dict              the JSON response from the Riot API as a dict
    """
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
    if(include_base):
        url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=encoded_params)
    else:
        url = "{request}?{params}".format(request=request, params=encoded_params)

    try:
        content = rate_limiter.call(executeRequest, url) if rate_limiter else executeRequest(url)
        return json.loads(content)
    except urllib.error.HTTPError as e:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if(e.code == 429 and rate_limiter):
            retry_after = 1
            if(e.headers["Retry-After"]):
                retry_after += int(e.headers["Retry-After"])
                
            rate_limiter.reset_in(retry_after)
            return get(request, params, static)
        else:
            raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url), e.code)

def executeRequest(url):
    """Executes an HTTP GET request and returns the result in a string

    url       str    the full URL to send a GET request to

    return    str    the content returned by the server
    """
    if(print_calls):
        print(url)

    response = None
    try:
        response = urllib.request.urlopen(url)
        content = response.read().decode(encoding="UTF-8")
        return content
    finally:
        if(response): 
            response.close()