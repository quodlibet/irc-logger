#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
APP="$DIR/web/index.py"
VENV="$DIR/web/venv"

source "$VENV/bin/activate"
authbind python "$APP"
