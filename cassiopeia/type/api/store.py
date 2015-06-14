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
        if(self._has_all[class_]):
            results = []
            for obj in self._cache[class_].items():
                results.append(obj[1])
            return results
        else:
            return []

    def get(self, class_, keys):
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
