#!/bin/bash

# Lightweight Raspberry Pi Zero Startup Script

# Set working directory
cd /home/pi/rpi_server/server

# Load environment variables
if [ -f ../config/settings.env ]; then
    export $(cat ../config/settings.env | xargs)
fi

# Function to check if a process is running
is_running() {
    pgrep -f "$1" > /dev/null
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

# Function to start the mining service
start_mining() {
    echo "Starting mining service..."
    if is_running "xmrig"; then
        echo "Mining already running"
    else
        # Start xmrig with conservative settings for Pi Zero
        nohup xmrig --config=/home/pi/xmrig/config.json > /dev/null 2>&1 &
        echo "Mining started"
    fi
}

# Start services
start_server
start_mining

echo "Services started"

exit 0