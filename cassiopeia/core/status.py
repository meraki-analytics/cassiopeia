from typing import List, Union

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy
from merakicommons.container import searchable, SearchableList

from ..configuration import settings
from ..data import Region, Platform
from .common import CoreData, CassiopeiaObject, CassiopeiaGhost


##############
# Data Types #
##############


class TranslationData(CoreData):
    _renamed = {}

    @property
    def locale(self) -> str:
        return self._dto["locale"]

    @property
    def content(self) -> str:
        return self._dto["content"]

    @property
    def updated_at(self) -> str:
        return self._dto["updated_at"]


class MessageData(CoreData):
    _renamed = {}

    @property
    def severity(self) -> str:
        return self._dto["severity"]

    @property
    def author(self) -> str:
        return self._dto["author"]

    @property
    def created_at(self) -> str:
        return self._dto["created_at"]

    @property
    def translations(self) -> List[TranslationData]:
        return [TranslationData.from_dto(trans) for trans in self._dto["translations"]]

    @property
    def updated_at(self) -> str:
        return self._dto["updated_at"]

    @property
    def content(self) -> str:
        return self._dto["content"]

    @property
    def id(self) -> str:
        return self._dto["id"]


class IncidentData(CoreData):
    _renamed = {}

    @property
    def active(self) -> bool:
        return self._dto["active"]

    @property
    def created_at(self) -> str:
        return self._dto["created_at"]

    @property
    def id(self) -> int:
        return self._dto["id"]

    @property
    def updates(self) -> List[MessageData]:
        return [MessageData.from_dto(message) for message in self._dto["updates"]]


class ServiceData(CoreData):
    _renamed = {}

    @property
    def status(self) -> str:
        return self._dto["status"]

    @property
    def incidents(self) -> List[IncidentData]:
        return [IncidentData.from_dto(inc) for inc in self._dto["incidents"]]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def slug(self) -> str:
        return self._dto["slug"]


class ShardStatusData(CoreData):
    _renamed = {}

    @property
    def region(self) -> str:
        return self._dto["region"]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def region_tag(self) -> str:
        return self._dto["region_tag"]

    @property
    def hostname(self) -> str:
        return self._dto["hostname"]

    @property
    def services(self) -> List[ServiceData]:
        return [ServiceData.from_dto(service) for service in self._dto["services"]]

    @property
    def slug(self) -> str:
        return self._dto["slug"]

    @property
    def locales(self) -> List[str]:
        return self._dto["locales"]


##############
# Core Types #
##############


@searchable({})
class Translation(CassiopeiaObject):
    _data_types = {TranslationData}

    @property
    def locale(self) -> str:
        return self._data[TranslationData].locale

    @property
    def content(self) -> str:
        return self._data[TranslationData].content

    @property
    def updated_at(self) -> str:
        return self._data[TranslationData].updated_at


class Message(CassiopeiaObject):
    _data_types = {MessageData}

    @property
    def severity(self) -> str:
        return self._data[MessageData].severity

    @property
    def author(self) -> str:
        return self._data[MessageData].author

    @property
    def created_at(self) -> str:
        return self._data[MessageData].created_at

    @property
    def translations(self) -> List[Translation]:
        return SearchableList([Translation(trans) for trans in self._data[MessageData].translations])

    @property
    def updated_at(self) -> str:
        return self._data[MessageData].updated_at

    @property
    def content(self) -> str:
        return self._data[MessageData].content

    @property
    def id(self) -> str:
        return self._data[MessageData].id


class Incident(CassiopeiaObject):
    _data_types = {IncidentData}

    @property
    def active(self) -> bool:
        return self._data[IncidentData].active

    @property
    def created_at(self) -> str:
        return self._data[IncidentData].created_at

    @property
    def id(self) -> int:
        return self._data[IncidentData].id

    @property
    def updates(self) -> List[Message]:
        return SearchableList([Message.from_data(message) for message in self._data[IncidentData].updates])


class Service(CassiopeiaObject):
    _data_types = {ServiceData}

    @property
    def status(self) -> str:
        return self._data[ServiceData].status

    @property
    def incidents(self) -> List[Incident]:
        return SearchableList([Incident.from_data(inc) for inc in self._data[ServiceData].incidents])

    @property
    def name(self) -> str:
        return self._data[ServiceData].name

    @property
    def slug(self) -> str:
        return self._data[ServiceData].slug


@searchable({})
class ShardStatus(CassiopeiaGhost):
    _data_types = {ShardStatusData}

    def __init__(self, region: Union[Region, str] = None):
        if region is None:
            region = settings.default_region
        if not isinstance(region, Region):
            region = Region(region)
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    @lazy
    def region(self) -> Region:
        return Region(self._data[ShardStatusData].region)

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    @lazy
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def name(self) -> str:
        return self._data[ShardStatusData].name

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def region_tag(self) -> str:
        return self._data[ShardStatusData].region_tag

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def hostname(self) -> str:
        return self._data[ShardStatusData].hostname

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def services(self) -> List[Service]:
        return SearchableList([Service.from_data(service) for service in self._data[ShardStatusData].services])

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def slug(self) -> str:
        return self._data[ShardStatusData].slug

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def locales(self) -> List[str]:
        return self._data[ShardStatusData].locales
