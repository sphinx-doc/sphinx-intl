# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

from nose.tools import raises

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
