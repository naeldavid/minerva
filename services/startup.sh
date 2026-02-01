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
    if is_running "cpuminer-ulti"; then
        echo "Mining already running"
    else
        # Start cpuminer-ulti with conservative settings for Pi Zero
        # Enable API on localhost:4048 for stats collection
        nohup cpuminer-ulti --cpu-threads=1 --api-bind=127.0.0.1:4048 > /dev/null 2>&1 &
        echo "Mining started"
    fi
}

# Start services
start_server
start_mining

echo "Services started"

exit 0