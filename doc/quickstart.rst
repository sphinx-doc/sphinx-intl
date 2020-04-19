===========
Quick Start
===========

Installation
============

Please install sphinx-intl using pip (8.1.1 or later).

.. code-block:: bash

   $ pip install sphinx-intl


QuickStart for sphinx translation
===================================

This section describe how to translate with Sphinx_ and `sphinx-intl` command.

1. Create your document by using Sphinx.

   * working-example project is here:
     https://github.com/sphinx-doc/sphinx-intl/tree/master/doc

2. Add configurations to your `conf.py`::

      locale_dirs = ['locale/']   # path is example but recommended.
      gettext_compact = False     # optional.

   `locale_dirs` is required and `gettext_compact` is optional.

   refs `example <https://github.com/sphinx-doc/sphinx-intl/blob/master/doc/conf.py#L29>`__.

3. Extract document's translatable messages into pot files::

      $ make gettext

   This invokes the sphinx gettext builder that generates ``*.pot`` files under
   ``_build/gettext`` directory.

4. Setup/Update your po files under ``locale_dir``::

      $ sphinx-intl update -p _build/gettext -l de -l ja

   After this, you get these directories that contain po files:

   * `./locale/de/LC_MESSAGES/`
   * `./locale/ja/LC_MESSAGES/`

5. Translate your ``po`` files under `./locale/<lang>/LC_MESSAGES/`.

6. Make translated document.

   On Linux/BSD::

      $ make -e SPHINXOPTS="-Dlanguage='ja'" html

   On Windows::

      $ set SPHINXOPTS=-Dlanguage=ja
      $ make html

That's all!

For more information, please refer to :doc:`refs`.

.. _Sphinx: http://sphinx-doc.org

QuickStart console log
----------------------

::

   (.venv) C:/sphinx-intl/doc> pip install -r requirements.txt sphinx-intl
   ...

   (.venv) C:/sphinx-intl/doc> tree /f
   C:.
       authors.rst
       basic.rst
       changes.rst
       conf.py
       dev.rst
       index.rst
       make.bat
       Makefile
       quickstart.rst
       refs.rst
       requirements.txt

   (.venv) C:/sphinx-intl/doc> make gettext
   Running Sphinx v2.0.1
   making output directory... done
   building [gettext]: targets for 0 template files
   building [gettext]: targets for 7 source files that are out of date
   updating environment: 7 added, 0 changed, 0 removed
   reading sources... [100%] refs
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [100%] refs
   writing message catalogs... [100%] refs
   build succeeded.

   The message catalogs are in _build/gettext.

   (.venv) C:/sphinx-intl/doc> tree /f
   C:.
   │  authors.rst
   │  basic.rst
   │  changes.rst
   │  conf.py
   │  dev.rst
   │  index.rst
   │  make.bat
   │  Makefile
   │  quickstart.rst
   │  refs.rst
   │  requirements.txt
   │
   └─_build
       └─gettext
           │  authors.pot
           │  basic.pot
           │  changes.pot
           │  dev.pot
           │  index.pot
           │  quickstart.pot
           │  refs.pot
           │
           └─.doctrees

   (.venv) C:/sphinx-intl/doc> sphinx-intl update -p _build/gettext -l de -l ja
   Create: locale/de/LC_MESSAGES/authors.po
   Create: locale/ja/LC_MESSAGES/authors.po
   Create: locale/de/LC_MESSAGES/basic.po
   Create: locale/ja/LC_MESSAGES/basic.po
   Create: locale/de/LC_MESSAGES/changes.po
   Create: locale/ja/LC_MESSAGES/changes.po
   Create: locale/de/LC_MESSAGES/dev.po
   Create: locale/ja/LC_MESSAGES/dev.po
   Create: locale/de/LC_MESSAGES/index.po
   Create: locale/ja/LC_MESSAGES/index.po
   Create: locale/de/LC_MESSAGES/quickstart.po
   Create: locale/ja/LC_MESSAGES/quickstart.po
   Create: locale/de/LC_MESSAGES/refs.po
   Create: locale/ja/LC_MESSAGES/refs.po

   (.venv) C:/sphinx-intl/doc> tree /f
   C:.
   │  authors.rst
   │  basic.rst
   │  changes.rst
   │  conf.py
   │  dev.rst
   │  index.rst
   │  make.bat
   │  Makefile
   │  quickstart.rst
   │  refs.rst
   │  requirements.txt
   │
   ├─locale
   │  ├─de
   │  │  └─LC_MESSAGES
   │  │          authors.po
   │  │          basic.po
   │  │          changes.po
   │  │          dev.po
   │  │          index.po
   │  │          quickstart.po
   │  │          refs.po
   │  │
   │  └─ja
   │      └─LC_MESSAGES
   │              authors.po
   │              basic.po
   │              changes.po
   │              dev.po
   │              index.po
   │              quickstart.po
   │              refs.po
   │
   └─_build
       └─gettext
           │  authors.pot
           │  basic.pot
           │  changes.pot
           │  dev.pot
           │  index.pot
           │  quickstart.pot
           │  refs.pot
           │
           └─.doctrees

   (.venv) C:/sphinx-intl/doc> # ================================
   (.venv) C:/sphinx-intl/doc> # Edit po files for each languages
   (.venv) C:/sphinx-intl/doc> # ================================

   (.venv) C:/sphinx-intl/doc> set SPHINXOPTS=-Dlanguage=ja

   (.venv) C:/sphinx-intl/doc> make html
   Running Sphinx v2.0.1
   loading translations [ja]... done
   making output directory... done
   building [mo]: targets for 7 po files that are out of date
   writing output... [100%] locale/ja/LC_MESSAGES/refs.mo
   building [html]: targets for 7 source files that are out of date
   updating environment: 7 added, 0 changed, 0 removed
   reading sources... [100%] refs
   looking for now-outdated files... none found
   pickling environment... done
   checking consistency... done
   preparing documents... done
   writing output... [100%] refs
   generating indices... genindex
   writing additional pages... searchc:/project/sphinx-dev/sphinx-intl/.venv/lib/site-packages/sphinx_rtd_theme/search.html:20: RemovedInSphinx30Warning: To modify script_fil
   es in the theme is deprecated. Please insert a <script> tag directly in your theme instead.
     {{ super() }}

   copying static files... done
   copying extra files... done
   dumping search index in Japanese (code: ja) ... done
   dumping object inventory... done
   build succeeded.

   The HTML pages are in _build/html.

   (.venv) C:/sphinx-intl/doc> tree /f
   C:.
   │  authors.rst
   │  basic.rst
   │  changes.rst
   │  conf.py
   │  dev.rst
   │  index.rst
   │  make.bat
   │  Makefile
   │  quickstart.rst
   │  refs.rst
   │  requirements.txt
   │
   ├─locale
   │  ├─de
   │  │  └─LC_MESSAGES
   │  │          authors.po
   │  │          basic.po
   │  │          changes.po
   │  │          dev.po
   │  │          index.po
   │  │          quickstart.po
   │  │          refs.po
   │  │
   │  └─ja
   │      └─LC_MESSAGES
   │              authors.po
   │              basic.po
   │              changes.po
   │              dev.po
   │              index.po
   │              quickstart.po
   │              refs.po
   │
   └─_build
       ├─doctrees
       │
       ├─gettext
       │  │  authors.pot
       │  │  basic.pot
       │  │  changes.pot
       │  │  dev.pot
       │  │  index.pot
       │  │  quickstart.pot
       │  │  refs.pot
       │  │
       │  └─.doctrees
       │
       └─html
           │  .buildinfo
           │  authors.html
           │  basic.html
           │  changes.html
           │  dev.html
           │  genindex.html
           │  index.html
           │  objects.inv
           │  quickstart.html
           │  refs.html
           │  search.html
           │  searchindex.js
           │
           ├─_sources
           └─_static

