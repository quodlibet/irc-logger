#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
VENV="$DIR/web/venv"

if [ -d "$VENV" ]; then
  echo "ERROR: $VENV exists"
  exit 1
fi

sudo apt update

sudo apt install python-dev python-virtualenv python-twisted python-flask python-tornado

virtualenv --system-site-packages "$VENV"
source "$VENV/bin/activate"
pip install irclog2html

# firewall
sudo apt install ufw
sudo ufw reset --force
sudo ufw allow from 192.168.0.0/24 to any port 22
sudo ufw allow 80/tcp
sudo ufw enable

# allow us to bind to port 80
sudo apt install authbind
sudo touch /etc/authbind/byport/80
sudo chown "$USER" /etc/authbind/byport/80
sudo chmod 755 /etc/authbind/byport/80
