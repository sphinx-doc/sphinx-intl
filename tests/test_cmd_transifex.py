# -*- coding: utf-8 -*-
"""
    test_cmd_transifex
    ~~~~~~~~~~~~~~~~~~

    Test transifex related commands.

    :copyright: Copyright 2015 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import re
from textwrap import dedent

from click.testing import CliRunner

from sphinx_intl import commands

runner = CliRunner()


def test_create_transifexrc(home_in_temp):
    r1 = runner.invoke(commands.main,
                       [
                           'create-transifexrc',
                           '--transifex-username', 'spam-id',
                           '--transifex-password', 'egg-pw',
                       ])
    assert r1.exit_code == 0


def test_create_txconfig(home_in_temp, temp):
    r1 = runner.invoke(commands.main, ['create-txconfig'])
    assert r1.exit_code == 0


def test_update_txconfig_resources(home_in_temp, temp):
    r1 = runner.invoke(commands.main, ['create-txconfig'])
    assert r1.exit_code == 0
    r2 = runner.invoke(commands.update_txconfig_resources,
                       [
                           '--transifex-project-name', 'ham-project',
                           '-d', 'locale',
                       ])
    assert r2.exit_code == 0


def test_update_txconfig_resources_with_config(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    [ham-project.domain1]
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    r1 = runner.invoke(commands.main, ['update-txconfig-resources', '-d', 'locale'])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project\.README\]', data)


def test_update_txconfig_resources_with_pot_dir_argument(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    [ham-project.domain1]
    """))

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '-d', 'locale',
                        '-p', '_build/locale',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text().replace('\\', '/')
    assert re.search(r'\[ham-project\.README\]', data)
    assert re.search(r'source_file = _build/locale/README.pot', data)


def test_update_txconfig_resources_with_project_name_including_dots(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '-d', 'locale',
                        '--transifex-project-name', 'ham-project.com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-projectcom\.README\]', data)


def test_update_txconfig_resources_with_project_name_including_spaces(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '-d', 'locale',
                        '--transifex-project-name', 'ham project com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project-com\.README\]', data)


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

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '-d', 'locale',
                        '--transifex-project-name', 'ham project com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project-com\.example_document\]', data)
    assert re.search(r'\[ham-project-com\.test_document\]', data)
