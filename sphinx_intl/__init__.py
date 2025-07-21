from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("sphinx_intl")
except PackageNotFoundError:
    # package is not installed
    pass
