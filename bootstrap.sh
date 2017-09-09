#!/bin/bash

sudo apt update

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

# web deps
sudo apt install python-twisted python-flask python3-twisted python3-flask \
    irclog2html python3-requests python-requests

sudo apt install git

rm -Rf msys2_web
git clone https://github.com/lazka/msys2-web.git msys2_web
