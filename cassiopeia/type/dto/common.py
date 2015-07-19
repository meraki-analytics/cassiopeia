import json
import sqlalchemy
import sqlalchemy.types
import sqlalchemy.ext.declarative

class CassiopeiaDto(object):
    def __init__(self, dictionary):
        for k,v in dictionary.items():
            setattr(self, k, v)

    def to_json(self):
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


BaseDB = sqlalchemy.ext.declarative.declarative_base()


class JSONEncoded(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value