import json


class CassiopeiaDto(object):
    """
    A Python representation of an object returned by the RiotAPI
    """

    def __init__(self, dictionary):
        """
        A Python representation of an object returned by the RiotAPI
        """
        for k, v in dictionary.items():
            setattr(self, k, v)

    def to_json(self, **kwargs):
        """
        Args:
            dictionary (dict): the JSON data returned from the Riot API as a dict
        """
        dictionary = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        default = kwargs.pop("default", lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith("_")})
        sort_keys = kwargs.pop("sort_keys", True)
        indent = kwargs.pop("indent", 4)
        return json.dumps(dictionary, default=default, sort_keys=sort_keys, indent=indent, **kwargs)

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


class CassiopeiaParametersDto(CassiopeiaDto):
    """
    Gets a JSON representation of the object

    Returns:
        str: a JSON representation of the object
    """

    def to_json(self, **kwargs):
        """
        Gets a JSON representation of the object

        Returns:
            str: a JSON representation of the object
        """
        dictionary = {k: v for k, v in self.__dict__.items() if not k.startswith("_") and v}
        default = kwargs.pop("default", lambda o: {k: v for k, v in o.__dict__.items() if not k.startswith("_") and v})
        sort_keys = kwargs.pop("sort_keys", True)
        indent = kwargs.pop("indent", 4)
        return json.dumps(dictionary, default=default, sort_keys=sort_keys, indent=indent, **kwargs)
