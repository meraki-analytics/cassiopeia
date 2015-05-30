import urllib.parse
import urllib.request
import json

api_versions = {
    "champion": "v1.2",
    "league": "v2.5",
    "staticdata": "v1.2"
}

api_key = ""
region = "NA"
mirror = "NA"
printCalls = False

def get(request, params={}, static=False):
    # Set server and rgn
    server = "global" if static else mirror.lower()
    rgn = ("static-data/{region}" if static else "{region}").format(region=region.lower())

    # Encode params
    params["api_key"] = api_key
    params = urllib.parse.urlencode(params)

    # Build request
    url = "https://{server}.api.pvp.net/api/lol/{region}/{request}?{params}".format(server=server, region=rgn, request=request, params=params)

    if(printCalls):
        print(url)

    # Execute request
    response = urllib.request.urlopen(url)
    content = response.read().decode(encoding="UTF-8")
    response.close()

    return json.loads(content)
