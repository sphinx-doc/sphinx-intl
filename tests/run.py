#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    sphinx-intl unit test driver
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This script runs the sphinx-intl unit test suite.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""

import sys
from os import path

# always test the sphinx-intl package from this directory
sys.path.insert(0, path.join(path.dirname(__file__), path.pardir))

try:
    import nose
except ImportError:
    print('The nose package is needed to run the sphinx-intl test suite.')
    sys.exit(1)

print('Running sphinx-intl test suite...')
nose.main()
