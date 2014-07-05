# -*- coding: utf-8 -*-
"""
    test_commands
    ~~~~~~~~~~~~~

    Test all commands that have no special checks.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
from __future__ import with_statement

from StringIO import StringIO

from nose.tools import raises

from sphinx_intl import commands

from utils import in_tmp


def teardown_module():
    pass


@raises(RuntimeError)
@in_tmp()
def test_update_pot_notfound(temp):
    commands.update('locale')


@raises(RuntimeError)
@in_tmp()
def test_update_no_language(temp):
    commands.update('locale', '_build/locale')


@in_tmp()
def test_update_simple(temp):
    commands.update('locale', '_build/locale', language=('ja',))


@in_tmp()
def test_update_difference_detect(temp):
    out = StringIO()
    commands.update('locale', '_build/locale', language=('ja',), out=out)
    output = out.getvalue()
    assert output.count('Create:') == 1
    assert output.count('Update:') == 0
    assert output.count('Not Changed:') == 0

    with open('_build/locale/README.pot', 'a') as f:
        f.write('\nmsgid "test1"\nmsgstr ""\n')

    out.truncate(0)
    commands.update('locale', '_build/locale', out=out)
    output = out.getvalue()
    assert output.count('Create:') == 0
    assert output.count('Update:') == 1
    assert output.count('Not Changed:') == 0

    with open('_build/locale/README.pot', 'r') as f:
        d = f.read()
        d = d.replace('test1', 'test2')
    with open('_build/locale/README.pot', 'w') as f:
        f.write(d)

    out.truncate(0)
    commands.update('locale', '_build/locale', out=out)
    output = out.getvalue()
    assert output.count('Create:') == 0
    assert output.count('Update:') == 1
    assert output.count('Not Changed:') == 0

    out.truncate(0)
    commands.update('locale', '_build/locale', out=out)
    output = out.getvalue()
    assert output.count('Create:') == 0
    assert output.count('Update:') == 0
    assert output.count('Not Changed:') == 1


@in_tmp()
def test_stat(temp):
    out = StringIO()
    commands.update('locale', '_build/locale', language=('ja',), out=out)
    commands.stat('locale', out=out)
    output = out.getvalue()
    assert 'README.po : 0 translated, 0 fuzzy, 1 untranslated.' in output


@in_tmp()
def test_build(temp):
    commands.build('locale')
