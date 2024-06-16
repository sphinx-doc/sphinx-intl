# setup

sudo pip install -U pip setuptools wheel setuptools_scm
sudo pip install -r requirements-dev.txt

# Install Transifex CLI tool
# refer to Installation instructions https://github.com/transifex/cli#installation

(cd `mktemp -d` && curl -o- https://raw.githubusercontent.com/transifex/cli/master/install.sh | bash && sudo mv ./tx /usr/local/bin )
