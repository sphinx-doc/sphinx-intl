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

import os
import shutil
import re
from textwrap import dedent

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


@in_tmp()
def test_update_txconfig_resources_with_config(temp):
    tx_dir = os.path.join(temp, '.tx')
    os.makedirs(tx_dir)
    f = open(os.path.join(tx_dir, 'config'), 'wt')
    f.write(dedent("""\
    [main]

    [ham-project.domain1]
    """))
    f.close()

    locale_dir = os.path.join(temp, 'locale')
    pot_dir = os.path.join(locale_dir, 'pot')
    shutil.copytree(os.path.join(temp, '_build', 'locale'), pot_dir)

    cmd = 'update-txconfig-resources'
    options, args = commands.parse_option([cmd, '-d', 'locale'])
    commands.commands[cmd](options)

    f = open(os.path.join(tx_dir, 'config'), 'rt')
    data = f.read()
    assert re.search(r'\[ham-project\.README\]', data)
