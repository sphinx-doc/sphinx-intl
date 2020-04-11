=======
CHANGES
=======

2.0.1 (2020/04/11)
==================

Environments
------------

Incompatibility
---------------

Features
--------

Documentation
-------------

Bug Fixes
---------
- #38: transifex: Sort dirs and files alphabetically

2.0.0 (2019/06/01)
==================

Environments
------------
- #31 Drop supporting Python-2.7

Incompatibility
---------------

Features
--------

Documentation
-------------

Bug Fixes
---------

1.0.0 (2019/05/12)
===================

Environments
------------
* Adopt to semver_

.. _semver: https://semver.org/spec/v2.0.0.html

Incompatibility
---------------

Features
--------

Documentation
-------------
* #6: http://sphinx-intl.rtfd.io/
* #23: Add working example for generating pot/po files

Bug Fixes
---------

0.9.12 (2019/05/12)
===================

Environments
------------
- Drop supporting Python-3.4
- Add supporting Python-3.7.

  #25: Python-3.7 introduce ``__dir__`` module function by :pep:`562`, so the
  attribute must not override for another purpose. Thanks to Julien Enselme.

Incompatibility
---------------

* #27: `settings` resource name will be renamed to `settings_` on Transifex.
  Thanks to Anthony.

Features
--------

* #28,#29: Add option `'-w', '--line-width'` for the maximum line width of PO files.
  Thanks to Armand Ciejak.

Documentation
-------------

- #22: ```_build/locale`` (for old sphinx) -> ``_build/gettext`` (for current sphinx)

Bug Fixes
---------

0.9.11 (2018/02/12)
===================

Environments
------------
* Support transifex-client~=0.13

Incompatibility
---------------

Features
--------
* #17,#18: Adding --tag -t option, to pass tags from arguments to conf.py. 


to
  Claudio Alarcon-Reyes.

Documentation
-------------

Bug Fixes
---------


0.9.10 (2017/09/13)
===================

Environments
------------
* Drop supporting Python-3.3 and 2.6
* Add supporting Python-3.6

Bug Fixes
---------

* Unit tests overwrite real .transifexrc file in HOME directory.
* #7, #8: Added `tags` variable for conf.py. Thanks to Dongping Xie.
* #15: default value of ``locale_dirs`` must be ``['locales']`` instead of
  ``['locale']``. Thanks to cocoatomo.


0.9.9 (2016/01/17)
==================

Bug Fixes
---------

* On Python-3 environment, 'update' command breaks po files.
* #4: 'fuzzy' cause crush on 'update' command.


0.9.8 (2015/12/28)
==================

Environments
------------

* Add supporting Python-3.5
* Drop supporting Python-2.5
* Use transifex-client>=0.11 for all environments
* Switch test runner to py.test
* BB#11 Switch to babel that is used with Sphinx.

Incompatibility
---------------

* `glossary` resource name will be renamed to `glossary_` on Transifex.
  Since Aug 2015, Transifex reject 'glossary' resource name because the slug is reserved.

Features
--------

* #2,#3: Add option to create MO files in a separate directory. Thanks to Campbell Barton.

Bug Fixes
---------

* #1: update_txconfig_resources command on Python 3.4/3.5 causes KeyError.


0.9.7 (2015/11/07)
==================

Environments
------------

* BB#8 Drop supporting Python-3.1 and 3.2
* BB#10 Depends to click for command-line feature.

0.9.6 (2015/09/22)
==================

Features
--------

* BB-PR#9: Support ``fuzzy`` translations. Thanks to Guilherme Brondani Torri.
* BB-PR#8: Detects pot_dir automatically if sphinx has generated. Thanks to
  Takeshi Komiya.

Bug Fixes
---------

* BB-PR#6: update_txconfig_resources command raise errors with pot filename
  including symbols and spaces. Thanks to Takeshi Komiya.
* BB-PR#7: sphinx-intl could not find conf.py in projects separating build
  and source directories. Thanks to Takeshi Komiya.
* BB-PR#10: Add __file__ to conf.py's namespace.
* On Windows environment, now using "transifex<0.9" because "transifex>=0.9" requires
  unnecessary py2exe installation.


0.9.5 (2014/07/10)
==================

Environments
------------

* Add supporting Python-3.4

Features
--------

* BB-PR#3: Skip building process if mo file is newer than po file. Thanks to
  Nozomu Kaneko.

Bug Fixes
---------

* BB-PR#2, BB-PR#4: ``update-txconfig-resources`` disregarded ``--pot-dir`` option.
  Thanks to Giacomo Spettoli, Takeshi Komiya.
* BB-PR#5: ``update-txconfig-resources`` command raise errors when project name
  includes spaces and dots. Thanks to Takeshi Komiya.

0.9.4 (2013/12/10)
===================

Environments
------------

* Now using setuptools instead of distribute.

Features
--------

* BB#3: ``update-txconfig-resources`` command now detect project-name from
  ``.tx/config`` that already exists.

Bug Fixes
---------

* sphinx-intl didn't use SPHINXINTL_CONFIG environment value.
* tox test raises a error with transifex-client-0.10

0.9.3 (2013/04/20)
===================

Bug Fixes
---------

* because ``--config`` option did not consider directory path, locale_dir
  did not contain directory path to ``conf.py`` file.

0.9.2 (2013/4/11)
===================

Features
--------

* Add ``stat`` command for displaying statistics like 'msgfmt --statistics'.
* Documentation and error messages are improved.

Bug Fixes
---------

* update command did not detect pot/po difference when translated
  count and untranslated count are not difference.


0.9.1 (2013/4/10)
===================

Environments
------------

* Add flake8 test and fix some errors.

Incompatibility
---------------

* Drop multiple ``locale directories`` feature. Now use only first directory of
  ``locale_dirs`` in conf.py.

Features
--------

* Add --pot-dir option. default is ``pot`` directory under ``locale_dir``.
  If you using Sphinx default settings, ``-p _build/locale`` is useful.
* Add append/deprecated msgid count information for ``update`` command.

Bug Fixes
---------

* Fix: ``-c`` option is not working. Thanks @tk0miya!

0.9.0 (2013/4/7)
=================
* First release that provides these commands:

  * update
  * build
  * create-transifexrc
  * create-txconfig
  * update-txconfig-resources


