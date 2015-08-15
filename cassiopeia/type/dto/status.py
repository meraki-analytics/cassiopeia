import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class Shard(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # str # Hostname
        self.hostname = dictionary.get("hostname", "")

        # list<str> # Locales
        self.locales = dictionary.get("locales", [])

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Region tag
        self.region_tag = dictionary.get("region_tag", "")

        # str # Slug
        self.slug = dictionary.get("slug", "")


class Translation(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # str # Content
        self.content = dictionary.get("content", "")

        # str # Locale
        self.locale = dictionary.get("locale", "")

        # str # Timestamp
        self.updated_at = dictionary.get("updated_at", "")


class Message(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # str # Author
        self.author = dictionary.get("author", "")

        # str # Content
        self.content = dictionary.get("content", "")

        # str # Timestamp created
        self.created_at = dictionary.get("created_at", "")

        # int # ID
        self.id = dictionary.get("id", 0)

        # str # Legal values: Info, Alert, Error
        self.severity = dictionary.get("severity", "")

        # list<Translation> # Translations
        self.translations = [(Translation(trans) if not isinstance(trans, Translation) else trans) for trans in dictionary.get("translations", []) if trans]

        # str # Timestamp updated
        self.updated_at = dictionary.get("updated_at", "")


class Incident(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # bool # Active
        self.active = dictionary.get("active", False)

        # str # Timestamp created
        self.created_at = dictionary.get("created_at", "")

        # int # ID
        self.id = dictionary.get("id", 0)

        # list<Message> # Updates
        self.updates = [(Message(msg) if not isinstance(msg, Message) else msg) for msg in dictionary.get("updates", []) if msg]


class Service(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Incident> # Incidents
        self.incidents = [(Incident(inc) if not isinstance(inc, Incident) else inc) for inc in dictionary.get("incidents", []) if inc]

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Slug
        self.slug = dictionary.get("slug", "")

        # str # Legal values: Online, Alert, Offline, Deploying
        self.status = dictionary.get("status", "")


class ShardStatus(cassiopeia.type.dto.common.CassiopeiaDto):
    def __init__(self, dictionary):
        # str # Hostname
        self.hostname = dictionary.get("hostname", "")

        # list<string> # Locales
        self.locales = dictionary.get("locales", [])

        # str # Name
        self.name = dictionary.get("name", "")

        # str # Region tag
        self.region_tag = dictionary.get("region_tag", "")

        # list<Service> # Services
        self.services = [(Service(srvc) if not isinstance(srvc, Service) else srvc) for srvc in dictionary.get("services", []) if srvc]

        # str # Slug
        self.slug = dictionary.get("slug", "")

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_bind_shard():
    global Shard
    class Shard(Shard, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Shard"
        hostname = sqlalchemy.Column(sqlalchemy.String(50))
        locales = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        region_tag = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
        slug = sqlalchemy.Column(sqlalchemy.String(30))

def sa_bind_translation():
    global Translation
    class Translation(Translation, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Translation"
        content = sqlalchemy.Column(sqlalchemy.Text)
        locale = sqlalchemy.Column(sqlalchemy.String(30))
        updated_at = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _message_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Message.id", ondelete="CASCADE"))

def sa_bind_message():
    global Message
    class Message(Message, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Message"
        author = sqlalchemy.Column(sqlalchemy.String(30))
        content = sqlalchemy.Column(sqlalchemy.Text)
        created_at = sqlalchemy.Column(sqlalchemy.String(30))
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        severity = sqlalchemy.Column(sqlalchemy.String(30))
        translations = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Translation", cascade="all, delete-orphan", passive_deletes=True)
        updated_at = sqlalchemy.Column(sqlalchemy.String(30))
        _incident_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Incident.id", ondelete="CASCADE"))

def sa_bind_incident():
    global Incident
    class Incident(Incident, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Incident"
        active = sqlalchemy.Column(sqlalchemy.Boolean)
        created_at = sqlalchemy.Column(sqlalchemy.String(30))
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        updates = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Message", cascade="all, delete-orphan", passive_deletes=True)
        _service_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Service._id", ondelete="CASCADE"))

def sa_bind_service():
    global Service
    class Service(Service, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Service"
        incidents = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Incident", cascade="all, delete-orphan", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        slug = sqlalchemy.Column(sqlalchemy.String(30))
        status = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _shard_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("ShardStatus._id", ondelete="CASCADE"))

def sa_bind_shard_status():
    global ShardStatus
    class ShardStatus(ShardStatus, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ShardStatus"
        hostname = sqlalchemy.Column(sqlalchemy.String(50))
        locales = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        region_tag = sqlalchemy.Column(sqlalchemy.String(30))
        services = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Service", cascade="all, delete-orphan", passive_deletes=True)
        slug = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

def sa_bind_all():
    sa_bind_shard()
    sa_bind_translation()
    sa_bind_message()
    sa_bind_incident()
    sa_bind_service()
    sa_bind_shard_status()