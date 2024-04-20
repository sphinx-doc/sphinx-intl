"""
    test_catalog
    ~~~~~~~~~~~~

    Test functions that implements catalog related features.

    :copyright: Copyright 2019 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
from babel.messages import Catalog, Message


def test_write_and_read_po_file_with_non_ascii_string(temp):
    from sphinx_intl import catalog

    cat = Catalog(locale='ja', domain='domain', fuzzy=False)
    msg = Message('Hello World', 'こんにちは世界')
    cat[msg.id] = msg

    po_file = (temp / 'domain.po')
    catalog.dump_po(po_file, cat)
    cat2 = catalog.load_po(po_file)

    assert cat2[msg.id].string == msg.string


def test_fuzzy_flag_on_catalog_update():
    from sphinx_intl import catalog

    cat = Catalog(locale='ja', domain='domain', fuzzy=False)
    msg = Message('Hello Internationalized Sphinx World !',
                  'こんにちは国際化されたSphinxの世界!')
    cat[msg.id] = msg
    assert not msg.fuzzy

    cat_src = Catalog(locale='en', domain='domain', fuzzy=False)
    msg_src = Message('Hello Internationalized Sphinx World ?')
    cat_src[msg_src.id] = msg_src

    catalog.update_with_fuzzy(cat, cat_src)
    assert msg.id not in cat
    assert cat[msg_src.id].fuzzy
