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
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    [ham-project.domain1]
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    cmd = 'update-txconfig-resources'
    options, args = commands.parse_option([cmd, '-d', 'locale'])
    commands.commands[cmd](options)

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project\.README\]', data)


@in_tmp()
def test_update_txconfig_resources_with_pot_dir_argument(temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    [ham-project.domain1]
    """))

    cmd = 'update-txconfig-resources'
    cmd_args = [cmd, '-d', 'locale', '-p', '_build/locale']
    options, args = commands.parse_option(cmd_args)
    commands.commands[cmd](options)

    data = (tx_dir / 'config').text().replace('\\', '/')
    assert re.search(r'\[ham-project\.README\]', data)
    assert re.search(r'source_file = _build/locale/README.pot', data)


@in_tmp()
def test_update_txconfig_resources_with_project_name_including_dots(temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    cmd = 'update-txconfig-resources'
    cmd_args = [cmd, '-d', 'locale',
                '--transifex-project-name', 'ham-project.com']
    options, args = commands.parse_option(cmd_args)
    commands.commands[cmd](options)

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-projectcom\.README\]', data)


@in_tmp()
def test_update_txconfig_resources_with_project_name_including_spaces(temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    cmd = 'update-txconfig-resources'
    cmd_args = [cmd, '-d', 'locale',
                '--transifex-project-name', 'ham project com']
    options, args = commands.parse_option(cmd_args)
    commands.commands[cmd](options)

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project-com\.README\]', data)


@in_tmp()
def test_update_txconfig_resources_with_potfile_including_symbols(temp):
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

    cmd = 'update-txconfig-resources'
    cmd_args = [cmd, '-d', 'locale',
                '--transifex-project-name', 'ham project com']
    options, args = commands.parse_option(cmd_args)
    commands.commands[cmd](options)

    data = (tx_dir / 'config').text()
    assert re.search(r'\[ham-project-com\.example_document\]', data)
    assert re.search(r'\[ham-project-com\.test_document\]', data)
