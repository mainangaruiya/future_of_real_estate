#!/bin/bash

while true; do
    # Get the process ID (PID) of the running Python app
    PID=$(pgrep -f "python app.py")

    if [ -n "$PID" ]; then
        echo "Stopping Python app with PID: $PID"
        # Stop the Python app gracefully (e.g., send a termination signal)
        kill -TERM $PID
        sleep 6 # Wait for the process to stop gracefully
    fi

    # Restart the Python app
    echo "Restarting Python app"
    python app.py &

    # Sleep for 10 minutes before the next iteration
    sleep 600
done
