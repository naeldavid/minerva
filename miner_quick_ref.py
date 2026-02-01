#!/usr/bin/env python3
"""
Quick Reference: Cpuminer-ulti Configuration for Minerva

Guide for setting up and configuring cpuminer-ulti with Minerva dashboard.
"""

print("""
╔════════════════════════════════════════════════════════════════════════╗
║      Cpuminer-ulti Configuration - Quick Reference                     ║
╚════════════════════════════════════════════════════════════════════════╝

ABOUT CPUMINER-ULTI:

cpuminer-ulti is an optimized CPU miner for Monero (XMR) that:
  ✓ Works well on Raspberry Pi (including Pi Zero)
  ✓ Provides JSON API for stats collection
  ✓ Supports GPU acceleration (if available)
  ✓ Lightweight and resource-efficient

QUICK START:

1. Start cpuminer-ulti with API enabled:
   
   Basic (localhost only):
   $ cpuminer-ulti --cpu-threads=1 --api-bind=127.0.0.1:4048

   With pool configuration:
   $ cpuminer-ulti --cpu-threads=1 \\
     -o stratum+tcp://pool.moneroocean.stream:10128 \\
     -u YOUR_MONERO_ADDRESS \\
     --api-bind=127.0.0.1:4048

2. Configure Minerva dashboard:
   
   $ nano config/settings.env
   # Verify: MINER_API_URL=http://localhost:4048/api/get_stats
   #         MINER_TYPE=cpuminer-ulti

3. Test API compatibility:
   
   $ python3 test_miner_compatibility.py
   ✓ Format parsing: PASS
   ✓ Live API connection: Will test once miner starts

4. Start Minerva dashboard:
   
   $ python3 app.py
   # Access at http://localhost:5000
   # Check Mining Stats widget for live data

COMMAND-LINE OPTIONS:

Essential Options:
  --cpu-threads=N     Number of CPU threads to use (1-32)
  --api-bind=HOST:PORT Enable API on specified address:port
  -o POOL_URL         Mining pool URL (stratum+tcp://...)
  -u ADDRESS          Your Monero wallet address

Optimization Options:
  --idle-priority     Lower CPU priority to reduce system impact
  --url-only          Only use URL from config, ignore other options

Example for Pi Zero (minimal):
$ cpuminer-ulti --cpu-threads=1 --idle-priority --api-bind=127.0.0.1:4048

Example with multiple threads:
$ cpuminer-ulti --cpu-threads=2 --api-bind=127.0.0.1:4048

MONITORING THE MINER:

Via Minerva Dashboard:
  - Open http://localhost:5000
  - Check "Mining Statistics" widget
  - View: hashrate, shares, uptime, estimated daily yield

Via API directly:
  $ curl http://localhost:4048/api/get_stats | jq

Typical API Response:
{
  "hashrate": 2500.5,
  "shares_valid": 42,
  "shares_rejected": 2,
  "uptime": 3600,
  "pool": "pool.moneroocean.stream:10128",
  "threads": 1
}

PERFORMANCE NOTES:

Pi Zero Recommendations:
  - Use --cpu-threads=1 (single core)
  - Use --idle-priority to not block system
  - Monitor CPU temperature with monitor_mining.py
  - Expected: 600-1200 H/s depending on Pi model

Better Performance:
  - Use Pi 4 or 5: --cpu-threads=2 to --cpu-threads=4
  - Add GPU miners if available
  - Pool mining is more consistent than solo mining

TROUBLESHOOTING:

No API response?
  $ netstat -tlnp | grep 4048
  Make sure --api-bind=127.0.0.1:4048 is in command

Connection refused?
  $ ps aux | grep cpuminer
  Check if cpuminer-ulti is actually running

Low hashrate?
  - Check CPU threads are being used: watch -n1 'grep MHz /proc/cpuinfo'
  - Try without --idle-priority for maximum performance
  - Check system doesn't have other heavy processes

UPDATES:

Check for new cpuminer-ulti versions:
  $ cpuminer-ulti --version

Download latest:
  https://github.com/fireice-uk/cpuminer-opt (cpuminer-opt)
  https://github.com/SChernykh/cpuminer-ulti (cpuminer-ulti)

""")
