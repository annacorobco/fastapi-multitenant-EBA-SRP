#!/bin/sh

HOST=$(echo "$1" | cut -d: -f1)
PORT=$(echo "$1" | cut -d: -f2)
TIMEOUT=${2:-15}

echo "Waiting for $HOST:$PORT for up to $TIMEOUT seconds..."

for i in $(seq 1 $TIMEOUT); do
    nc -z "$HOST" "$PORT" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$HOST:$PORT is available!"
        exit 0
    fi
    sleep 1
done

echo "Timeout after $TIMEOUT seconds waiting for $HOST:$PORT"
exit 1
