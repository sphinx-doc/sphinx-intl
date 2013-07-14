# -*- coding: utf-8 -*-
"""
    utils
    ~~~~~

    Test utilities.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import os
import shutil
import tempfile
from functools import wraps

__dir__ = os.path.dirname(os.path.abspath(__file__))


def in_tmp(template_dir='root', **kwargs):
    def generator(func):
        @wraps(func)
        def deco(*args2, **kwargs2):
            tempdir = tempfile.mkdtemp(prefix='sphinx-intl-')
            shutil.copytree(
                os.path.join(__dir__, template_dir),
                os.path.join(tempdir, template_dir))
            cwd = os.getcwd()
            try:
                temp = os.path.join(tempdir, template_dir)
                os.chdir(temp)
                func(temp, *args2, **kwargs2)
                shutil.rmtree(tempdir, ignore_errors=True)
            finally:
                os.chdir(cwd)
        return deco
    return generator
