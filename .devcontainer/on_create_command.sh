#!/bin/sh
# setup

set -ex

curl -LsSf https://astral.sh/uv/install.sh | sh
. $HOME/.cargo/env
uv tool install -U ruff
uv tool install -U tox --with tox-uv

# Install Transifex CLI tool into /usr/local/bin
# refer to Installation instructions https://github.com/transifex/cli#installation

(cd /usr/local/bin && curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | sudo bash)
