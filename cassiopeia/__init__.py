import sys

if sys.version_info.major == 2:
    import future.standard_library

    future.standard_library.install_aliases()
