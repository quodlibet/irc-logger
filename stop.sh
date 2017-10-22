#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

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
