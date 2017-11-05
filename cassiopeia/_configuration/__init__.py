from .settings import Settings, get_default_config
from .load import load_config


class MetaConfiguration(type):
    # A singleton-like metaclass that never changes the object, but instead modifies the underlying settings attribute
    # upon instantiation.
    # This is required in order to not lose the reference that gets defined in cassiopeia/__init__.py.
    def __init__(self, *args, **kwargs):
        self.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(self, settings: Settings = None):
        if self.__instance is None:
            self.__instance = super().__call__(settings)
            return self.__instance
        else:
            self.__instance._settings = settings
            return self.__instance


class CassiopeiaConfiguration(object, metaclass=MetaConfiguration):
    def __init__(self, settings: Settings = None):
        self._settings = settings

    @property
    def settings(self):
        if self._settings is None:
            config = load_config()  # Use default
            settings = Settings(config)
            self._settings = settings
        return self._settings


import sys
sys.modules["cassiopeia.configuration"] = CassiopeiaConfiguration()
