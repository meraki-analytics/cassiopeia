import sys
import os

try:
    import ujson as json
except ImportError:
    import json


head, tail = os.path.split(__file__)
default_filename = os.path.normpath(os.path.join(head, "default.json"))
jupyter_kernel_json_filepath = os.path.normpath(os.path.join("jupyter", "runtime", "kernel"))

filename = None
if len(sys.argv) > 1 and any(fn.endswith(".json") for fn in sys.argv):
    for fn in sys.argv:
        if fn.endswith(".json") and jupyter_kernel_json_filepath not in fn:
            filename = fn
            break

if filename is None:
    filename = default_filename

if not os.path.exists(filename):
    filename = os.path.normpath(os.path.join(head, filename))
    if not os.path.exists(filename):
        print("WARNING! Could not find settings file {}, using default.".format(filename))
        filename = os.path.normpath(os.path.join(head, "default.json"))

config = json.loads(open(filename).read())
if "logging" not in config:
    config["logging"] = {}
assert "Riot API" in config and "key" in config["Riot API"]
