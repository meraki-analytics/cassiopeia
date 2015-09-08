import json

class CassiopeiaDto(object):
    """A Python representation of an object returned by the RiotAPI"""

    def __init__(self, dictionary):
        """
        dictionary    dict    the JSON data returned from the Riot API as a dict
        """
        for k,v in dictionary.items():
            setattr(self, k, v)

    def to_json(self):
        """Gets a JSON representation of the object
        
        return    str    a JSON representation of the object
        """
        dictionary = {k: v for k,v in self.__dict__.items() if not k.startswith("_")}
        return json.dumps(dictionary, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return "{class_}({dict_})".format(class_=self.__class__.__name__, dict_=self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__ if other else False

    def __ne__(self, other):
        return self.__dict__ != other.__dict__ if other else True

    def __hash__(self):
        return hash(id(self))
