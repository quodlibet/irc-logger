#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

# buildbot

BUILDBOT="$DIR/buildbot"
MASTER="$BUILDBOT/master"
SLAVE="$BUILDBOT/slave"
buildbot restart "$MASTER"
buildslave restart "$SLAVE"

# duckdns updater

DUCKDNSPID="$DIR/.duckdns.pid"
if [ -f "$DUCKDNSPID" ]; then
    pkill -P $(cat "$DUCKDNSPID")
    kill $(cat "$DUCKDNSPID")
    rm "$DUCKDNSPID"
fi
./duckdns_update.sh >/dev/null 2>&1 &
echo $! > "$DUCKDNSPID"

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
