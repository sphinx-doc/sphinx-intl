import dataclasses
import multiprocessing as mp
import os
from glob import glob
from typing import Optional

import click

from . import catalog as c
from .pycompat import relpath


# ==================================
# utility functions


def get_lang_dirs(path):
    dirs = [
        relpath(d, path)
        for d in glob(path + "/[a-z]*")
        if os.path.isdir(d) and not d.endswith("pot")
    ]
    return (tuple(dirs),)


# ==================================
# commands


@dataclasses.dataclass(frozen=True)
class UpdateItem:
    po_file: str
    pot_file: str
    lang: str
    line_width: int
    ignore_obsolete: bool


@dataclasses.dataclass(frozen=True)
class UpdateResult:
    po_file: str
    status: str
    added: Optional[int] = 0
    deleted: Optional[int] = 0


def _update_single_file(update_item: UpdateItem):
    cat_pot = c.load_po(update_item.pot_file)
    if os.path.exists(update_item.po_file):
        cat = c.load_po(update_item.po_file)
        msgids = {m.id for m in cat if m.id}
        c.update_with_fuzzy(cat, cat_pot)
        new_msgids = {m.id for m in cat if m.id}
        if msgids != new_msgids:
            added = new_msgids - msgids
            deleted = msgids - new_msgids
            c.dump_po(
                update_item.po_file,
                cat,
                width=update_item.line_width,
                ignore_obsolete=update_item.ignore_obsolete,
            )
            return UpdateResult(update_item.po_file, "update", len(added), len(deleted))
        else:
            return UpdateResult(update_item.po_file, "notchanged")
    else:  # new po file
        cat_pot.locale = update_item.lang
        c.dump_po(
            update_item.po_file,
            cat_pot,
            width=update_item.line_width,
            ignore_obsolete=update_item.ignore_obsolete,
        )
        return UpdateResult(update_item.po_file, "create")


def update(
    locale_dir, pot_dir, languages, line_width=76, ignore_obsolete=False, jobs=0
):
    """
    Update specified language's po files from pot.

    :param unicode locale_dir: path for locale directory
    :param unicode pot_dir: path for pot directory
    :param tuple languages: languages to update po files
    :param number line_width: maximum line width of po files
    :param bool ignore_obsolete: ignore obsolete entries in po files
    :param number jobs: number of CPUs to use
    :return: {'create': 0, 'update': 0, 'notchanged': 0}
    :rtype: dict
    """
    status = {
        "create": 0,
        "update": 0,
        "notchanged": 0,
    }

    to_translate = []
    for dirpath, dirnames, filenames in os.walk(pot_dir):
        for filename in filenames:
            pot_file = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(pot_file)
            if ext != ".pot":
                continue
            basename = relpath(base, pot_dir)
            for lang in languages:
                po_dir = os.path.join(locale_dir, lang, "LC_MESSAGES")
                po_file = os.path.join(po_dir, basename + ".po")
                to_translate.append(
                    UpdateItem(po_file, pot_file, lang, line_width, ignore_obsolete)
                )

    with mp.Pool(processes=jobs or None) as pool:
        for result in pool.imap_unordered(_update_single_file, to_translate):
            status[result.status] += 1
            if result.status == "update":
                click.echo(
                    f"Update: {result.po_file} +{result.added}, -{result.deleted}"
                )
            elif result.status == "create":
                click.echo(f"Create: {result.po_file}")
            else:
                click.echo(f"Not Changed: {result.po_file}")

    return status


def build(locale_dir, output_dir, languages):
    """
    Build specified language's po files into mo.

    :param unicode locale_dir: path for locale directory
    :param unicode output_dir: path for mo output directory
    :param tuple languages: languages to update po files
    :return: None
    """
    for lang in languages:
        lang_dir = os.path.join(locale_dir, lang)
        for dirpath, dirnames, filenames in os.walk(lang_dir):
            dirpath_output = os.path.join(
                output_dir, os.path.relpath(dirpath, locale_dir)
            )

            for filename in filenames:
                base, ext = os.path.splitext(filename)
                if ext != ".po":
                    continue

                mo_file = os.path.join(dirpath_output, base + ".mo")
                po_file = os.path.join(dirpath, filename)

                if os.path.exists(mo_file) and os.path.getmtime(
                    mo_file
                ) > os.path.getmtime(po_file):
                    continue
                click.echo(f"Build: {mo_file}")
                cat = c.load_po(po_file)
                c.write_mo(mo_file, cat)


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

                cat = c.load_po(po_file)
                r = result[po_file.replace("\\", "/")] = {
                    "translated": len(c.translated_entries(cat)),
                    "fuzzy": len(c.fuzzy_entries(cat)),
                    "untranslated": len(c.untranslated_entries(cat)),
                }
                click.echo(
                    "{}: {} translated, {} fuzzy, {} untranslated.".format(
                        po_file,
                        r["translated"],
                        r["fuzzy"],
                        r["untranslated"],
                    )
                )

    return result
