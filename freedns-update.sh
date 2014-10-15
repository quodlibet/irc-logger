#!/bin/sh

DIR="$( cd "$( dirname "$0" )" && pwd )"
TOKEN=$("$DIR/config.py" FREEDNS_TOKEN)
IP=$(ip -6 addr show dev wlan0 | sed -e's/^.*inet6 \([^ ]*\)\/.*$/\1/;t;d' | head -n1)

while true; do
    echo url="https://freedns.afraid.org/dynamic/update.php?$TOKEN&address=$IP" | curl --config -
    sleep 300
done
