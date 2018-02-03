from typing import List, Union

from merakicommons.cache import lazy
from merakicommons.container import searchable, SearchableList

from ..data import Region, Platform
from .common import CoreData, CassiopeiaObject, CassiopeiaGhost, provide_default_region, ghost_load_on


##############
# Data Types #
##############


class TranslationData(CoreData):
    _renamed = {"updated_at": "updated"}


class MessageData(CoreData):
    _renamed = {"created_at": "created", "updated_at": "updated"}

    def __call__(self, **kwargs):
        if "translations" in kwargs:
            self.translations = [TranslationData(**translation) for translation in kwargs.pop("translations")]
        super().__call__(**kwargs)
        return self


class IncidentData(CoreData):
    _renamed = {"created_at": "created"}

    def __call__(self, **kwargs):
        if "updates" in kwargs:
            self.updates = [MessageData(**update) for update in kwargs.pop("updates")]
        super().__call__(**kwargs)
        return self


class ServiceData(CoreData):
    _renamed = {}

    def __call__(self, **kwargs):
        if "incidents" in kwargs:
            self.incidents = [IncidentData(**incident) for incident in kwargs.pop("incidents")]
        super().__call__(**kwargs)
        return self


class ShardStatusData(CoreData):
    _renamed = {"region_tag": "platform"}

    def __call__(self, **kwargs):
        if "services" in kwargs:
            self.services = [ServiceData(**service) for service in kwargs.pop("services")]
        super().__call__(**kwargs)
        return self


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
    def updated(self) -> str:
        return self._data[TranslationData].updated


class Message(CassiopeiaObject):
    _data_types = {MessageData}

    @property
    def severity(self) -> str:
        return self._data[MessageData].severity

    @property
    def author(self) -> str:
        return self._data[MessageData].author

    @property
    def created(self) -> str:
        return self._data[MessageData].created

    @property
    def translations(self) -> List[Translation]:
        return SearchableList([Translation(trans) for trans in self._data[MessageData].translations])

    @property
    def updated(self) -> str:
        return self._data[MessageData].updated

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
    def created(self) -> str:
        return self._data[IncidentData].created

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

    @provide_default_region
    def __init__(self, region: Union[Region, str] = None):
        kwargs = {"region": region}
        super().__init__(**kwargs)

    def __get_query__(self):
        return {"region": self.region, "platform": self.platform}

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    @lazy
    def region(self) -> Region:
        return Region(self._data[ShardStatusData].region)

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    @lazy
    def platform(self) -> Platform:
        return self.region.platform

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    def name(self) -> str:
        return self._data[ShardStatusData].name

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    def hostname(self) -> str:
        return self._data[ShardStatusData].hostname

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    def services(self) -> List[Service]:
        return SearchableList([Service.from_data(service) for service in self._data[ShardStatusData].services])

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    def slug(self) -> str:
        return self._data[ShardStatusData].slug

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on
    def locales(self) -> List[str]:
        return self._data[ShardStatusData].locales
