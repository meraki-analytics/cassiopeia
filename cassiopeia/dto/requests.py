"""
Handles making HTTP requests to the REST API and converting the results into a usable format
"""

import urllib.parse
import urllib.request
import urllib.error
import json
import zlib
import time

import cassiopeia.type.api.exception
import cassiopeia.type.api.rates


api_versions = {
    "champion": "v1.2",
    "championmastery": None,
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
    "team": "v2.4",
    "tournament": "v1"
}

api_key = ""
tournament_api_key = ""
region = ""
print_calls = False
rate_limiter = None
tournament_rate_limiter = None


def get(request, params={}, static=False, include_base=True, tournament=False):
    return make_request(request=request, method="GET", params=params, static=static, include_base=include_base, tournament=tournament)


def put(request, payload, params={}, include_base=True, tournament=False):
    return make_request(request=request, method="PUT", payload=payload, params=params, include_base=include_base, tournament=tournament)


def post(request, payload, params={}, include_base=True, tournament=False):
    return make_request(request=request, method="POST", payload=payload, params=params, include_base=include_base, tournament=tournament)


def make_request(request, method, params={}, payload=None, static=False, include_base=True, tournament=False):
    """
    Makes a rate-limited HTTP request to the Riot API and returns the result

    Args:
        request (str): the request string
        method (str): the HTTP method to use
        params (dict<str, any>): the path parameters to send with the request (default {})
        payload (CassiopeiaDto | CassiopeiaObject): the payload to send with the POST or PUT request (default None)
        static (bool): whether this is a call to a static (non-rate-limited) API (default False)
        include_base (bool): whether to prepend https://{server}.api.pvp.net/api/lol/{region}/ to the request (default True)
        tournament (bool): whether to use the tournament API rate limit (default False)

    Returns:
        dict: the JSON response from the Riot API as a dict
    """
    if (not tournament and not api_key) or (tournament and not tournament_api_key):
        raise cassiopeia.type.api.exception.CassiopeiaException("API Key must be set before the API can be queried.")
    if not region:
        raise cassiopeia.type.api.exception.CassiopeiaException("Region must be set before the API can be queried.")

    # Set server and rgn
    server = "global" if static else region
    rgn = ("static-data/{region}" if static else "{region}").format(region=region)

    # Encode params
    params["api_key"] = tournament_api_key if tournament else api_key
    encoded_params = urllib.parse.urlencode(params)

    payload = payload.to_json(separators=(",", ":"), indent=None) if payload else ""

    # Build and execute request
    if include_base:
        url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=encoded_params)
    else:
        url = "{request}?{params}".format(request=request, params=encoded_params)

    limiter = tournament_rate_limiter if tournament else rate_limiter
    try:
        content = limiter.call(execute_request, url, method, payload) if limiter else execute_request(url, method, payload)
        return json.loads(content) if content else {}
    except urllib.error.HTTPError as e:
        # Reset rate limiter and retry on 429 (rate limit exceeded)
        if e.code == 429 and limiter:
            if "X-Rate-Limit-Type" not in e.headers or e.headers["X-Rate-Limit-Type"] == "service":
                time.sleep(1)  # Backoff for 1 second before retrying
            else:
                retry_after = 1
                if e.headers["Retry-After"]:
                    retry_after += int(e.headers["Retry-After"])

                limiter.reset_in(retry_after)
            return make_request(request, method, params, payload, static, include_base, tournament)
        else:
            raise cassiopeia.type.api.exception.APIError("Server returned error {code} on call: {url}".format(code=e.code, url=url), e.code)


def execute_request(url, method, payload=""):
    """
    Executes an HTTP request and returns the result in a string

    Args:
        url (str): the full URL to send a request to
        method (str): the HTTP method to use
        payload (str): the json payload to send if appropriate for HTTP method (default "")

    Returns:
        str: the content returned by the server
    """
    if print_calls:
        print(url)

    response = None
    try:
        if payload:
            payload = payload.encode("UTF-8")
            request = urllib.request.Request(url, method=method, data=payload)
            request.add_header("Content-Type", "application/json")
        else:
            request = urllib.request.Request(url, method=method)
        request.add_header("Accept-Encoding", "gzip")
        response = urllib.request.urlopen(request)
        content = response.read()
        if content:
            if "gzip" == response.getheader("Content-Encoding"):
                content = zlib.decompress(content, zlib.MAX_WBITS | 16).decode(encoding="UTF-8")
            else:
                content = content.decode("UTF-8")
        return content
    finally:
        if response:
            response.close()
