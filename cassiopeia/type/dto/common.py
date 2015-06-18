import json

class CassiopeiaDto(object):
    def __init__(self, dictionary):
        for k,v in dictionary.items():
            setattr(self, k, v)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return "{class_}({dict_})".format(class_=self.__class__.__name__, dict_=self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__
