"""
    test_transifex
    ~~~~~~~~~~~~~~

    Test functions that implements transifex related features.

    :copyright: Copyright 2019 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import re
from textwrap import dedent

import pytest

from sphinx_intl import transifex


def test_create_transifexrc(home_in_temp):
    transifex.create_transifexrc('spam-token')


def test_create_txconfig(home_in_temp, temp):
    transifex.create_txconfig()


def test_update_txconfig_resources(home_in_temp, temp):
    transifex.create_txconfig()
    transifex.update_txconfig_resources('eggs-org', 'ham-project', 'locale', '_build/locale')


def test_update_txconfig_resources_with_config(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    """))

    transifex.update_txconfig_resources('eggs-org', 'ham-project', 'locale', '_build/locale')

    data = (tx_dir / 'config').text().replace('\\', '/')
    assert re.search(r'\[o:eggs-org:p:ham-project:r:README\]', data)
    assert re.search(r'source_file\W*=\W*_build/locale/README.pot', data)


def test_update_txconfig_resources_with_another_pot_dir(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    [ham-project.domain1]
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    transifex.update_txconfig_resources('eggs-org', 'ham-project', 'locale', 'locale/pot')

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project:r:README\]', data)



def test_update_txconfig_resources_with_project_name_including_dots(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    transifex.update_txconfig_resources('eggs-org', 'ham-project.com', 'locale', '_build/locale')

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-projectcom:r:README\]', data)


def test_update_txconfig_resources_with_project_name_including_spaces(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    transifex.update_txconfig_resources('eggs-org', 'ham project com', 'locale', '_build/locale')

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:README\]', data)


def test_update_txconfig_resources_with_potfile_including_symbols(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    # copy README.pot to 'example document.pot'
    readme = (temp / '_build' / 'locale' / 'README.pot').text()
    (temp / '_build' / 'locale' / 'example document.pot').write_text(readme)

    # copy README.pot to 'test.document.pot'
    (temp / '_build' / 'locale' / 'test.document.pot').write_text(readme)

    transifex.update_txconfig_resources('eggs-org', 'ham project com', 'locale', '_build/locale')

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:example_document\]', data)
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:test_document\]', data)


@pytest.mark.parametrize("input,expected", [
    ('spam/ham', 'spam--ham'),
    ('spam\\ham', 'spam--ham'),
    ('ham egg.pot', 'ham_egg_pot'),
    ('spam-ham/egg.pot', 'spam-ham--egg_pot'),
    ('glossary', 'glossary_'),
    ('glossary_', 'glossary_'),
    ('settings', 'settings_'),
])
def test_normalize_resource_name(input, expected):
    _callSUT = transifex.normalize_resource_name
    assert _callSUT(input) == expected
