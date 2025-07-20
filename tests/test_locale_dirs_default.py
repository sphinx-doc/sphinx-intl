"""
    test_locale_dirs_default
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Test locale_dirs default value handling.

    :copyright: Copyright 2025 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import os
from unittest import mock
from pathlib import Path

import pytest
from click.testing import CliRunner

from sphinx_intl.commands import main


def test_locale_dirs_explicit_setting(tmp_path: Path):
    """Test that explicit locale_dirs setting is respected in ctx.locale_dir."""
    # Arrange
    conf_content = """locale_dirs = ['custom_locale']"""
    conf_path = tmp_path / 'conf.py'
    conf_path.write_text(conf_content)
    pot_dir = tmp_path / '_build' / 'gettext'
    pot_dir.mkdir(parents=True)
    (pot_dir / 'test.pot').write_text('msgid "test"')
    
    # Act
    with mock.patch('sphinx_intl.commands.basic.update') as mock_update:
        result = CliRunner().invoke(main, ['-c', str(conf_path), 'update', '-p', str(pot_dir), '-l', 'ja'])
        
    # Assert
    assert mock_update.called, "basic.update should have been called"
    called_locale_dir = mock_update.call_args[0][0]
    expected_locale_dir = str(tmp_path / 'custom_locale')
    assert called_locale_dir == expected_locale_dir


def test_locale_dirs_default_value(tmp_path: Path):
    """
    Test that default locale_dirs value ['locales'] is used when not specified.
    
    This also serves as a regression test for issue #116: locale_dir should be
    set relative to conf.py location, not relative to the current working directory.
    """
    # Arrange
    # No locale_dirs setting - should use default ['locales']
    conf_content = """project = 'test'"""
    conf_path = tmp_path / 'conf.py'
    conf_path.write_text(conf_content)
    pot_dir = tmp_path / '_build' / 'gettext'
    pot_dir.mkdir(parents=True)
    (pot_dir / 'test.pot').write_text('msgid "test"')
    
    # Act
    with mock.patch('sphinx_intl.commands.basic.update') as mock_update:
        result = CliRunner().invoke(main, ['-c', str(conf_path), 'update', '-p', str(pot_dir), '-l', 'ja'])
        
    # Assert
    assert mock_update.called, "basic.update should have been called"
    called_locale_dir = mock_update.call_args[0][0]
    expected_locale_dir = str(tmp_path / 'locales')
    assert called_locale_dir == expected_locale_dir
