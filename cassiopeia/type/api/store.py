class Cache(object):
    def __init__(self):
        self.cache = {}

    def get(self, class_, keys):
        if(class_ not in self.cache):
            if(not isinstance(keys, list)):
                return None
            else:
                results = []
                for _ in range(len(keys)):
                    results.append(None)

        if(not isinstance(keys, list)):
            try:
                return self.cache[class_][keys]
            except(KeyError):
                return None
        else:
            results = []
            for key in keys:
                try:
                    results.append(self.cache[class_][key])
                except(KeyError):
                    results.append(None)
            return results

    def store(self, objs, keys):
        is_list = isinstance(objs, list)
        if(is_list is not isinstance(keys, list)):
            raise ValueError("Object(s) and Key(s) must both be lists or both be non-lists")

        if(not is_list):
            class_ = type(objs)
            if(class_ not in self.cache):
                self.cache[class_] = {}
            self.cache[class_][keys] = objs
        else:
            if(len(objs) is not len(keys)):
                raise ValueError("Objects and Keys must be the same length")

            for i in range(len(objs)):
                class_ = type(objs[i])
                if(class_ not in self.cache):
                    self.cache[class_] = {}
                self.cache[class_][keys[i]] = objs[i]