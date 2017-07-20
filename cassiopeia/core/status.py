import os
import datetime
from PIL.Image import Image as PILImage

from merakicommons.ghost import ghost_load_on
from merakicommons.cache import lazy, lazy_property
from merakicommons.container import searchable, SearchableList

from ..configuration import settings
from ..data import Region, Platform
from .common import DataObject, CassiopeiaObject, CassiopeiaGhost
from ..dto.summoner import SummonerDto
from .staticdata.version import VersionListData


##############
# Data Types #
##############


class TranslationData(DataObject):
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


class MessageData(DataObject):
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
        return [TranslationData(trans) for trans in self._dto["translations"]]

    @property
    def updated_at(self) -> str:
        return self._dto["updated_at"]

    @property
    def content(self) -> str:
        return self._dto["content"]

    @property
    def id(self) -> str:
        return self._dto["id"]


class IncidentData(DataObject):
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
        return [MessageData(message) for message in self._dto["updates"]]


class ServiceData(DataObject):
    _renamed = {}

    @property
    def status(self) -> str:
        return self._dto["status"]

    @property
    def incidents(self) -> List[Incident]:
        return [IncidentData(inc) for inc in self._dto["incidents"]]

    @property
    def name(self) -> str:
        return self._dto["name"]

    @property
    def slug(self) -> str:
        return self._dto["slug"]


class ShardStatusData(DataObject):
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
        return [ServiceData(service) for service in self._dto["services"]]

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
        return SearchableList([Message(message) for message in self._data[IncidentData].updates])


class Service(CassiopeiaObject):
    _data_types = {ServiceData}

    @property
    def status(self) -> str:
        return self._data[ServiceData].status

    @property
    def incidents(self) -> List[Incident]:
        return SearchableList([Incident(inc) for inc in self._data[ServiceData].incidents])

    @property
    def name(self) -> str:
        return self._data[ServiceData].name

    @property
    def slug(self) -> str:
        return self._data[ServiceData].slug


@searchable({})
class ShardStatus(CassiopeiaGhost):
    _data_types = {ShardStatusData}

    def __init__(self, *args, **kwargs):
        if "region" not in kwargs and "platform" not in kwargs:
            kwargs["region"] = settings.default_region.value
        super().__init__(*args, **kwargs)

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
        return SearchableList([Service(service) for service in self._data[ShardStatusData].services])

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def slug(self) -> str:
        return self._data[ShardStatusData].slug

    @CassiopeiaGhost.property(ShardStatusData)
    @ghost_load_on(KeyError)
    def locales(self) -> List[str]:
        return self._data[ShardStatusData].locales
