==========
References
==========

.. contents::
   :local:

Commands
========

Type `sphinx-intl` without arguments, options to show command help.


Environment Variables
=====================

All command-line options can be set with environment variables using the
format SPHINXINTL_<UPPER_LONG_NAME> . Dashes (-) have to be replaced with
underscores (_).

For example, to set the languages::

   export SPHINXINTL_LANGUAGE=de,ja

This is the same as passing the option to sphinx-intl directly::

   sphinx-intl <command> --language=de --language=ja


Sphinx conf.py
==============

Add below settings to sphinx document's conf.py if they do not exists::

   locale_dirs = ['locale/']   #for example
   gettext_compact = False     #optional


Makefile / make.bat
===================

`make gettext` will generate pot files into `_build/gettext` directory,
however it is much convenient if pot files are generated into the
`locale/pot` directory.  You can achieve this by replacing `_build/gettext`
with `locale/pot` in your `Makefile` and/or `make.bat` that was generated
by sphinx-quickstart.

