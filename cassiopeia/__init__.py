import sys

if (sys.version_info.major == 2):
    import future.standard_library

    future.standard_library.install_aliases()

    # __all__ = ('basestring')
    # # import __builtin__
    # # __builtin__.str = unicode
    # basestring = str
    # str = unicode
    #
    # python 3 renames str -> bytes and unicode -> str
    # #str = unicode
    # from future.builtins.misc import super
    import __builtin__
    __builtin__.str = unicode
