# -*- coding: utf-8 -*-
"""
    conftest
    ~~~~~~~~

    PyTest utilities.

    :copyright: Copyright 2015 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import os

import pytest

from path import path

__dir__ = path(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="function")
def temp(request, tmpdir):
    template_dir = 'root'

    tmpdir = path(tmpdir)
    (__dir__ / template_dir).copytree(tmpdir / template_dir)
    cwd = os.getcwd()
    temp = tmpdir / template_dir
    os.chdir(temp)

    def fin():
        os.chdir(cwd)
    request.addfinalizer(fin)
    return temp
