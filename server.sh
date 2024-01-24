#!/bin/bash

while true; do
    PID=$(pgrep -f "python app.py")

    if [ -n "$PID" ]; then
        echo "Stopping Python app with PID: $PID"
        kill -TERM $PID
        sleep 1
    fi

    echo "Restarting Python app"
    python app.py &

    #sleep 5

done
