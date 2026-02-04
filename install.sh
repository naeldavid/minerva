#!/bin/bash
set -e

echo "Installing Raspberry Pi Dashboard..."

# Install Python dependencies
echo "Installing Python dependencies..."
if ! pip3 install -r requirements.txt; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

# Setup systemd service
echo "Setting up systemd service..."
if ! sudo cp services/rpi-dashboard.service /etc/systemd/system/; then
    echo "Error: Failed to copy service file"
    exit 1
fi

if ! sudo systemctl daemon-reload; then
    echo "Error: Failed to reload systemd"
    exit 1
fi

if ! sudo systemctl enable rpi-dashboard.service; then
    echo "Error: Failed to enable service"
    exit 1
fi

echo "Installation complete!"
echo "Configure settings in config/settings.env"
echo "Start with: sudo systemctl start rpi-dashboard.service"
echo "Access at http://localhost:5000"