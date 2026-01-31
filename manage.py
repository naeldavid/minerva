#!/usr/bin/env python3

"""
Simple management script for Raspberry Pi Server Dashboard
"""

import argparse
import subprocess
import sys
import os

def start_service():
    """Start the dashboard service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'start', 'rpi-dashboard.service'], check=True)
        print("Dashboard service started")
    except subprocess.CalledProcessError:
        print("Failed to start dashboard service")

def stop_service():
    """Stop the dashboard service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'stop', 'rpi-dashboard.service'], check=True)
        print("Dashboard service stopped")
    except subprocess.CalledProcessError:
        print("Failed to stop dashboard service")

def restart_service():
    """Restart the dashboard service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'restart', 'rpi-dashboard.service'], check=True)
        print("Dashboard service restarted")
    except subprocess.CalledProcessError:
        print("Failed to restart dashboard service")

def status_service():
    """Check the status of the dashboard service"""
    try:
        subprocess.run(['sudo', 'systemctl', 'status', 'rpi-dashboard.service'], check=True)
    except subprocess.CalledProcessError:
        print("Failed to get service status")

def setup_service():
    """Setup the systemd service"""
    try:
        # Copy service file
        subprocess.run(['sudo', 'cp', 'services/rpi-dashboard.service', '/etc/systemd/system/'], check=True)
        
        # Reload systemd
        subprocess.run(['sudo', 'systemctl', 'daemon-reload'], check=True)
        
        # Enable service
        subprocess.run(['sudo', 'systemctl', 'enable', 'rpi-dashboard.service'], check=True)
        
        print("Dashboard service setup complete")
        print("Start the service with: sudo systemctl start rpi-dashboard.service")
    except subprocess.CalledProcessError as e:
        print(f"Failed to setup service: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Manage Raspberry Pi Server Dashboard")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    subparsers.add_parser('start', help='Start the dashboard service')
    
    # Stop command
    subparsers.add_parser('stop', help='Stop the dashboard service')
    
    # Restart command
    subparsers.add_parser('restart', help='Restart the dashboard service')
    
    # Status command
    subparsers.add_parser('status', help='Check the status of the dashboard service')
    
    # Setup command
    subparsers.add_parser('setup', help='Setup the systemd service')
    
    args = parser.parse_args()
    
    if args.command == 'start':
        start_service()
    elif args.command == 'stop':
        stop_service()
    elif args.command == 'restart':
        restart_service()
    elif args.command == 'status':
        status_service()
    elif args.command == 'setup':
        setup_service()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()