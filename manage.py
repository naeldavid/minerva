#!/usr/bin/env python3

"""
Simple management script for Raspberry Pi Server Dashboard
"""

import argparse
import subprocess
import sys
import os

def run_command(cmd, error_msg):
    """Run a command and handle errors"""
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{error_msg}: {e}")
        return False
    except FileNotFoundError:
        print(f"Command not found: {cmd[0]}")
        return False

def start_service():
    """Start the dashboard service"""
    if run_command(['sudo', 'systemctl', 'start', 'rpi-dashboard.service'], 
                   "Failed to start dashboard service"):
        print("Dashboard service started")

def stop_service():
    """Stop the dashboard service"""
    if run_command(['sudo', 'systemctl', 'stop', 'rpi-dashboard.service'],
                   "Failed to stop dashboard service"):
        print("Dashboard service stopped")

def restart_service():
    """Restart the dashboard service"""
    if run_command(['sudo', 'systemctl', 'restart', 'rpi-dashboard.service'],
                   "Failed to restart dashboard service"):
        print("Dashboard service restarted")

def status_service():
    """Check the status of the dashboard service"""
    run_command(['sudo', 'systemctl', 'status', 'rpi-dashboard.service'],
                "Failed to get service status")

def setup_service():
    """Setup the systemd service"""
    service_file = 'services/rpi-dashboard.service'
    if not os.path.exists(service_file):
        print(f"Error: Service file not found: {service_file}")
        return
    
    # Copy service file
    if not run_command(['sudo', 'cp', service_file, '/etc/systemd/system/'],
                       "Failed to copy service file"):
        return
    
    # Reload systemd
    if not run_command(['sudo', 'systemctl', 'daemon-reload'],
                       "Failed to reload systemd"):
        return
    
    # Enable service
    if run_command(['sudo', 'systemctl', 'enable', 'rpi-dashboard.service'],
                   "Failed to enable service"):
        print("Dashboard service setup complete")
        print("Start the service with: sudo systemctl start rpi-dashboard.service")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Manage Raspberry Pi Server Dashboard")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add subcommands
    subparsers.add_parser('start', help='Start the dashboard service')
    subparsers.add_parser('stop', help='Stop the dashboard service')
    subparsers.add_parser('restart', help='Restart the dashboard service')
    subparsers.add_parser('status', help='Check the status of the dashboard service')
    subparsers.add_parser('setup', help='Setup the systemd service')
    
    args = parser.parse_args()
    
    commands = {
        'start': start_service,
        'stop': stop_service,
        'restart': restart_service,
        'status': status_service,
        'setup': setup_service
    }
    
    if args.command in commands:
        commands[args.command]()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()