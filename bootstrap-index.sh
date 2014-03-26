#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
VENV="$DIR/web/venv"

if [ -d "$VENV" ]; then
  echo "ERROR: $VENV exists"
  exit 1
fi

sudo apt-get install python-virtualenv

virtualenv "$VENV"
source "$VENV/bin/activate"
pip install irclog2html
pip install flask
pip install tornado

# allow us to bind to port 80
sudo apt-get install authbind
sudo touch /etc/authbind/byport/80
sudo chown "$USER" /etc/authbind/byport/80
sudo chmod 755 /etc/authbind/byport/80
