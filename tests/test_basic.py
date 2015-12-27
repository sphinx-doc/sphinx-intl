# -*- coding: utf-8 -*-
"""
    test_basic
    ~~~~~~~~~~

    Test functions that implements pot related features.

    :copyright: Copyright 2015 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
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

    with open('_build/locale/README.pot', 'r') as f:
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


def test_build(temp):
    basic.build('locale', 'locale', ('ja',))

