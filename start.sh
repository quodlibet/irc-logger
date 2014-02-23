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

# web server

WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    rm "$WEBPID"
fi
./start_web.sh >/dev/null 2>&1 &
echo $! > "$WEBPID"
