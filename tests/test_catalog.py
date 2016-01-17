# -*- coding: utf-8 -*-
"""
    test_catalog
    ~~~~~~~~~~~~

    Test functions that implements catalog related features.

    :copyright: Copyright 2015 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
from babel.messages import Catalog, Message


def test_write_and_read_po_file_with_non_ascii_string(temp):
    from sphinx_intl import catalog

    cat = Catalog(locale='ja', domain='domain', fuzzy=False)
    msg = Message('Hello World', u'こんにちは世界')
    cat[msg.id] = msg

    po_file = (temp / 'domain.po')
    catalog.dump_po(po_file, cat)
    cat2 = catalog.load_po(po_file)

    assert cat2[msg.id].string == msg.string
