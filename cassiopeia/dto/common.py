try:
    import ujson as json
except ImportError:
    import json

try:
    import msgpack
except ImportError:
    pass

class DtoObject(dict):

    @property
    def __dict__(self):
        return {k: v for k, v in self.items()}

    def to_json(self, **kwargs):
        return json.dumps(self, **kwargs)

    def to_bytes(self, **kwargs):
        return msgpack.dumps(self, **kwargs)
