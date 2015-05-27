from cassiopeia.type.dto.common import CassiopeiaDto

class Shard(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Hostname
        self.hostname = dictionary["hostname"]

        # list<string> # Locales
        self.locales = dictionary["locales"]

        # string # Name
        self.name = dictionary["name"]

        # string # Region tag
        self.region_tag = dictionary["region_tag"]

        # string # Slug
        self.slug = dictionary["slug"]


class Translation(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Content
        self.content = dictionary["content"]

        # string # Locale
        self.locale = dictionary["locale"]

        # string # Timestamp
        self.updated_at = dictionary["updated_at"]


class Message(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Author
        self.author = dictionary["author"]

        # string # Content
        self.content = dictionary["content"]

        # string # Timestamp created
        self.created_at = dictionary["created_at"]

        # long # ID
        self.id = dictionary["id"]

        # string # Legal values: Info, Alert, Error
        self.severity = dictionary["severity"]

        # list<Translation> # Translations
        self.translations = [Translation(trans) if not isinstance(trans, Translation) else trans for trans in dictionary["translations"]]

        # string # Timestamp updated
        self.updated_at = dictionary["updated_at"]


class Incident(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Active
        self.active = dictionary["active"]

        # string # Timestamp created
        self.created_at = dictionary["created_at"]

        # long # ID
        self.id = dictionary["id"]

        # list<Message> # Updates
        self.updates = [Message(msg) if not isinstance(msg, Message) else msg for msg in dictionary["updates"]]


class Service(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Incident> # Incidents
        self.incidents = [Incident(inc) if not isinstance(inc, Incident) else inc for inc in dictionary["incidents"]]

        # string # Name
        self.name = dictionary["name"]

        # string # Slug
        self.slug = dictionary["slug"]

        # string # Legal values: Online, Alert, Offline, Deploying
        self.status = dictionary["status"]


class ShardStatus(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Hostname
        self.hostname = dictionary["hostname"]

        # list<string> # Locales
        self.locales = dictionary["locales"]

        # string # Name
        self.name = dictionary["name"]

        # string # Region tag
        self.region_tag = dictionary["region_tag"]

        # list<Service> # Services
        self.services = [Service(srvc) if not isinstance(srvc, Service) else srvc for srvc in dictionary["services"]]

        # string # Slug
        self.slug = dictionary["slug"]