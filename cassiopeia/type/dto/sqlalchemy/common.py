import sqlalchemy
import sqlalchemy.types
import sqlalchemy.ext.declarative

from cassiopeia.type.dto.common import *

BaseDB = sqlalchemy.ext.declarative.declarative_base()

class JSONEncoded(sqlalchemy.types.TypeDecorator):
    """JSON encoded storage for SQLAlchemy"""

    impl = sqlalchemy.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
