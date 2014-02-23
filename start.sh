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
    kill $(cat "$DUCKDNSPID")
    rm "$DUCKDNSPID"
fi
./duckdns.sh >/dev/null 2>&1 &
echo $! > "$DUCKDNSPID"

# google bot
GOOGLEBOT="$DIR/googlebot/googlecode-irc-bot.py"
GOOGLEPID="$DIR/.google.pid"
if [ -f "$GOOGLEPID" ]; then
    pkill -P $(cat "$GOOGLEPID")
    rm "$GOOGLEPID"
fi
python "$GOOGLEBOT" >/dev/null 2>&1 &
echo $! > "$GOOGLEPID"

# web server

WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    rm "$WEBPID"
fi
./start_web.sh >/dev/null 2>&1 &
echo $! > "$WEBPID"
