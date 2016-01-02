"""
Handles making HTTP requests to the REST API and converting the results into a usable format
"""

import requests
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
    "matchlist": "v2.2",
    "stats": "v1.3",
    "summoner": "v1.4",
    "team": "v2.4"
}

api_key = ""
tournament_api_key = ""
region = ""
print_calls = False
rate_limiter = None
tournament_rate_limiter = None
proxy = {}


def request(method, address, params=None, static=False, include_base=True, tournament=False, key_in_header=False, **kwargs):
    """Makes a rate-limited HTTP request to the Riot API and returns the result

    method          str               http method (get, post, put...)
    address         str               url or relative resource address
    params          dict<str, any>    the parameters to send with the request, in the url
    static          bool              whether this is a call to a static (non-rate-limited) API
    include_base    bool              whether to prepend https://{server}.api.pvp.net/api/lol/{region}/ to the request
    tournament      bool              is this request for the standard apis or the tournament one
    key_in_header   bool              if true, send the key as a header

    return          dict              the JSON response from the Riot API as a dict
    """
    if (not tournament and not api_key) or (tournament and not tournament_api_key):
        raise cassiopeia.type.api.exception.CassiopeiaException("API Key must be set before the API can be queried.")
    if not region:
        raise cassiopeia.type.api.exception.CassiopeiaException("Region must be set before the API can be queried.")

    # Set server and rgn
    server = "global" if static else region
    rgn = ("static-data/{region}" if static else "{region}").format(region=region)

    # Add the API key to headers or request params depending on the API
    headers = {}
    if params is None:
        params = {}
    if key_in_header:
        headers['X-Riot-Token'] = tournament_api_key if tournament else api_key
    else:
        params["api_key"] = tournament_api_key if tournament else api_key

    # Do we have json data in the request body? If yes encode it
    if method.upper() in ('POST', 'PUT') and 'data' in kwargs:
        headers['Content-Type'] = 'application/json'
        kwargs['data'] = json.dumps(kwargs['data'])

    # Build and send the request
    if include_base:
        url = "https://{server}.api.pvp.net/api/lol/{region}/{address}".format(
                server=server, region=rgn, address=address)
    else:
        url = address

    limiter = tournament_rate_limiter if tournament else rate_limiter
    response = limiter.call(execute_request, method, url, params=params, headers=headers, **kwargs) if limiter \
        else execute_request(method, url, params=params, headers=headers, **kwargs)

    if not response.ok:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if response.status_code == 429 and limiter:
            retry_after = 1
            if 'Retry-After' in response.headers and response.headers["Retry-After"]:
                retry_after += int(response.headers["Retry-After"])

            limiter.reset_in(retry_after)
            return request(method, address, params, static, include_base, tournament, key_in_header, **kwargs)
        else:
            raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(
                    code=response.status_code, url=url), response.status_code, response)
    return response.json() if len(response.text) is not 0 else None


def get(address, **kwargs):
    """ Performs a get request, see `request` for documentation """
    return request('get', address, **kwargs)


def post(address, **kwargs):
    """ Performs a post request, see `request` for documentation """
    return request('post', address, **kwargs)


def put(address, **kwargs):
    """ Performs a put request, see `request` for documentation """
    return request('put', address, **kwargs)


def execute_request(method, url, **kwargs):
    """ Performs a put request, see `request` for documentation """
    if print_calls:
        print(url)
    return requests.request(method, url, proxies=proxy, **kwargs)
