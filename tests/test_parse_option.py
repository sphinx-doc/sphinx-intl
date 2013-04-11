# -*- coding: utf-8 -*-
"""
    test_parse_option
    ~~~~~~~~~~~~~~~~~

    Test parse option.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import os

from nose.tools import raises

from sphinx_intl import commands

from utils import in_tmp


def teardown_module():
    pass


@raises(SystemExit)
@in_tmp()
def test_command_not_found(temp):
    commands.parse_option(['some-command'])


@raises(RuntimeError)
@in_tmp()
def test_confpy_not_have_locale_dirs(temp):
    f = open('conf.py', 'w')
    f.close()
    commands.parse_option(['update'])


@in_tmp()
def test_confpy_have_locale_dirs(temp):
    f = open('conf.py', 'w')
    f.write('locale_dirs=["somedir"]\n')
    f.close()
    opts, args = commands.parse_option(['update'])
    assert opts.locale_dir == 'somedir'


@in_tmp()
def test_confpy_in_subdir(temp):
    os.mkdir('source')
    f = open('source/conf.py', 'w')
    f.write('locale_dirs=["somedir"]\n')
    f.close()
    opts, args = commands.parse_option(['update', '-c', 'source/conf.py'])
    assert opts.locale_dir == os.path.normpath('source/somedir')


@in_tmp()
def test_no_confpy_and_locale_dir_specified(temp):
    opts, args = commands.parse_option(['update', '-d', 'somedir'])
    assert opts.locale_dir == 'somedir'
