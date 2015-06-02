#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
GOOGLEBOT="$DIR/googlebot"

sudo apt-get install  python-feedparser python-yaml python-twisted

"$DIR/config.py" "$DIR/misc/googlebot.yaml.tmpl" > "$GOOGLEBOT/bot.yaml"
