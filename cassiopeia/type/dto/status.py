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