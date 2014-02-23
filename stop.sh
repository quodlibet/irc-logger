#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

# buildbot

BUILDBOT="$DIR/buildbot"
MASTER="$BUILDBOT/master"
SLAVE="$BUILDBOT/slave"

buildslave stop "$SLAVE"
buildbot stop "$MASTER"

# duckdns updater

DUCKDNSPID="$DIR/.duckdns.pid"
if [ -f "$DUCKDNSPID" ]; then
    kill $(cat "$DUCKDNSPID")
    echo "sent SIGTERM to duckdns process"
    rm "$DUCKDNSPID"
else
    echo "duckdns updater not running"
fi

# google bot

GOOGLEPID="$DIR/.google.pid"
if [ -f "$GOOGLEPID" ]; then
    pkill -P $(cat "$GOOGLEPID")
    echo "sent SIGTERM to googlebot process"
    rm "$GOOGLEPID"
else
    echo "google bot not running"
fi

# web server

WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    echo "sent SIGTERM to web process"
    rm "$WEBPID"
else
    echo "web process not running"
fi
