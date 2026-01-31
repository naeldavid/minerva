#!/bin/bash

# Lightweight Raspberry Pi Zero Installation Script

echo "Installing Raspberry Pi Dashboard..."

# Install Python dependencies only
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Setup systemd service
echo "Setting up systemd service..."
sudo cp services/rpi-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rpi-dashboard.service

echo "Installation complete!"
echo "Configure settings in config/settings.env"
echo "Start with: sudo systemctl start rpi-dashboard.service"
echo "Access at http://<your-pi-ip>:5000"