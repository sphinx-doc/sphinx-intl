# -*- coding: utf-8 -*-
"""
    sphinx-intl
    ~~~~~~~~~~~
    Sphinx utility that make it easy to translate and to apply translation.

    :copyright: Copyright 2013 by Takayuki SHIMIZUKAWA.
    :license: BSD, see LICENSE for details.
"""
from __future__ import with_statement

import os
import sys
from six import PY3, print_, exec_, b
from glob import glob
import optparse
import textwrap
if sys.version_info < (2, 7):
    from ordereddict import OrderedDict
else:
    from collections import OrderedDict

import polib


ENVKEY_PREFIX = 'SPHINXINTL_'
FS_ENCODING = sys.getfilesystemencoding() or sys.getdefaultencoding()


####################################
# templates

TRANSIFEXRC_TEMPLATE = """\
[https://www.transifex.com]
hostname = https://www.transifex.com
password = %(transifex_password)s
username = %(transifex_username)s
token =
"""

TXCONFIG_TEMPLATE = """\
[main]
host = https://www.transifex.com
"""


commands = OrderedDict()
required = object()


####################################
# Python compat
if sys.version_info >= (2, 6):
    # Python >= 2.6
    relpath = os.path.relpath
else:
    from os.path import curdir

    def relpath(path, start=curdir):
        """Return a relative version of a path"""
        from os.path import sep, abspath, commonprefix, join, pardir

        if not path:
            raise ValueError("no path specified")

        start_list = abspath(start).split(sep)
        path_list = abspath(path).split(sep)

        # Work out how much of the filepath is shared by start and path.
        i = len(commonprefix([start_list, path_list]))

        rel_list = [pardir] * (len(start_list)-i) + path_list[i:]
        if not rel_list:
            return start
        return join(*rel_list)
    del curdir

if PY3:
    def convert_with_2to3(filepath):
        from lib2to3.refactor import RefactoringTool, get_fixers_from_package
        from lib2to3.pgen2.parse import ParseError
        fixers = get_fixers_from_package('lib2to3.fixes')
        refactoring_tool = RefactoringTool(fixers)
        source = refactoring_tool._read_python_source(filepath)[0]
        try:
            tree = refactoring_tool.refactor_string(source, 'conf.py')
        except ParseError:
            typ, err, tb = sys.exc_info()
            # do not propagate lib2to3 exceptions
            lineno, offset = err.context[1]
            # try to match ParseError details with SyntaxError details
            raise SyntaxError(err.msg, (filepath, lineno, offset, err.value))
        return str(tree)
else:
    convert_with_2to3 = None


def command(func):
    name = func.__name__.replace('_', '-')
    commands[name] = (func, [l.strip()
                             for l in func.__doc__.splitlines()
                             if l][0])

    options = OrderedDict()
    if PY3:
        argcount = func.__code__.co_argcount
        varnames = func.__code__.co_varnames[:argcount]
        defaults = list(func.__defaults__ or [])
    else:
        argcount = func.func_code.co_argcount
        varnames = func.func_code.co_varnames[:argcount]
        defaults = list(func.func_defaults or [])
    defaults = [required] * (argcount - len(defaults)) + defaults
    for name, val in zip(varnames, defaults):
        options[name] = val

    func.options = options
    return func


def execfile_(filepath, _globals):
    # get config source -- 'b' is a no-op under 2.x, while 'U' is
    # ignored under 3.x (but 3.x compile() accepts \r\n newlines)
    f = open(filepath, 'rbU')
    try:
        source = f.read()
    finally:
        f.close()

    # py25,py26,py31 accept only LF eol instead of CRLF
    if sys.version_info[:2] in ((2, 5), (2, 6), (3, 1)):
        source = source.replace(b('\r\n'), b('\n'))

    # compile to a code object, handle syntax errors
    filepath_enc = filepath.encode(FS_ENCODING)
    try:
        code = compile(source, filepath_enc, 'exec')
    except SyntaxError:
        if convert_with_2to3:
            # maybe the file uses 2.x syntax; try to refactor to
            # 3.x syntax using 2to3
            source = convert_with_2to3(filepath)
            code = compile(source, filepath_enc, 'exec')
        else:
            raise

    exec_(code, _globals)


def read_config(path):
    namespace = {}
    olddir = os.getcwd()
    try:
        if not os.path.isfile(path):
            msg = "'%s' is not found (or specify --locale_dir option)." % path
            raise RuntimeError(msg)
        os.chdir(os.path.dirname(path) or ".")
        execfile_(os.path.basename(path), namespace)
    finally:
        os.chdir(olddir)

    return namespace


def get_lang_dirs(path):
    dirs = [relpath(d, path)
            for d in glob(path+'/[a-z]*')
            if os.path.isdir(d) and not d.endswith('pot')]
    return dirs


def get_tx_root():
    import txclib.utils
    tx_root = txclib.utils.find_dot_tx()
    if tx_root is None:
        msg = "'.tx/config' not found. You need 'create-txconfig' first."
        raise RuntimeError(msg)
    return tx_root


@command
def update(locale_dir, pot_dir=None, language=()):
    """
    Update specified language's po files from pot.

    :param locale_dir: a locale directry. required.
    :param pot_dir: a pot directry. if negative, use `pot` directory under
                    `locale_dir`.
    :param language: tuple of language. if empty, all languages are specified.
    :return: None
    """
    locale_dir = locale_dir.rstrip()
    if not pot_dir:
        pot_dir = os.path.join(locale_dir, 'pot')
    if not os.path.exists(pot_dir):
        msg = ("%(pot_dir)r is not exist. Please specify pot directory with "
               "-p option, or preparing your pot files in %(pot_dir)r."
               % locals())
        raise RuntimeError(msg)
    if not language:
        language = get_lang_dirs(locale_dir)
    for dirpath, dirnames, filenames in os.walk(pot_dir):
        for filename in filenames:
            pot_file = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(pot_file)
            if ext != ".pot":
                continue
            basename = relpath(base, pot_dir)
            for lang in language:
                po_dir = os.path.join(locale_dir, lang, 'LC_MESSAGES')
                po_file = os.path.join(po_dir, basename + ".po")
                outdir = os.path.dirname(po_file)
                if not os.path.exists(outdir):
                    os.makedirs(outdir)

                pot = polib.pofile(pot_file)
                if os.path.exists(po_file):
                    po = polib.pofile(po_file)
                    trans_n = len(po.translated_entries())
                    untrans_n = len(po.untranslated_entries())
                    po.merge(pot)
                    trans_n2 = len(po.translated_entries())
                    untrans_n2 = len(po.untranslated_entries())
                    trans_d = trans_n2 - trans_n
                    untrans_d = untrans_n2 - untrans_n
                    if trans_d or untrans_d:
                        print_('Update:', po_file, "%+d, %+d" % (
                            trans_d, untrans_d))
                        po.save(po_file)
                    else:
                        print_('Not Changed:', po_file)
                else:
                    po = polib.POFile()
                    po.metadata = pot.metadata
                    print_('Create:', po_file)
                    po.merge(pot)
                    po.save(po_file)


@command
def build(locale_dir, language=()):
    """
    Build all po files into mo file.

    :param locale_dir: a locale directry. required.
    :param language: tuple of language. if empty, all languages are specified.
    :return: None
    """
    if not language:
        language = get_lang_dirs(locale_dir)
    for lang in language:
        lang_dir = os.path.join(locale_dir, lang)
        for dirpath, dirnames, filenames in os.walk(lang_dir):
            for filename in filenames:
                po_file = os.path.join(dirpath, filename)
                base, ext = os.path.splitext(po_file)
                if ext != ".po":
                    continue

                mo_file = base + ".mo"
                print_('Build: %s' % mo_file)
                po = polib.pofile(po_file)
                po.save_as_mofile(fpath=mo_file)


@command
def create_transifexrc(transifex_username, transifex_password):
    """
    Create `$HOME/.transifexrc`

    :param transifex_username: transifex username.
    :param transifex_password: transifex password.
    :return: None
    """
    target = os.path.normpath(os.path.expanduser('~/.transifexrc'))

    if os.path.exists(target):
        print_(target, 'already exists, skipped.')
        return

    if not transifex_username or not 'transifex_password':
        msg = textwrap.dedent("""\
        You need transifex username/password by command option or environment.
        command option: --transifex-username, --transifex-password
        """)
        raise RuntimeError(msg)

    with open(target, 'wt') as rc:
        rc.write(TRANSIFEXRC_TEMPLATE % locals())
    print_('Create:', target)


@command
def create_txconfig():
    """
    Create `./.tx/config`

    :return: None
    """
    target = os.path.normpath('.tx/config')
    if os.path.exists(target):
        print_(target, 'already exists, skipped.')
        return

    if not os.path.exists('.tx'):
        os.mkdir('.tx')

    with open(target, 'wt') as f:
        f.write(TXCONFIG_TEMPLATE)

    print_('Create:', target)


@command
def update_txconfig_resources(transifex_project_name, locale_dir,
                              pot_dir=None):
    """
    Update resource sections of `./.tx/config`.

    :param transifex_project_name: transifex project name.
    :param locale_dir: a locale directry. required.
    :param pot_dir: a pot directry. if negative, use `pot` directory under
                    `locale_dir`.
    :return: None
    """
    try:
        import txclib.utils
    except ImportError:
        msg = textwrap.dedent("""\
            Could not import 'txclib.utils'.
            You need install transifex_client external library.
            Please install below command if you want to this action:

                $ pip install sphinx-intl[transifex]
            """)
        raise RuntimeError(msg)

    tx_root = get_tx_root()
    args_tmpl = (
        '--auto-local -r %(transifex_project_name)s.%(resource_name)s '
        '%(locale_dir)s/<lang>/LC_MESSAGES/%(resource_path)s.po '
        '--source-lang en '
        '--source-file %(locale_dir)s/pot/%(resource_path)s.pot '
        '--execute'
    )
    if not pot_dir:
        pot_dir = os.path.join(locale_dir, 'pot')
    for dirpath, dirnames, filenames in os.walk(pot_dir):
        for filename in filenames:
            pot_file = os.path.join(dirpath, filename)
            base, ext = os.path.splitext(pot_file)
            if ext != ".pot":
                continue
            resource_path = relpath(base, pot_dir)
            pot = polib.pofile(pot_file)
            if len(pot):
                resource_name = \
                    resource_path.replace('\\', '/').replace('/', '--')
                args = (args_tmpl % locals()).split()
                txclib.utils.exec_command('set', args, tx_root)
            else:
                print_(pot_file, 'is empty, skipped')

    txclib.utils.exec_command('set', ['-t', 'PO'], tx_root)


def parse_option(argv):
    usage = textwrap.dedent("""
    %%prog [options] command

    Commands:
      %(commands)s

    Environment Variables:
      All command-line options can be set with environment variables using the
      format TXUTIL_<UPPER_LONG_NAME> . Dashes (-) have to replaced with
      underscores (_).

      For example, to set the languages:

         export SPHINXINTL_LANGUAGE=de,ja

      This is the same as passing the option to txutil directly:

         sphinx-intl --language=de --language=ja <command>
    """) % {
        'commands': '\n  '.join(
            '%s: %s' % (c, d) for c, (f, d) in commands.items())}

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-c', '--config', dest='config',
                      type='string', action='store', default='conf.py',
                      metavar='FILE',
                      help='read configurations from FILE')
    parser.add_option('-l', '--language', dest='language',
                      type='string', action='append', default=[],
                      metavar='de',
                      help='target language')
    parser.add_option('-p', '--pot-dir', dest='pot_dir',
                      type='string', action='store', default=None,
                      metavar='_build/locale',
                      help='pot files directory which is generated by sphinx. '
                           'default is `pot` directory under `locale_dir`.')
    parser.add_option('-d', '--locale-dir', dest='locale_dir',
                      type='string', action='store', default=None,
                      metavar='dir',
                      help='locale directories that allow comman separated '
                           'string. This option override locale_dir in '
                           'conf.py setting if provided. default is empty '
                           'list.')
    parser.add_option('--transifex-username', dest='transifex_username',
                      type='string', action='store', default=None,
                      metavar='username',
                      help='Your transifex username. default is None.')
    parser.add_option('--transifex-password', dest='transifex_password',
                      type='string', action='store', default=None,
                      metavar='password',
                      help='Your transifex password. default is None.')
    parser.add_option('--transifex-project-name',
                      dest='transifex_project_name',
                      type='string', action='store', default=None,
                      metavar='project-name',
                      help='Your transifex project name. default is None')
    options, args = parser.parse_args(argv)

    if len(args) != 1 or args[0] not in commands:
        parser.print_help()
        sys.exit(-1)

    environ = dict(os.environ)
    for key in [k for k in environ if k.startswith(ENVKEY_PREFIX)]:
        value = environ[key]
        optname = key[len(ENVKEY_PREFIX):].lower().replace('-', '_')
        if hasattr(options, optname):
            if not getattr(options, optname):
                if optname in ('locale_dir', 'language'):
                    setattr(options, optname, value.split(','))
                else:
                    setattr(options, optname, value)

    if not options.locale_dir:
        config = read_config(options.config)
        if 'locale_dirs' not in config:
            msg = "locale_dirs was not defined: %s" % options.config
            raise RuntimeError(msg)

        options.locale_dir = config['locale_dirs'][0]

    return options, args


def run(argv):
    options, args = parse_option(argv)
    cmd = args[0]

    if cmd in commands:
        func, desc = commands[cmd]
        kwargs = func.options.copy()
        for k, v in kwargs.items():
            if v is required and not getattr(options, k):
                msg = "'--%s' option is required." % k.replace('_', '-')
                raise RuntimeError(msg)
            kwargs[k] = getattr(options, k, v)
        func(**kwargs)
    else:
        msg = 'unknown command: %s' % cmd
        raise RuntimeError(msg)


def main():
    try:
        run(sys.argv[1:])
    except RuntimeError:
        typ, err, tb = sys.exc_info()
        print_("ERROR:", err, file=sys.stderr)


if __name__ == '__main__':
    main()
