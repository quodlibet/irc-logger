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

# irc bot

IRCBOT="$DIR/ircbot.py"
IRCPID="$DIR/.ircbot.pid"
if [ -f "$IRCPID" ]; then
    pkill -P $(cat "$IRCPID")
    kill $(cat "$IRCPID")
    rm "$IRCPID"
fi
python "$IRCBOT" "$DIR/_irc-logs" >/dev/null 2>&1 &
echo $! > "$IRCPID"

# web server

WEBAPP="$DIR/web/index.py"
WEBPID="$DIR/.web.pid"
if [ -f "$WEBPID" ]; then
    pkill -P $(cat "$WEBPID")
    kill $(cat "$WEBPID")
    rm "$WEBPID"
fi
authbind python "$WEBAPP" >/dev/null 2>&1 &
echo $! > "$WEBPID"
