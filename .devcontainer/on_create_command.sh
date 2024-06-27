#!/bin/sh
# setup

set -ex

pip install -U pip setuptools wheel setuptools_scm
pip install -r requirements-dev.txt

# Install Transifex CLI tool into /usr/local/bin
# refer to Installation instructions https://github.com/transifex/cli#installation

(cd /usr/local/bin && curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | sudo bash)
