from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("sphinx_intl")
except PackageNotFoundError:
    # package is not installed
    pass
