===========
Quick Start
===========

Installation
============

Please install sphinx-intl with using pip (8.1.1 or later).

.. code-block:: bash

   $ pip install sphinx-intl


QuickStart for sphinx translation
===================================

This section describe to translate with Sphinx_ and `sphinx-intl` command.

1. Create your document by using Sphinx.

2. Add configurations to your `conf.py`::

      locale_dirs = ['locale/']   # path is example but recommended.
      gettext_compact = False     # optional.

   `locale_dirs` is required and `gettext_compact` is optional.

3. Extract document's translatable messages into pot files::

      $ make gettext

4. Setup/Update your `locale_dir`::

      $ sphinx-intl update -p _build/gettext -l de -l ja

   Done. You got these directories that contain po files:

   * `./locale/de/LC_MESSAGES/`
   * `./locale/ja/LC_MESSAGES/`

5. Translate your po files under `./locale/<lang>/LC_MESSAGES/`.

6. Build mo files and make translated document::

      $ sphinx-intl build
      $ make -e SPHINXOPTS="-D language='ja'" html

That's all!

For more information, please refer :doc:`refs`.

.. _Sphinx: http://sphinx-doc.org
