# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

from nose import SkipTest
from nose.tools import raises
from six import PY3

from sphinx_intl import commands

from utils import in_tmp


def teardown_module():
    pass


@raises(RuntimeError)
@in_tmp()
def test_update_pot_notfound():
    commands.update('locale')


@in_tmp()
def test_update():
    commands.update('locale', '_build/locale')


@in_tmp()
def test_build():
    commands.build('locale')


@in_tmp()
def test_create_transifexrc():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_transifexrc('spam-id', 'egg-pw')


@in_tmp()
def test_create_txconfig():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_txconfig()


@in_tmp()
def test_update_txconfig_resources():
    if PY3:
        raise SkipTest('transifex-client not support Python3')
    commands.create_txconfig()
    commands.update_txconfig_resources('ham-project', 'locale')
