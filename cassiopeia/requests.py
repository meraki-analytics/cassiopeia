import urllib.parse
import urllib.request
from urllib.error import HTTPError
import json

from cassiopeia.type.api.exception import CassiopeiaError, APIError
from cassiopeia.type.api.rates import MultiRateLimiter

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
mirror = ""
print_calls = False
rate_limiter = MultiRateLimiter([(10, 10), (500, 600)])

# @param request # str # The request string which follows /api/lol/{region}/
# @param params # dict<str, *> # The parameters to send with the request
# @param static # bool # Whether this is a call to a static (non-rate-limited) API
def get(request, params={}, static=False):
    if(not api_key):
        raise CassiopeiaError("API Key must be set before the API can be queried.")
    if(not region):
        raise CassiopeiaError("Region must be set before the API can be queried.")
    if(not mirror):
        raise CassiopeiaError("Mirror must be set before the API can be queried.")

    # Set server and rgn
    server = "global" if static else mirror.lower()
    rgn = ("static-data/{region}" if static else "{region}").format(region=region.lower())

    # Encode params
    params["api_key"] = api_key
    encoded_params = urllib.parse.urlencode(params)

    # Build and execute request
    url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=encoded_params)

    try:
        content = rate_limiter.call(executeRequest, url) if rate_limiter else executeRequest(url)
        return json.loads(content)
    except HTTPError as e:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if(e.code == 429 and rate_limiter):
            rate_limiter.reset_in(int(e.headers["Retry-After"]) + 1)
            return get(request, params, static)
        else:
            raise APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url))

# @param url # str # The full URL to send a GET request to
# @return # str # The content returned by the server
def executeRequest(url):
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