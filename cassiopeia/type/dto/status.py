import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class Shard(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        hostname (str): hostname
        locales (list<str>): locales
        name (str): name
        region_tag (str): region tag
        slug (str): slug
    """
    def __init__(self, dictionary):
        self.hostname = dictionary.get("hostname", "")
        self.locales = dictionary.get("locales", [])
        self.name = dictionary.get("name", "")
        self.region_tag = dictionary.get("region_tag", "")
        self.slug = dictionary.get("slug", "")


@cassiopeia.type.core.common.inheritdocs
class Translation(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        content (str): content
        locale (str): locale
        updated_at (str): timestamp
    """
    def __init__(self, dictionary):
        self.content = dictionary.get("content", "")
        self.locale = dictionary.get("locale", "")
        self.updated_at = dictionary.get("updated_at", "")


@cassiopeia.type.core.common.inheritdocs
class Message(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        author (str): author
        content (str): content
        created_at (str): timestamp created
        id (int): ID
        severity (str): legal values: Info, Alert, Error
        translations (list<Translation>): translations
        updated_at (str): timestamp updated
    """
    def __init__(self, dictionary):
        self.author = dictionary.get("author", "")
        self.content = dictionary.get("content", "")
        self.created_at = dictionary.get("created_at", "")
        self.id = dictionary.get("id", 0)
        self.severity = dictionary.get("severity", "")
        self.translations = [(Translation(trans) if not isinstance(trans, Translation) else trans) for trans in dictionary.get("translations", []) if trans]
        self.updated_at = dictionary.get("updated_at", "")


@cassiopeia.type.core.common.inheritdocs
class Incident(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        active (bool): active
        created_at (str): timestamp created
        id (int): ID
        updates (list<Message>): updates
    """
    def __init__(self, dictionary):
        self.active = dictionary.get("active", False)
        self.created_at = dictionary.get("created_at", "")
        self.id = dictionary.get("id", 0)
        self.updates = [(Message(msg) if not isinstance(msg, Message) else msg) for msg in dictionary.get("updates", []) if msg]


@cassiopeia.type.core.common.inheritdocs
class Service(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        incidents (list<Incident>): incidents
        name (str): name
        slug (str): slug
        status (str): legal values: Online, Alert, Offline, Deploying
    """
    def __init__(self, dictionary):
        self.incidents = [(Incident(inc) if not isinstance(inc, Incident) else inc) for inc in dictionary.get("incidents", []) if inc]
        self.name = dictionary.get("name", "")
        self.slug = dictionary.get("slug", "")
        self.status = dictionary.get("status", "")


@cassiopeia.type.core.common.inheritdocs
class ShardStatus(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        hostname (str): hostname
        locales (list<string>): locales
        name (str): name
        region_tag (str): region tag
        services (list<Service>): services
        slug (str): slug
    """
    def __init__(self, dictionary):
        self.hostname = dictionary.get("hostname", "")
        self.locales = dictionary.get("locales", [])
        self.name = dictionary.get("name", "")
        self.region_tag = dictionary.get("region_tag", "")
        self.services = [(Service(srvc) if not isinstance(srvc, Service) else srvc) for srvc in dictionary.get("services", []) if srvc]
        self.slug = dictionary.get("slug", "")


###############################
# Dynamic SQLAlchemy bindings #
###############################
def _sa_bind_shard():
    global Shard

    @cassiopeia.type.core.common.inheritdocs
    class Shard(Shard, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Shard"
        hostname = sqlalchemy.Column(sqlalchemy.String(50))
        locales = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        region_tag = sqlalchemy.Column(sqlalchemy.String(30), primary_key=True)
        slug = sqlalchemy.Column(sqlalchemy.String(30))


def _sa_bind_translation():
    global Translation

    @cassiopeia.type.core.common.inheritdocs
    class Translation(Translation, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Translation"
        content = sqlalchemy.Column(sqlalchemy.Text)
        locale = sqlalchemy.Column(sqlalchemy.String(30))
        updated_at = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _message_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Message.id", ondelete="CASCADE"))


def _sa_bind_message():
    global Message

    @cassiopeia.type.core.common.inheritdocs
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


def _sa_bind_incident():
    global Incident

    @cassiopeia.type.core.common.inheritdocs
    class Incident(Incident, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Incident"
        active = sqlalchemy.Column(sqlalchemy.Boolean)
        created_at = sqlalchemy.Column(sqlalchemy.String(30))
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        updates = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Message", cascade="all, delete-orphan", passive_deletes=True)
        _service_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("Service._id", ondelete="CASCADE"))


def _sa_bind_service():
    global Service

    @cassiopeia.type.core.common.inheritdocs
    class Service(Service, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Service"
        incidents = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Incident", cascade="all, delete-orphan", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        slug = sqlalchemy.Column(sqlalchemy.String(30))
        status = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _shard_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("ShardStatus._id", ondelete="CASCADE"))


def _sa_bind_shard_status():
    global ShardStatus

    @cassiopeia.type.core.common.inheritdocs
    class ShardStatus(ShardStatus, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ShardStatus"
        hostname = sqlalchemy.Column(sqlalchemy.String(50))
        locales = sqlalchemy.Column(cassiopeia.type.dto.common.JSONEncoded)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        region_tag = sqlalchemy.Column(sqlalchemy.String(30))
        services = sqlalchemy.orm.relationship("cassiopeia.type.dto.status.Service", cascade="all, delete-orphan", passive_deletes=True)
        slug = sqlalchemy.Column(sqlalchemy.String(30))
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)


def _sa_bind_all():
    _sa_bind_shard()
    _sa_bind_translation()
    _sa_bind_message()
    _sa_bind_incident()
    _sa_bind_service()
    _sa_bind_shard_status()
