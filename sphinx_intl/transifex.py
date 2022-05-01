# -*- coding: utf-8 -*-

import os
import re
import subprocess
import textwrap
from pathlib import Path
from shutil import which

import click
from sphinx.util.osutil import cd

from .pycompat import relpath
from .catalog import load_po


# ==================================
# settings

MINIMUM_VERSION = (1, 1, 0)

# To avoid using invalid resource name, append underscore to such names.
# As a limitation, append `_` doesn't care about collision to other resources.
# e.g. 'glossary' and 'glossary_' are pushed as a 'glossary_'. The following
# resource names are reserved slugs, Transifex will reply with an error on these
# resource names.
IGNORED_RESOURCE_NAMES = (
    'glossary',
    'settings',
)

TRANSIFEXRC_TEMPLATE = """\
[https://www.transifex.com]
rest_hostname = https://www.transifex.com
token = %(transifex_token)s
"""

TXCONFIG_TEMPLATE = """\
[main]
host = https://www.transifex.com
"""


# ==================================
# utility functions

def normalize_resource_name(name):
    # replace path separator with '--'
    name = re.sub(r'[\\/]', '--', name)

    # replace unusable characters (not: -, _ ascii, digit) with '_'
    name = re.sub(r'[^\-\w]', '_', name)

    # append `_` for ignored resource names
    while name in IGNORED_RESOURCE_NAMES:
        name += '_'

    return name

def check_transifex_cli_installed():
    if not which("tx"):
        msg = textwrap.dedent("""\
            Could not run "tx".
            You need to install the Transifex CLI external library.
            Please install the below command and restart your terminal if you want to use this action:

                $ curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash

            """)
        raise click.BadParameter(msg)

    version_msg = subprocess.check_output("tx --version", shell=True)
    version = tuple(int(x) for x in version_msg.split("=")[-1].strip().split("."))

    if not version_msg.startswith("TX Client"):
        msg = textwrap.dedent("""\
            The old transifex_client library was found.
            You need to install the Transifex CLI external library.
            Please install the below command and restart your terminal if you want to use this action:

                $ curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash

            """)
        raise click.BadParameter(msg)

    if not version >= MINIMUM_VERSION:
        msg = textwrap.dedent(f"""\
        An unsupported version of the Transifex CLI was found.
        Version {MINIMUM_VERSION} or greater is required.
        Please run the below command if you want to use this action:

            $ tx update

        """)
        raise click.BadParameter(msg)      

 
def get_tx_root():
    check_transifex_cli_installed()
    curr_dir = Path.cwd().resolve()

    while True:
        tx_root = curr_dir / ".tx"
        if tx_root.is_dir():
            return str(tx_root)

        if curr_dir == curr_dir.root:
            msg = "'.tx/config' not found. You need 'create-txconfig' first."
            raise click.BadParameter(msg)           

        curr_dir = curr_dir.parent


# ==================================
# commands

def create_transifexrc(transifex_token):
    """
    Create `$HOME/.transifexrc`
    """
    target = os.path.normpath(os.path.expanduser('~/.transifexrc'))

    if os.path.exists(target):
        click.echo('{0} already exists, skipped.'.format(target))
        return

    if not transifex_token:
        msg = textwrap.dedent("""\
        You need a transifex token by command option or environment.
        command option: --transifex-token
        """)
        raise click.BadParameter(msg, param_hint='transifex_token')

    with open(target, 'wt') as rc:
        rc.write(TRANSIFEXRC_TEMPLATE % locals())
    click.echo('Create: {0}'.format(target))


def create_txconfig():
    """
    Create `./.tx/config`
    """
    target = os.path.normpath('.tx/config')
    if os.path.exists(target):
        click.echo('{0} already exists, skipped.'.format(target))
        return

    if not os.path.exists('.tx'):
        os.mkdir('.tx')

    with open(target, 'wt') as f:
        f.write(TXCONFIG_TEMPLATE)

    click.echo('Create: {0}'.format(target))


def update_txconfig_resources(transifex_organization_name, transifex_project_name, locale_dir, pot_dir):
    """
    Update resource sections of `./.tx/config`.
    """
    check_transifex_cli_installed()

    tx_root = get_tx_root()

    cmd_tmpl = (
        'tx',
        'add',
        '--organization', '%(transifex_organization_name)s',
        '--project', '%(transifex_project_name)s',
        '--resource', '%(resource_path)s',
        '--file-filter', '%(locale_dir)s/<lang>/LC_MESSAGES/%(resource_path)s.po',
        '--type', 'PO',
        '%(pot_dir)s/%(resource_path)s.pot',
    )

    pot_dir = Path(pot_dir)
    for pot_path in sorted(pot_dir.glob('**/*.pot')):
        resource_path = normalize_resource_name(str(pot_path.relative_to(pot_dir)))
        pot = load_po(str(pot_path))
        if len(pot):
            lv = locals()
            cmd = [arg % lv for arg in cmd_tmpl]
            subprocess.run(cmd, shell=True)
        else:
            click.echo('{0} is empty, skipped'.format(pot_path))

