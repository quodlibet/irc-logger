#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
WEBAPP="$DIR/run.py"
authbind python3 "$WEBAPP" 80 443 --irc
