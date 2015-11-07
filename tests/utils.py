# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    Test utilities.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
import os
import tempfile
from functools import wraps
from contextlib import contextmanager

from path import path

__dir__ = path(os.path.dirname(os.path.abspath(__file__)))


def in_tmp(template_dir='root', **kwargs):
    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            tempdir = tempfile.mkdtemp(prefix='sphinx-intl-')
            tempdir = path(tempdir)
            (__dir__ / template_dir).copytree(tempdir / template_dir)
            cwd = os.getcwd()
            try:
                temp = tempdir / template_dir
                os.chdir(temp)
                func(temp, *args2, **kwargs2)
                tempdir.rmtree(ignore_errors=True)
            finally:
                os.chdir(cwd)
        return deco
    return generator


@contextmanager
def isolated_root_dir(runner):
    with runner.isolated_filesystem() as tempdir:
        tempdir = path(tempdir)
        target = tempdir / 'root'
        (__dir__ / 'root').copytree(target)
        os.chdir(target)
        yield target
