"""
    conftest
    ~~~~~~~~

    PyTest utilities.

    :copyright: Copyright 2019 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import os

import pytest

from path import path

_dir = path(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def temp(request, tmpdir):
    template_dir = 'root'

    tmpdir = path(tmpdir)
    (_dir / template_dir).copytree(tmpdir / template_dir)
    cwd = os.getcwd()
    temp = tmpdir / template_dir
    os.chdir(temp)

    def fin():
        os.chdir(cwd)
    request.addfinalizer(fin)
    return temp


@pytest.fixture(scope="function")
def home_in_temp(request, tmpdir):
    """change HOME environment variable to temporary location

     To avoid real .transifexrc will be rewritten.
     """
    home = os.environ.get('HOME')
    os.environ['HOME'] = tmpdir.strpath

    def fin():
        del os.environ['HOME']
        if home:
            os.environ['HOME'] = home
    request.addfinalizer(fin)
    return tmpdir
