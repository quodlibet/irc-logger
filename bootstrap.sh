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
sudo apt install python-twisted python-flask python3-twisted python3-flask
