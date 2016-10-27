import cassiopeia.type.core.common
import cassiopeia.type.dto.common


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
        self.translations = [(Translation(trans) if not isinstance(trans, Translation) else trans) for trans in
                             dictionary.get("translations", []) if trans]
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
        self.updates = [(Message(msg) if not isinstance(msg, Message) else msg) for msg in dictionary.get("updates", [])
                        if msg]


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
        self.incidents = [(Incident(inc) if not isinstance(inc, Incident) else inc) for inc in
                          dictionary.get("incidents", []) if inc]
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
        self.services = [(Service(srvc) if not isinstance(srvc, Service) else srvc) for srvc in
                         dictionary.get("services", []) if srvc]
        self.slug = dictionary.get("slug", "")
