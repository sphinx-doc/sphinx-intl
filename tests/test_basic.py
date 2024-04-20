"""
    test_basic
    ~~~~~~~~~~

    Test functions that implements pot related features.

    :copyright: Copyright 2019 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
from unittest import mock

from sphinx_intl import basic


def test_update_simple(temp):
    basic.update('locale', '_build/locale', ('ja',))


def test_update_difference_detect(temp):
    r1 = basic.update('locale', '_build/locale', ('ja',))
    assert r1 == {'create': 1, 'update': 0, 'notchanged': 0}

    with open('_build/locale/README.pot', 'a') as f:
        f.write('\nmsgid "test1"\nmsgstr ""\n')
    r2 = basic.update('locale', '_build/locale', ('ja',))
    assert r2 == {'create': 0, 'update': 1, 'notchanged': 0}

    with open('_build/locale/README.pot') as f:
        d = f.read()
        d = d.replace('test1', 'test2')
    with open('_build/locale/README.pot', 'w') as f:
        f.write(d)
    r3 = basic.update('locale', '_build/locale', ('ja',))
    assert r3 == {'create': 0, 'update': 1, 'notchanged': 0}

    r4 = basic.update('locale', '_build/locale', ('ja',))
    assert r4 == {'create': 0, 'update': 0, 'notchanged': 1}


def test_stat(temp):
    r1 = basic.update('locale', '_build/locale', ('ja',))
    r2 = basic.stat('locale', ('ja',))
    assert r2 == {'locale/ja/LC_MESSAGES/README.po': {'translated': 0, 'fuzzy': 0, 'untranslated': 1}}


def test_stat_with_multiple_languages(temp):
    r1 = basic.update('locale', '_build/locale', ('ja','de','it'))
    r2 = basic.stat('locale', ('ja','de','it'))
    assert r2 == {
        'locale/ja/LC_MESSAGES/README.po': {'translated': 0, 'fuzzy': 0, 'untranslated': 1},
        'locale/de/LC_MESSAGES/README.po': {'translated': 0, 'fuzzy': 0, 'untranslated': 1},
        'locale/it/LC_MESSAGES/README.po': {'translated': 0, 'fuzzy': 0, 'untranslated': 1},
    }


@mock.patch('sphinx_intl.catalog.write_mo')
@mock.patch('sphinx_intl.catalog.load_po')
def test_build(load_po, write_mo, temp):
    basic.update('locale', '_build/locale', ('ja',))
    basic.build('locale', 'locale', ('ja',))
    assert load_po.call_args[0][0].startswith('locale')
    assert load_po.call_args[0][0].endswith('README.po')
    assert write_mo.call_args[0][0].startswith('locale')
    assert write_mo.call_args[0][0].endswith('README.mo')


@mock.patch('sphinx_intl.catalog.write_mo')
@mock.patch('sphinx_intl.catalog.load_po')
def test_build_mo_on_another_location(load_po, write_mo, temp):
    basic.update('locale', '_build/locale', ('ja',))
    basic.build('locale', 'mo_dir', ('ja',))
    assert load_po.call_args[0][0].startswith('locale')
    assert load_po.call_args[0][0].endswith('README.po')
    assert write_mo.call_args[0][0].startswith('mo_dir')
    assert write_mo.call_args[0][0].endswith('README.mo')
