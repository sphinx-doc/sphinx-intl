"""
    test_cmd_transifex
    ~~~~~~~~~~~~~~~~~~

    Test transifex related commands.

    :copyright: Copyright 2019 by Takayuki SHIMIZUKAWA.
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
                           '--transifex-token', 'green-token',
                       ])
    assert r1.exit_code == 0


def test_create_txconfig(home_in_temp, temp):
    r1 = runner.invoke(commands.main, ['create-txconfig'])
    assert r1.exit_code == 0


def test_update_txconfig_resources(home_in_temp, temp):
    r1 = runner.invoke(commands.main, ['create-txconfig'])
    assert r1.exit_code == 0

    r2 = runner.invoke(commands.main,
                       [
                           'create-transifexrc',
                           '--transifex-token', 'green-token',
                       ])
    assert r2.exit_code == 0

    r3 = runner.invoke(commands.update_txconfig_resources,
                       [
                           '--transifex-organization-name', 'eggs-org',
                           '--transifex-project-name', 'ham-project',
                           '-d', 'locale',
                       ])
    assert r3.exit_code == 0


def test_update_txconfig_resources_with_config(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    r1 = runner.invoke(commands.update_txconfig_resources,
                       [
                           '--transifex-organization-name', 'eggs-org',
                           '--transifex-project-name', 'ham-project',
                           '-d', 'locale',
                       ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project:r:README\]', data)
    assert re.search(r'\nresource_name += README\n', data)


def test_update_txconfig_resources_with_pot_dir_argument(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com

    """))

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '--transifex-organization-name', 'eggs-org',
                        '--transifex-project-name', 'ham-project',
                        '-d', 'locale',
                        '-p', '_build/locale',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text().replace('\\', '/')
    assert re.search(r'\[o:eggs-org:p:ham-project:r:README\]', data)
    assert re.search(r'\nresource_name += README\n', data)
    assert re.search(r'source_file\W*=\W*_build/locale/README.pot', data)


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
                        '--transifex-organization-name', 'eggs-org',
                        '--transifex-project-name', 'ham-project.com',
                        '-d', 'locale',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-projectcom:r:README\]', data)
    assert re.search(r'\nresource_name += README\n', data)


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
                        '--transifex-organization-name', 'eggs-org',
                        '--transifex-project-name', 'ham project com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:README\]', data)
    assert re.search(r'\nresource_name += README\n', data)


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
                        '--transifex-organization-name', 'eggs-org',
                        '--transifex-project-name', 'ham project com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:example_document\]', data)
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:test_document\]', data)
    assert re.search(r'\nresource_name += example_document\n', data)
    assert re.search(r'\nresource_name += test_document\n', data)


def test_update_txconfig_resources_with_potfile_including_path_separators(home_in_temp, temp):
    tx_dir = temp / '.tx'
    tx_dir.makedirs()
    (tx_dir / 'config').write_text(dedent("""\
    [main]
    host = https://www.transifex.com
    """))

    (temp / '_build' / 'locale').copytree(temp / 'locale' / 'pot')

    # copy README.pot to 'example document.pot'
    readme = (temp / '_build' / 'locale' / 'README.pot').text()
    (temp / '_build' / 'locale' / 'example').makedirs()
    (temp / '_build' / 'locale' / 'example' / 'document.pot').write_text(readme)

    r1 = runner.invoke(commands.main,
                       ['update-txconfig-resources',
                        '-d', 'locale',
                        '--transifex-organization-name', 'eggs-org',
                        '--transifex-project-name', 'ham project com',
                        ])
    assert r1.exit_code == 0

    data = (tx_dir / 'config').text()
    assert re.search(r'\[o:eggs-org:p:ham-project-com:r:example--document\]', data)
    assert re.search(r'\nresource_name += example--document\n', data)
