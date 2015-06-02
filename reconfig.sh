#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

BUILDBOT="$DIR/buildbot"
MASTER="$BUILDBOT/master"
"$DIR/config.py" "$DIR/buildbot.cfg.tmpl" > "$MASTER/master.cfg"

echo "done."
echo "Call start.sh to restart all services."
