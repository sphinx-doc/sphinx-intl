# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

from nose import SkipTest
from six import PY3

from sphinx_intl import commands

from utils import in_tmp


def setup_module():
    if PY3:
        raise SkipTest('transifex-client not support Python3')


def teardown_module():
    pass


@in_tmp()
def test_create_transifexrc(temp):
    commands.create_transifexrc('spam-id', 'egg-pw')


@in_tmp()
def test_create_txconfig(temp):
    commands.create_txconfig()


@in_tmp()
def test_update_txconfig_resources(temp):
    commands.create_txconfig()
    commands.update_txconfig_resources('ham-project', 'locale')
