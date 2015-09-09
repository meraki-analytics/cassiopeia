import sqlalchemy

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.matchlist import *


###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_match_reference():
    global MatchReference
    @cassiopeia.type.core.common.inheritdocs
    class MatchReference(MatchReference, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "MatchReference"
        champion = sqlalchemy.Column(sqlalchemy.Integer)
        lane = sqlalchemy.Column(sqlalchemy.String(30))
        matchId = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        platformId = sqlalchemy.Column(sqlalchemy.String(30))
        queue = sqlalchemy.Column(sqlalchemy.String(30))
        role = sqlalchemy.Column(sqlalchemy.String(30))
        season = sqlalchemy.Column(sqlalchemy.String(30))
        timestamp = sqlalchemy.Column(sqlalchemy.BigInteger)

def _sa_bind_all():
    _sa_bind_match_reference()