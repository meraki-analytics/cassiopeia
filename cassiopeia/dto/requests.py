import urllib.parse
import urllib.request
import json

api_versions = {
    "champion": "v1.2",
    "league": "v2.5"
}

api_key = ""
region = "NA"
mirror = "NA"
printCalls = False

def get(request, params={}, static=False):
    # Set server
    server = "global" if static else mirror.lower()

    # Encode params
    params["api_key"] = api_key
    params = urllib.parse.urlencode(params)

    # Build and execute request
    url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=region.lower(), request=request, params=params)

    if(printCalls):
        print(url)

    response = urllib.request.urlopen(url)
    content = response.read().decode(encoding="UTF-8")
    response.close()

    return json.loads(content)
