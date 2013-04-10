# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import os
import shutil
import tempfile
from functools import wraps

from nose import SkipTest
from six import PY3

import sphinx_intl


def in_tmp(*args, **kwargs):
    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            tempdir = tempfile.mkdtemp()
            cwd = os.getcwd()
            try:
                os.chdir(tempdir)
                func(*args2, **kwargs2)
                shutil.rmtree(tempdir, ignore_errors=True)
            finally:
                os.chdir(cwd)
        return deco
    return generator


def teardown_module():
    pass


@in_tmp()
def test_update():
    sphinx_intl.update('locale')


@in_tmp()
def test_build():
    sphinx_intl.build('locale')


@in_tmp()
def test_create_transifexrc():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    sphinx_intl.create_transifexrc('spam-id', 'egg-pw')


@in_tmp()
def test_create_txconfig():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    sphinx_intl.create_txconfig()


@in_tmp()
def test_update_txconfig_resources():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    sphinx_intl.create_txconfig()
    sphinx_intl.update_txconfig_resources('locale', 'ham')
