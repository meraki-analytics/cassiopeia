import sys
import os
import configparser

try:
    import ujson as json
except ImportError:
    import json


head, tail = os.path.split(__file__)
if len(sys.argv) > 1 and any(fn.endswith(".json") for fn in sys.argv):
    for fn in sys.argv:
        if fn.endswith(".json"):
            filename = fn
            break
else:
    filename = os.path.join(head, "default.json")

if not os.path.exists(filename):
    filename = os.path.join(head, filename)
    if not os.path.exists(filename):
        filename = os.path.join(head, "default.json")

config = json.loads(open(filename).read())
if "logging" not in config:
    config["logging"] = {}
assert "Riot API" in config and "key" in config["Riot API"]