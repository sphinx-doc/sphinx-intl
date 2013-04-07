# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys

install_requires = [
    'setuptools',
    'six',
    'polib',
]

if sys.version_info < (2, 7):
    install_requires.append('ordereddict')

extras_require = {
    'transifex': [
        'transifex_client',
    ]
}

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='sphinx-intl',
    version='0.9.0',
    description='Sphinx utility that make it easy to translate and to apply translation.',
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
        "Programming Language :: Python :: 2.4",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
    ],
    author = "Takayuki SHIMIZUKAWA",
    author_email = "shimizukawa@gmail.com",
    url = "https://bitbucket.org/shimizukawa/sphinx-intl",
    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    extras_require=extras_require,
    py_modules=['sphinx_intl'],
    entry_points = """\
    [console_scripts]
    sphinx-intl = sphinx_intl:main
    """,
)
