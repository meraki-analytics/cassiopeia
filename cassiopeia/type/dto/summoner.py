import cassiopeia.type.dto.common
import cassiopeia.type.core.common


if cassiopeia.type.dto.common.sqlalchemy_imported:
    import sqlalchemy
    import sqlalchemy.orm


@cassiopeia.type.core.common.inheritdocs
class RunePages(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        pages (list<RunePage>): collection of rune pages associated with the summoner
        summonerId (int): summoner ID
    """
    def __init__(self, dictionary):
        self.pages = [(RunePage(p) if not isinstance(p, RunePage) else p) for p in dictionary.get("pages", []) if p]
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def rune_ids(self):
        """
        Gets all rune IDs contained in this object
        """
        ids = set()
        for p in self.pages:
            ids = ids | p.rune_ids
        return ids


@cassiopeia.type.core.common.inheritdocs
class RunePage(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all rune IDs contained in this object
    """
    def __init__(self, dictionary):
        self.current = dictionary.get("current", False)
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.slots = [(RuneSlot(s) if not isinstance(s, RuneSlot) else s) for s in dictionary.get("slots", []) if s]

    @property
    def rune_ids(self):
        """
        Args:
            current (bool): indicates if the page is the current page
            id (int): rune page ID
            name (str): rune page name
            slots (list<RuneSlot>): collection of rune slots associated with the rune page
        """
        ids = set()
        for s in self.slots:
            if s.runeId:
                ids.add(s.runeId)
        return ids


@cassiopeia.type.core.common.inheritdocs
class RuneSlot(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        current (bool): indicates if the page is the current page
        id (int): rune page ID
        name (str): rune page name
        slots (list<RuneSlot>): collection of rune slots associated with the rune page
    """
    def __init__(self, dictionary):
        self.runeId = dictionary.get("runeId", 0)
        self.runeSlotId = dictionary.get("runeSlotId", 0)


@cassiopeia.type.core.common.inheritdocs
class MasteryPages(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all rune IDs contained in this object
    """
    def __init__(self, dictionary):
        self.pages = [(MasteryPage(p) if not isinstance(p, MasteryPage) else p) for p in dictionary.get("pages", []) if p]
        self.summonerId = dictionary.get("summonerId", 0)

    @property
    def mastery_ids(self):
        """
        Args:
            runeId (int): rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API.
            runeSlotId (int): rune slot ID.
        """
        ids = set()
        for p in self.pages:
            ids = ids | p.mastery_ids
        return ids


@cassiopeia.type.core.common.inheritdocs
class MasteryPage(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        runeId (int): rune ID associated with the rune slot. For static information correlating to rune IDs, please refer to the LoL Static Data API.
        runeSlotId (int): rune slot ID.
    """
    def __init__(self, dictionary):
        self.current = dictionary.get("current", False)
        self.id = dictionary.get("id", 0)
        self.masteries = [(Mastery(s) if not isinstance(s, Mastery) else s) for s in dictionary.get("masteries", []) if s]
        self.name = dictionary.get("name", "")

    @property
    def mastery_ids(self):
        """
        Args:
            pages (list<MasteryPage>): collection of mastery pages associated with the summoner
            summonerId (int): summoner ID
        """
        ids = set()
        for m in self.masteries:
            if m.id:
                ids.add(m.id)
        return ids


@cassiopeia.type.core.common.inheritdocs
class Mastery(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Args:
        pages (list<MasteryPage>): collection of mastery pages associated with the summoner
        summonerId (int): summoner ID
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.rank = dictionary.get("rank", 0)


@cassiopeia.type.core.common.inheritdocs
class Summoner(cassiopeia.type.dto.common.CassiopeiaDto):
    """
    Gets all mastery IDs contained in this object
    """
    def __init__(self, dictionary):
        self.id = dictionary.get("id", 0)
        self.name = dictionary.get("name", "")
        self.profileIconId = dictionary.get("profileIconId", 0)
        self.revisionDate = dictionary.get("revisionDate", 0)
        self.summonerLevel = dictionary.get("summonerLevel", 0)


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
