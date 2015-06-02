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
    pkill -P $(cat "$DUCKDNSPID")
    kill $(cat "$DUCKDNSPID")
    echo "sent SIGTERM to duckdns process"
    rm "$DUCKDNSPID"
else
    echo "duckdns updater not running"
fi

# google bot

IRCPID="$DIR/.ircbot.pid"
if [ -f "$IRCPID" ]; then
    pkill -P $(cat "$IRCPID")
    kill $(cat "$IRCPID")
    echo "sent SIGTERM to irc process"
    rm "$IRCPID"
else
    echo "irc logger not running"
fi

# web server

WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    kill $(cat "$WEBPID")
    echo "sent SIGTERM to web process"
    rm "$WEBPID"
else
    echo "web process not running"
fi
