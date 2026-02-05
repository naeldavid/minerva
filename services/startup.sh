#!/bin/bash
set -e

# Determine the minerva directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd .. && pwd)"

# Set working directory
cd "$SCRIPT_DIR" || exit 1

# Load environment variables safely
if [ -f config/settings.env ]; then
    set -a
    # shellcheck source=/dev/null
    . config/settings.env
    set +a
fi

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null 2>&1
    return $?
}

# Function to start the Flask server
start_server() {
    echo "Starting dashboard server..."
    if is_running "app.py"; then
        echo "Server already running"
    else
        nohup python3 app.py > /dev/null 2>&1 &
        echo "Server started"
    fi
}

# Start services
start_server

echo "Services started"
exit 0