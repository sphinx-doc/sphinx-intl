# -*- coding: utf-8 -*-

import os
from glob import glob

import polib
import click

from pycompat import relpath


# ==================================
# utility functions

def get_lang_dirs(path):
    dirs = [relpath(d, path)
            for d in glob(path+'/[a-z]*')
            if os.path.isdir(d) and not d.endswith('pot')]
    return (tuple(dirs),)


# http://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance
# 4th version, seems short and fast enough compared to the others.
def levenshtein(seq1, seq2):
    oneago = None
    thisrow = list(range(1, len(seq2) + 1)) + [0]
    for x in range(len(seq1)):
        oneago, thisrow = thisrow, [0] * len(seq2) + [x + 1]
        for y in range(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]


# ==================================
# commands

def update(locale_dir, pot_dir, languages):
    """
    Update specified language's po files from pot.

    :param unicode locale_dir: path for locale directory
    :param unicode pot_dir: path for pot directory
    :param tuple languages: languages to update po files
    :return: {'create': 0, 'update': 0, 'notchanged': 0}
    :rtype: dict
    """
    status = {
        'create': 0,
        'update': 0,
        'notchanged': 0,
    }

    for dirpath, dirnames, filenames in os.walk(pot_dir):
        for filename in filenames:
            pot_file = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(pot_file)
            if ext != ".pot":
                continue
            basename = relpath(base, pot_dir)
            for lang in languages:
                po_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
                po_file = os.path.join(po_dir, basename + ".po")
                outdir = os.path.dirname(po_file)
                if not os.path.exists(outdir):
                    os.makedirs(outdir)

                pot = polib.pofile(pot_file)
                if os.path.exists(po_file):
                    po = polib.pofile(po_file)
                    msgids = set([str(m) for m in po])
                    po.merge(pot)
                    # merge() will place modified content as obsolete
                    # try to use obsolete translations (if any), mark as fuzzy
                    for old in po.obsolete_entries():
                        if not old.msgstr:
                            continue
                        for new in po.untranslated_entries():
                            dist = levenshtein(old.msgid, new.msgid)
                            ratio = 1. - (float(dist) / len(new.msgid))
                            # use old mgstr if msgids are 65% similar or more
                            if dist and ratio > 0.65:
                                new.msgstr = old.msgstr
                                new.flags.append('fuzzy')
                    new_msgids = set([str(m) for m in po])
                    if msgids != new_msgids:
                        added = new_msgids - msgids
                        deleted = msgids - new_msgids
                        status['update'] += 1
                        click.echo('Update: {0} +{1}, -{2}'.format(
                                po_file, len(added), len(deleted)))
                        po.save(po_file)
                    else:
                        status['notchanged'] += 1
                        click.echo('Not Changed: {0}'.format(po_file))
                else:
                    po = polib.POFile()
                    po.metadata = pot.metadata
                    status['create'] += 1
                    click.echo('Create: {0}'.format(po_file))
                    po.merge(pot)
                    po.save(po_file)

    return status


def build(locale_dir, output_dir, languages):
    """
    Update specified language's po files from pot.

    :param unicode locale_dir: path for locale directory
    :param unicode output_dir: path for mo output directory
    :param tuple languages: languages to update po files
    :return: None
    """
    use_output_dir = locale_dir != output_dir

    for lang in languages:
        lang_dir = os.path.join(locale_dir, lang)
        for dirpath, dirnames, filenames in os.walk(lang_dir):
            if use_output_dir:
                dirpath_output = os.path.join(
                        output_dir,
                        os.path.relpath(dirpath, locale_dir))

            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                if ext != ".po":
                    continue

                if use_output_dir:
                    if not os.path.exists(dirpath_output):
                        os.makedirs(dirpath_output)
                    mo_file = os.path.join(dirpath_output, filename + ".mo")
                else:
                    mo_file = base + ".mo"

                if os.path.exists(mo_file) and \
                                os.path.getmtime(mo_file) > os.path.getmtime(po_file):
                    continue
                click.echo('Build: {0}'.format(mo_file))
                po = polib.pofile(po_file)
                po.save_as_mofile(fpath=mo_file)


def stat(locale_dir, languages):
    """
    Print statistics for all po files.

    :param unicode locale_dir: path for locale directory
    :param tuple languages: languages to update po files
    :return: {'FILENAME': {'translated': 0, 'fuzzy': 0, 'untranslated': 0}, ...}
    :rtype: dict
    """
    result = {}

    for lang in languages:
        lang_dir = os.path.join(locale_dir, lang)
        for dirpath, dirnames, filenames in os.walk(lang_dir):
            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                if ext != ".po":
                    continue

                po = polib.pofile(po_file)
                r = result[po_file.replace('\\', '/')] = {
                    'translated': len(po.translated_entries()),
                    'fuzzy': len(po.fuzzy_entries()),
                    'untranslated': len(po.untranslated_entries()),
                }
                click.echo(
                    '{0}: {1} translated, {2} fuzzy, {3} untranslated.'.format(
                        po_file,
                        r['translated'],
                        r['fuzzy'],
                        r['untranslated'],
                    )
                )

    return result
