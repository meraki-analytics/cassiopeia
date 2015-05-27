from cassiopeia.type.dto.common import CassiopeiaDto

class Shard(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Hostname
        self.hostname = dictionary.get("hostname",'')

        # list<string> # Locales
        self.locales = dictionary.get("locales",[])

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Region tag
        self.region_tag = dictionary.get("region_tag",'')

        # string # Slug
        self.slug = dictionary.get("slug",'')


class Translation(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Content
        self.content = dictionary.get("content",'')

        # string # Locale
        self.locale = dictionary.get("locale",'')

        # string # Timestamp
        self.updated_at = dictionary.get("updated_at",'')


class Message(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Author
        self.author = dictionary.get("author",'')

        # string # Content
        self.content = dictionary.get("content",'')

        # string # Timestamp created
        self.created_at = dictionary.get("created_at",'')

        # long # ID
        self.id = dictionary.get("id",0)

        # string # Legal values: Info, Alert, Error
        self.severity = dictionary.get("severity",'')

        # list<Translation> # Translations
        self.translations = [Translation(trans) if not isinstance(trans, Translation) else trans for trans in dictionary.get("translations",[])]

        # string # Timestamp updated
        self.updated_at = dictionary.get("updated_at",'')


class Incident(CassiopeiaDto):
    def __init__(self, dictionary):
        # boolean # Active
        self.active = dictionary.get("active",False)

        # string # Timestamp created
        self.created_at = dictionary.get("created_at",'')

        # long # ID
        self.id = dictionary.get("id",0)

        # list<Message> # Updates
        self.updates = [Message(msg) if not isinstance(msg, Message) else msg for msg in dictionary.get("updates",[])]


class Service(CassiopeiaDto):
    def __init__(self, dictionary):
        # list<Incident> # Incidents
        self.incidents = [Incident(inc) if not isinstance(inc, Incident) else inc for inc in dictionary.get("incidents",[])]

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Slug
        self.slug = dictionary.get("slug",'')

        # string # Legal values: Online, Alert, Offline, Deploying
        self.status = dictionary.get("status",'')


class ShardStatus(CassiopeiaDto):
    def __init__(self, dictionary):
        # string # Hostname
        self.hostname = dictionary.get("hostname",'')

        # list<string> # Locales
        self.locales = dictionary.get("locales",[])

        # string # Name
        self.name = dictionary.get("name",'')

        # string # Region tag
        self.region_tag = dictionary.get("region_tag",'')

        # list<Service> # Services
        self.services = [Service(srvc) if not isinstance(srvc, Service) else srvc for srvc in dictionary.get("services",[])]

        # string # Slug
        self.slug = dictionary.get("slug",'')