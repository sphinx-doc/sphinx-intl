===========
Development
===========

Code of Conduct
===============

.. include:: ../CODE_OF_CONDUCT.rst

Contribution Guideline
======================

.. include:: ../CONTRIBUTING.rst

Setup development environment
=============================

* Requires supported Python version
* do setup under sphinx-intl.git repository root as::

    $ pip install -U pip setuptools wheel setuptools_scm
    $ pip install -r requirements-testing.txt

Testing
=======

Tests with supported python version that are in:

* ``setup.py``
* ``tox.ini``
* ``.travis.yml``


Run test
--------

Just run tox::

   $ tox

tox have several sections for testing.

CI (Continuous Integration)
----------------------------

All tests will be run on Travis CI service.

* https://travis-ci.org/sphinx-doc/sphinx-intl

Releasing
=========

New package version
-------------------

The sphinx-intl package will be uploaded to PyPI: https://pypi.org/project/sphinx-intl/.

Here is a release procefure for releasing.

.. include:: ../checklist.rst


Updated documentation
---------------------

Sphinx documentation under ``doc/`` directory on the master branch will be automatically uploaded into ReadTheDocs: http://sphinx-intl.rtfd.io/.

