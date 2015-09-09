import sqlalchemy

import cassiopeia.type.dto.common

from cassiopeia.type.dto.pure.champion import *

###############################
# Dynamic SQLAlchemy bindings #
###############################

def _sa_bind_champion():
    global Champion
    @cassiopeia.type.core.common.inheritdocs
    class Champion(Champion, cassiopeia.type.dto.common.BaseDB):
        __tablename__ = "ChampionStatus"
        active = sqlalchemy.Column(sqlalchemy.Boolean)
        botEnabled = sqlalchemy.Column(sqlalchemy.Boolean)
        botMmEnabled = sqlalchemy.Column(sqlalchemy.Boolean)
        freeToPlay = sqlalchemy.Column(sqlalchemy.Boolean)
        id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
        rankedPlayEnabled = sqlalchemy.Column(sqlalchemy.Boolean)

def _sa_bind_all():
    _sa_bind_champion()