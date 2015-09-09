import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.summoner import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_rune_page():
    global RunePage
    @cassiopeia.type.core.common.inheritdocs
    class RunePage(RunePage, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "RunePage"
        current = sqlalchemy.Column(sqlalchemy.Boolean)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String(50))
        slots = sqlalchemy.orm.relationship("cassiopeia.type.dto.summoner.RuneSlot", cascade="all, delete-orphan, delete, merge", passive_deletes=True)

def _sa_bind_rune_slot():
    global RuneSlot
    @cassiopeia.type.core.common.inheritdocs
    class RuneSlot(RuneSlot, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "RuneSlot"
        runeId = sqlalchemy.Column(sqlalchemy.Integer)
        runeSlotId = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _page_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("RunePage.id", ondelete="CASCADE"))

def _sa_bind_mastery_page():
    global MasteryPage
    @cassiopeia.type.core.common.inheritdocs
    class MasteryPage(MasteryPage, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MasteryPage"
        current = sqlalchemy.Column(sqlalchemy.Boolean)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        masteries = sqlalchemy.orm.relationship("cassiopeia.type.dto.summoner.Mastery", cascade="all, delete-orphan, delete, merge", passive_deletes=True)
        name = sqlalchemy.Column(sqlalchemy.String(50))

def _sa_bind_mastery():
    global Mastery
    @cassiopeia.type.core.common.inheritdocs
    class Mastery(Mastery, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MasterySlot"
        id = sqlalchemy.Column(sqlalchemy.Integer)
        rank = sqlalchemy.Column(sqlalchemy.Integer)
        _id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        _page_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("MasteryPage.id", ondelete="CASCADE"))

def _sa_bind_summoner():
    global Summoner
    @cassiopeia.type.core.common.inheritdocs
    class Summoner(Summoner, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "Summoner"
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        name = sqlalchemy.Column(sqlalchemy.String(30))
        profileIconId = sqlalchemy.Column(sqlalchemy.Integer)
        revisionDate = sqlalchemy.Column(sqlalchemy.BigInteger)
        summonerLevel = sqlalchemy.Column(sqlalchemy.Integer)

def _sa_bind_all():
    _sa_bind_rune_page()
    _sa_bind_rune_slot()
    _sa_bind_mastery_page()
    _sa_bind_mastery()
    _sa_bind_summoner()