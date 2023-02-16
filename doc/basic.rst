=====
Basic
=====

.. contents::
   :local:

Basic Features
===============

* create or update po files from pot files.
* build mo files from po files.

Optional features
==================
These features depends on the `transifex-client`_ tool.
Please refer Installation_ section to install it.

* create ``.transifexrc`` file from environment variable, without interactive
  input.
* create ``.tx/config`` file without interactive input.
* update ``.tx/config`` file from locale/pot files automatically.
* build mo files from po files in the locale directory.

You need to use `tx` command for below features:

* ``tx push -s`` : push pot (translation catalogs) to transifex.
* ``tx pull -l ja`` : pull po (translated catalogs) from transifex.

.. _transifex-client: https://github.com/transifex/cli


Installation
=============

It is strongly recommended to use virtualenv/venv for this procedure::

   $ pip install sphinx-intl

If you want to use `Optional Features`_, you need install Transifex CLI tool.
Please refer to `Installation instructions <https://github.com/transifex/cli#installation>`_.

