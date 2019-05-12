# -*- coding: utf-8 -*-

from sphinx_intl import __version__

# -- Project information -----------------------------------------------------

project = 'sphinx-intl'
copyright = 'Sphinx team'
author = 'Sphinx team'

version = release = __version__

# -- General configuration ---------------------------------------------------

extensions = [
]

source_suffix = '.rst'
master_doc = 'index'
language = None
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
# html_theme_options = {}

