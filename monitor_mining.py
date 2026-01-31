#!/usr/bin/env python3

"""
Lightweight mining process monitor for Raspberry Pi Zero
"""

import time
import psutil
import subprocess
import os
import signal
import sys

class LightweightMiningMonitor:
    def __init__(self, process_name="xmrig", cpu_threshold=50.0):
        self.process_name = process_name
        self.cpu_threshold = cpu_threshold
        self.mining_process = None
        self.is_mining_paused = False
        
    def find_mining_process(self):
        """Find the mining process by name"""
        for proc in psutil.process_iter(['pid', 'name']):
            if self.process_name.lower() in proc.info['name'].lower():
                return proc
        return None
    
    def get_system_cpu_usage(self):
        """Get overall system CPU usage"""
        return psutil.cpu_percent(interval=0.5)
    
    def pause_mining(self):
        """Pause mining by sending SIGSTOP to the process"""
        if self.mining_process:
            try:
                self.mining_process.send_signal(signal.SIGSTOP)
                self.is_mining_paused = True
                print(f"Paused mining process (PID: {self.mining_process.pid})")
                return True
            except Exception as e:
                print(f"Failed to pause mining: {e}")
                return False
        return False
    
    def resume_mining(self):
        """Resume mining by sending SIGCONT to the process"""
        if self.mining_process:
            try:
                self.mining_process.send_signal(signal.SIGCONT)
                self.is_mining_paused = False
                print(f"Resumed mining process (PID: {self.mining_process.pid})")
                return True
            except Exception as e:
                print(f"Failed to resume mining: {e}")
                return False
        return False
    
    def monitor(self):
        """Main monitoring loop - optimized for Raspberry Pi Zero"""
        print(f"Starting mining monitor for '{self.process_name}'")
        print(f"CPU threshold: {self.cpu_threshold}%")
        print("Press Ctrl+C to stop monitoring")
        
        check_count = 0
        
        while True:
            try:
                # Find mining process if not already found
                if not self.mining_process:
                    self.mining_process = self.find_mining_process()
                    if self.mining_process:
                        print(f"Found mining process: {self.mining_process.info['name']} (PID: {self.mining_process.pid})")
                    else:
                        # Check less frequently if process not found
                        time.sleep(10)
                        continue
                
                # Get system CPU usage
                cpu_usage = self.get_system_cpu_usage()
                
                # Check if we need to pause/resume mining
                if cpu_usage > self.cpu_threshold and not self.is_mining_paused:
                    print(f"High CPU usage: {cpu_usage:.1f}%, pausing mining")
                    self.pause_mining()
                elif cpu_usage <= self.cpu_threshold and self.is_mining_paused:
                    print(f"CPU usage normalized: {cpu_usage:.1f}%, resuming mining")
                    self.resume_mining()
                
                # Log status every 30 checks (about every 15 seconds)
                check_count += 1
                if check_count % 30 == 0:
                    print(f"Status - CPU: {cpu_usage:.1f}%, Mining paused: {self.is_mining_paused}")
                
                # Short sleep to keep monitoring responsive
                time.sleep(0.5)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                print(f"Error in monitoring: {e}")
                time.sleep(5)  # Wait before retrying

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Lightweight Mining Process Monitor")
    parser.add_argument("--process", default="xmrig", help="Process name to monitor")
    parser.add_argument("--threshold", type=float, default=50.0, help="CPU threshold percentage")
    
    args = parser.parse_args()
    
    monitor = LightweightMiningMonitor(process_name=args.process, cpu_threshold=args.threshold)
    monitor.monitor()

if __name__ == "__main__":
    main()