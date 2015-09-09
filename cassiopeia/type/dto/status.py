import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.status import *

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