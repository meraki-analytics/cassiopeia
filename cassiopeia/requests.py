import urllib.parse
import urllib.request
import json

from cassiopeia.type.exception import CassiopeiaError

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
    params = urllib.parse.urlencode(params)

    # Build request
    url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=params)

    if(print_calls):
        print(url)

    # Execute request
    response = urllib.request.urlopen(url)
    content = response.read().decode(encoding="UTF-8")
    response.close()

    return json.loads(content)
