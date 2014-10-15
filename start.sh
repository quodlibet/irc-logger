#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

# buildbot

BUILDBOT="$DIR/buildbot"
MASTER="$BUILDBOT/master"
SLAVE="$BUILDBOT/slave"
buildbot restart "$MASTER"
buildslave restart "$SLAVE"

# freedns updater

FREEDNSPID="$DIR/.freedns.pid"
if [ -f "$FREEDNSPID" ]; then
    pkill -P $(cat "$FREEDNSPID")
    kill $(cat "$FREEDNSPID")
    rm "$FREEDNSPID"
fi
./freedns-update.sh >/dev/null 2>&1 &
echo $! > "$FREEDNSPID"

# google bot

GOOGLEBOT="$DIR/googlebot/googlecode-irc-bot.py"
GOOGLEPID="$DIR/.google.pid"
if [ -f "$GOOGLEPID" ]; then
    pkill -P $(cat "$GOOGLEPID")
    kill $(cat "$GOOGLEPID")
    rm "$GOOGLEPID"
fi
python "$GOOGLEBOT" >/dev/null 2>&1 &
echo $! > "$GOOGLEPID"

# pypy bot

PYPYBOT="$DIR/pypybot/googlecode-irc-bot.py"
PYPYPID="$DIR/.pypy.pid"
if [ -f "$PYPYPID" ]; then
    pkill -P $(cat "$PYPYPID")
    kill $(cat "$PYPYPID")
    rm "$PYPYPID"
fi
python "$PYPYBOT" >/dev/null 2>&1 &
echo $! > "$PYPYPID"

# gtk bot

GTKBOT="$DIR/gtkbot/googlecode-irc-bot.py"
GTKPID="$DIR/.gtk.pid"
if [ -f "$GTKPID" ]; then
    pkill -P $(cat "$GTKPID")
    kill $(cat "$GTKPID")
    rm "$GTKPID"
fi
python "$GTKBOT" >/dev/null 2>&1 &
echo $! > "$GTKPID"

# web server

WEBAPP="$DIR/web/index.py"
WEBVENV="$DIR/web/venv"
WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    kill $(cat "$WEBPID")
    rm "$WEBPID"
fi
source "$WEBVENV/bin/activate"
authbind python "$WEBAPP" >/dev/null 2>&1 &
echo $! > "$WEBPID"
deactivate
