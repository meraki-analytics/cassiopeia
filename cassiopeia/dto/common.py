class DtoObject(dict):

    @property
    def __dict__(self):
        return {k: v for k, v in self.items()}
