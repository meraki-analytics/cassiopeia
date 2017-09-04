from typing import Dict
import os

try:
    import ujson as json
except ImportError:
    import json


def load_config(filename = None) -> Dict:
    head, tail = os.path.split(__file__)

    if filename is not None:
        if not os.path.exists(filename):
            filename = os.path.normpath(os.path.join(head, filename))
            if not os.path.exists(filename):
                print("WARNING! Could not find settings file {}, using default.".format(filename))

        config = json.loads(open(filename).read())
    else:
        config = {}
    return config
