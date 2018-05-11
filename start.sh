#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"

# duckdns updater

DUCKDNSPID="$DIR/.duckdns.pid"
if [ -f "$DUCKDNSPID" ]; then
    pkill -P $(cat "$DUCKDNSPID")
    kill $(cat "$DUCKDNSPID")
    rm "$DUCKDNSPID"
fi
./duckdns-update.sh >/dev/null 2>&1 &
echo $! > "$DUCKDNSPID"

# web server

WEBAPP="$DIR/run.py"
WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    kill $(cat "$WEBPID")
    rm "$WEBPID"
fi
authbind python3 "$WEBAPP" 80 443 --irc >/dev/null 2>&1 &
echo $! > "$WEBPID"
