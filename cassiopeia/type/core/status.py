import datetime

import cassiopeia.type.core.common
import cassiopeia.type.dto.status

@cassiopeia.type.core.common.inheritdocs
class Shard(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.Shard

    def __str__(self):
        return self.name

    @property
    def host_name(self):
        """The domain name of the server"""
        return self.data.hostname

    @property
    def locales(self):
        """The languages that you can have api results in"""
        return self.data.locales

    @property
    def name(self):
        """The full name of the region the server is located in"""
        return self.data.name

    @property
    def platform(self):
        """The Platform (ie server) for this match"""
        return cassiopeia.type.core.common.Platform(self.data.region_tag.upper()) if self.data.region_tag else None

    @property
    def region(self):
        """The Region of the server is located in"""
        return cassiopeia.type.core.common.Region(self.data.slug.upper()) if self.data.slug else None


@cassiopeia.type.core.common.inheritdocs
class ShardStatus(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.ShardStatus

    def __str__(self):
        return "Status ({name})".format(name=self.name)

    def __iter__(self):
        return iter(self.services)

    def __len__(self):
        return len(self.services)

    def __getitem__(self, index):
        return self.services[index]

    @property
    def host_name(self):
        """The domain name of the server"""
        return self.data.hostname

    @property
    def locales(self):
        """The languages that you can have api results in"""
        return self.data.locales

    @property
    def name(self):
        """The full name of the region the server is located in"""
        return self.data.name

    @property
    def platform(self):
        """The Platform (ie server) for this match"""
        return cassiopeia.type.core.common.Platform(self.data.region_tag.upper()) if self.data.region_tag else None

    @cassiopeia.type.core.common.lazyproperty
    def services(self):
        """A list of Services that this region offers"""
        return [Service(service) for service in self.data.services]

    @property
    def region(self):
        """The Region of the server is located in"""
        return cassiopeia.type.core.common.Region(self.data.slug.upper()) if self.data.slug else None


@cassiopeia.type.core.common.inheritdocs
class Service(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.Service

    def __str__(self):
        return name

    def __iter__(self):
        return iter(self.incidents)

    def __len__(self):
        return len(self.incidents)

    def __getitem__(self, index):
        return self.incidents[index]

    @cassiopeia.type.core.common.lazyproperty
    def incidents(self):
        """The incidents associated with this Server"""
        return [Incident(incident) for incident in self.data.incidents]

    @property
    def name(self):
        """The name of this Service"""
        return self.data.name

    @property
    def slug(self):
        """The name of the Service in lowercase"""
        return self.data.slug

    @property
    def status(self):
        """The Status of the Service"""
        return self.data.status


@cassiopeia.type.core.common.inheritdocs
class Incident(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.Incident

    def __str__(self):
        return "Incident #{id_}".format(id_=self.id)

    def __iter__(self):
        return iter(self.updates)

    def __len__(self):
        return len(self.updates)

    def __getitem__(self, index):
        return self.updates[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def active(self):
        """Whether or not this Incident is active"""
        return self.data.active

    @cassiopeia.type.core.common.lazyproperty
    def created(self):
        """When this Incident was created"""
        return datetime.datetime.strptime(self.data.created_at, "%Y-%m-%dT%H:%M:%SZ") if self.data.created_at else None

    @property
    def id(self):
        """The ID of this Incident"""
        return self.data.id

    @cassiopeia.type.core.common.lazyproperty
    def updates(self):
        """The updates associated with this Incident"""
        return [Message(update) for update in self.data.updates]


@cassiopeia.type.core.common.inheritdocs
class Message(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.Message

    def __str__(self):
        return self.content

    def __iter__(self):
        return iter(self.translations)

    def __len__(self):
        return len(self.translations)

    def __getitem__(self, index):
        return self.translations[index]

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def author(self):
        """Who wrote this Message"""
        return self.author

    @property
    def content(self):
        """The content of this Message"""
        return self.content

    @cassiopeia.type.core.common.lazyproperty
    def created(self):
        """Whent his Message was created"""
        return datetime.datetime.strptime(self.data.created_at, "%Y-%m-%dT%H:%M:%SZ") if self.data.created_at else None

    @property
    def id(self):
        """The ID of this Message"""
        return self.data.id

    @property
    def severity(self):
        """The severity of this Message"""
        return self.data.severity

    @cassiopeia.type.core.common.lazyproperty
    def translations(self):
        """The translated text of this Message"""
        return {translation.locale: Translation(translation) for translation in self.data.translations}

    @cassiopeia.type.core.common.lazyproperty
    def updated(self):
        """When this Message was last updated"""
        return datetime.datetime.strptime(self.data.updated_at, "%Y-%m-%dT%H:%M:%SZ") if self.data.updated_at else None


@cassiopeia.type.core.common.inheritdocs
class Translation(cassiopeia.type.core.common.CassiopeiaObject):
    dto_type = cassiopeia.type.dto.status.Translation

    def __str__(self):
        return self.content

    @property
    def content(self):
        """The content of this Translation"""
        return self.data.content

    @property
    def locale(self):
        """The language of this Translation"""
        return self.data.locale

    @cassiopeia.type.core.common.lazyproperty
    def updated(self):
        """When this Translation was last updated"""
        return datetime.datetime.strptime(self.data.updated_at, "%Y-%m-%dT%H:%M:%SZ") if self.data.updated_at else None

###############################
# Dynamic SQLAlchemy bindings #
###############################

def sa_rebind_all():
    Shard.dto_type = cassiopeia.type.dto.status.Shard
    ShardStatus.dto_type = cassiopeia.type.dto.status.ShardStatus
    Service.dto_type = cassiopeia.type.dto.status.Service
    Incident.dto_type = cassiopeia.type.dto.status.Incident
    Message.dto_type = cassiopeia.type.dto.status.Message
    Translation.dto_type = cassiopeia.type.dto.status.Translation
