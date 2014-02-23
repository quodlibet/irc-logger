#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
GOOGLEBOT="$DIR/googlebot"

if [ -d "$GOOGLEBOT" ]; then
  echo "ERROR: $GOOGLEBOT exists"
  exit 1
fi

sudo apt-get install python-gdata python-feedparser python-yaml python-twisted

git clone https://github.com/jmhobbs/googlecode-irc-bot.git "$GOOGLEBOT"
patch -p1 -d "$GOOGLEBOT" < "$DIR/misc/googlebot.diff"
"$DIR/config.py" "$DIR/misc/googlebot.yaml.tmpl" > "$GOOGLEBOT/bots/bot.yaml"
