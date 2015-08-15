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
    "match": "v2.2",
    "matchhistory": "v2.2",
    "matchlist": "v2.2",
    "stats": "v1.3",
    "summoner": "v1.4"
}

api_key = ""
region = ""
print_calls = False
rate_limiter = cassiopeia.type.api.rates.MultiRateLimiter([(10, 10), (500, 600)])

# @param request # str # The request string which follows /api/lol/{region}/
# @param params # dict<str, *> # The parameters to send with the request
# @param static # bool # Whether this is a call to a static (non-rate-limited) API
# @param include_base # bool # If false, don't include /api/lol/{region}/
# @return # dict # The JSON response in a dict
def get(request, params={}, static=False, include_base=True):
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
        url = "https://{server}.api.pvp.net/{request}?{params}".format(server=server, region=rgn, request=request, params=encoded_params)

    try:
        content = rate_limiter.call(executeRequest, url) if rate_limiter else executeRequest(url)
        return json.loads(content)
    except urllib.error.HTTPError as e:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if(e.code == 429 and rate_limiter):
            try:
                rate_limiter.reset_in(int(e.headers["Retry-After"]) + 1)
            except(TypeError):
                # Retry-Ater wasn't sent
                raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url), e.code)
            return get(request, params, static)
        else:
            raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url), e.code)

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