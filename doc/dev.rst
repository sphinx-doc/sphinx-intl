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
* Do setup under sphinx-intl.git repository root as::

    $ pip install -U uv
    $ uv sync

* Install Transifex CLI tool (refer to `Installation instructions <https://github.com/transifex/cli>`_)::

    $ curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash

Testing
=======

Tests with supported python version that are in:

* ``tox.ini``
* ``.github/workflow/test.yml``

Run test
--------

Just run tox::

   $ tox

tox have several sections for testing.

CI (Continuous Integration)
----------------------------

All tests will be run on GitHub Actions.

* https://github.com/sphinx-doc/sphinx-intl/tree/master/.github/workflows/

Releasing
=========

New package version
-------------------

The sphinx-intl package will be uploaded to PyPI: https://pypi.org/project/sphinx-intl/.

Here is a release procedure:

.. include:: ../checklist.rst


Updated documentation
---------------------

Sphinx documentation under ``doc/`` directory on the master branch will be automatically uploaded into ReadTheDocs: http://sphinx-intl.rtfd.io/.

