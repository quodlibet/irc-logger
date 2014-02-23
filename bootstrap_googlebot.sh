#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
GOOGLEBOT="$DIR/googlebot"

if [ -d "$GOOGLEBOT" ]; then
  echo "ERROR: $GOOGLEBOT exists"
  exit 1
fi

git clone https://github.com/jmhobbs/googlecode-irc-bot.git "$GOOGLEBOT"
"$DIR/config.py" "$DIR/misc/googlebot.yaml.tmpl" > "$GOOGLEBOT/bots/bot.yaml"
