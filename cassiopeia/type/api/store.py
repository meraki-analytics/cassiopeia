import sqlalchemy
import sqlalchemy.orm

import cassiopeia.type.dto.common

class Cache(object):
    def __init__(self):
        self._cache = {}
        self._has_all = {}

    def has_all(self, class_):
        try:
            return self._has_all[class_]
        except(KeyError):
            return False

    def get_all(self, class_):
        results = []
        try:
            for obj in self._cache[class_].items():
                results.append(obj[1])
        except(KeyError):
            pass

        return results

    def iterate(self, class_):
        try:
            iter(self._cache[class_].values())
        except(KeyError):
            return iter([])

    def get(self, class_, keys, key_field):
        if(class_ not in self._cache):
            if(not isinstance(keys, list)):
                return None
            else:
                results = []
                for _ in range(len(keys)):
                    results.append(None)
                return results

        if(not isinstance(keys, list)):
            try:
                return self._cache[class_][keys]
            except(KeyError):
                return None
        else:
            results = []
            for key in keys:
                try:
                    results.append(self._cache[class_][key])
                except(KeyError):
                    results.append(None)
            return results

    def store(self, objs, keys, complete_sets=[]):
        is_list = isinstance(objs, list)
        if(is_list != isinstance(keys, list)):
            raise ValueError("Object(s) and Key(s) must both be lists or both be non-lists")

        if(not is_list):
            class_ = type(objs)
            if(class_ not in self._cache):
                self._cache[class_] = {}
            self._cache[class_][keys] = objs
        else:
            if(len(objs) != len(keys)):
                raise ValueError("Objects and Keys must be the same length")

            for i in range(len(objs)):
                class_ = type(objs[i])
                if(class_ not in self._cache):
                    self._cache[class_] = {}
                self._cache[class_][keys[i]] = objs[i]

        if(complete_sets):
            for class_ in complete_sets:
                self._has_all[class_] = True


class HasAllStatus(cassiopeia.type.dto.common.BaseDB):
    __tablename__ = "HasAll"
    class_ = sqlalchemy.Column(sqlalchemy.String(50), primary_key=True)
    have_all = sqlalchemy.Column(sqlalchemy.Boolean)

    def get_name(class_):
        return "{module}.{name}".format(module=class_.dto_type.__module__, name=class_.dto_type.__name__)

    def __init__(self, class_, have_all=True):
        self.class_ = HasAllStatus.get_name(class_)
        self.have_all = have_all


class SQLAlchemyDB(object):
    class Iterator(object):
        def __init__(self, class_, result):
            self.class_ = class_
            self.result = result

        def __next__(self):
            try:
                val = self.class_(self.result[self.index])
                self.index += 1
                return val
            except(IndexError):
                raise StopIteration

        def __iter__(self):
            self.index = 0
            return self

    def __init__(self, flavor, host, database, username, password):
        self.db = sqlalchemy.create_engine("{flavor}://{username}:{password}@{host}/{database}".format(flavor=flavor, host=host, database=database, username=username, password=password))
        cassiopeia.type.dto.common.BaseDB.metadata.create_all(self.db)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.db)()

    def has_all(self, class_):
        class_name = HasAllStatus.get_name(class_)
        has_all = self.session.query(HasAllStatus).filter(HasAllStatus.class_==class_name).first()
        return has_all.have_all if has_all else False

    def get_all(self, class_):
        return [class_(dto) for dto in self.session.query(class_.dto_type).all()]

    def iterate(self, class_):
        return SQLAlchemyDB.Iterator(class_, self.session.query(class_.dto_type).all())

    def get(self, class_, keys, key_field):
        if(not isinstance(keys, list)):
            val = self.session.query(class_.dto_type).filter(getattr(class_.dto_type, key_field)==keys).first()
            return class_(val) if val else None
        else:
            from_db = self.session.query(class_.dto_type).filter(getattr(class_.dto_type, key_field).in_(keys)).all()
            from_db = {getattr(x, key_field): x for x in from_db}
            
            results = []
            for key in keys:
                try:
                    val = from_db[key]
                    results.append(class_(val) if val else None)
                except KeyError:
                    results.append(None)
            return results

    def store(self, objs, keys=None, complete_sets=[]):
        if(not isinstance(objs, list)):
            class_ = objs.data.__class__
            p_key = class_.__mapper__.primary_key[0].name.split("\\.")[-1]
            val = self.session.query(class_).filter(getattr(class_, p_key)==getattr(objs.data, p_key)).first()
            if(not val):
                self.session.add(objs.data)
        else:
            class_ = objs[0].data.__class__
            p_key = class_.__mapper__.primary_key[0].name.split("\\.")[-1]
            to_store = {getattr(obj.data, p_key): obj.data for obj in objs}

            for obj in self.session.query(class_).filter(getattr(class_, p_key).in_(to_store.keys())).all():
                del to_store[getattr(obj, p_key)]

            self.session.add_all(to_store.values())
        
        if(complete_sets):
            classes = {HasAllStatus.get_name(class_): HasAllStatus(class_) for class_ in complete_sets}
            for obj in self.session.query(HasAllStatus).filter(HasAllStatus.class_.in_(classes.keys())).all():
                if(not obj.have_all):
                    obj.have_all = True
                del classes[obj.class_]
            self.session.add_all(classes.values())

        self.session.commit()

    def close(self):
        self.session.close()
        self.db.dispose()