# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages
import os
import sys

from sphinx_intl import __version__

install_requires = [
    'setuptools',
    'six',
    'polib',
    'sphinx',
]

if sys.version_info < (2, 7):
    install_requires.append('ordereddict')

extras_require = {
    'test': [
        'nose',
    ],
}

if sys.version_info < (2, 6):
    extras_require['transifex'] = ['transifex_client==0.8']
elif sys.platform == 'win32':
    extras_require['transifex'] = ['transifex_client<0.9']
else:
    extras_require['transifex'] = ['transifex_client']


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
description = \
    'Sphinx utility that make it easy to translate and to apply translation.'

setup(
    name='sphinx-intl',
    version=__version__,
    description=description,
    long_description=README,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "License :: OSI Approved :: BSD License",
        "Topic :: Documentation",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: General",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
    ],
    author="Takayuki SHIMIZUKAWA",
    author_email="shimizukawa@gmail.com",
    url="https://bitbucket.org/shimizukawa/sphinx-intl",
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points="""\
    [console_scripts]
    sphinx-intl = sphinx_intl.commands:main
    """,
)
