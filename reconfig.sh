#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

# buildbot

BUILDBOT="$DIR/buildbot"
MASTER="$BUILDBOT/master"
"$DIR/config.py" "$DIR/misc/buildbot.cfg.tmpl" > "$MASTER/master.cfg"

# google bot

GOOGLEBOT="$DIR/googlebot"
"$DIR/config.py" "$DIR/misc/googlebot.yaml.tmpl" > "$GOOGLEBOT/bot.yaml"

echo "done."
echo "Call start.sh to restart all services."
