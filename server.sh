#!/bin/bash

while true; do
    PID=$(pgrep -f "python app.py")

    if [ -n "$PID" ]; then
        echo "Stopping Python app with PID: $PID"
        kill -TERM $PID
        sleep 6
    fi

    echo "Restarting Python app"
    python app.py &

    sleep 600
done
