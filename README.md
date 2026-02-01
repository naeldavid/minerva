# Minerva

**Minerva** (Miner + EVA) is a lightweight web-based control panel for Raspberry Pi Zero that combines cryptocurrency mining management with an integrated AI assistant. It provides:
- AI study assistant (EVA) via external free AI API
- Real-time system performance monitoring
- Live crypto mining statistics with cpuminer-ulti integration
- Continuous operation with minimal resource usage on low-power devices

## Features

### Study Assistant
- Web-based chat interface with AI
- Structured response formatting (headings, bullet points, code blocks)
- Multi-message history support

### System Monitoring
- CPU usage percentage
- RAM usage percentage
- CPU temperature
- System uptime
- Network status

### Mining Statistics
- Total XMR mined
- Current hashrate
- Miner uptime
- Estimated daily yield

## Project Structure

```
minerva/
├── app.py                          # Main Flask application
├── manage.py                       # Service management script
├── monitor_mining.py               # Mining monitoring with CPU throttling
├── verify_optimization.py          # Performance verification utility
├── test_miner_compatibility.py     # Miner API compatibility tester
├── miner_quick_ref.py              # Cpuminer-ulti configuration reference
├── DEPLOYMENT_CHECKLIST.py         # Deployment verification checklist
├── requirements.txt                # Python dependencies (Flask, psutil, requests, python-dotenv)
├── LICENSE                         # Project license
├── install.sh                      # Installation script
├── README.md                       # This file
├── api/
│   ├── ai_client.py                # AI API client for EVA assistant
│   ├── system_stats.py             # System statistics collection
│   └── miner_stats.py              # Mining statistics collection
├── config/
│   └── settings.env                # Environment configuration file
├── docs/
│   ├── api.md                      # API documentation
│   ├── deployment.md               # Deployment guide
│   └── modules.md                  # Module documentation
├── templates/
│   └── dashboard.html              # Main dashboard template
├── static/
│   ├── style.css                   # Dashboard styling
│   └── app.js                      # Frontend JavaScript
└── services/
    ├── rpi-dashboard.service       # systemd service file
    └── startup.sh                  # Service startup script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd minerva
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

   Or manually install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
# Edit config/settings.env with your API keys and settings
nano config/settings.env
```

4. Start the server:

   **Development mode:**
```bash
python app.py
```

   **Production with systemd:**
```bash
sudo ./manage.py setup
sudo systemctl start rpi-dashboard.service
```

## Configuration

Edit `config/settings.env` to configure:

- **Flask settings** - Port, debug mode, host
- **AI API settings** - API URL, authentication key, model configuration
- **Miner API settings** - cpuminer-ulti API endpoint configuration
- **Logging preferences** - Log level and output configuration
- **Mining thresholds** - CPU usage limits for throttling

### Cpuminer-ulti Integration

Minerva is designed to work with **cpuminer-ulti**, an optimized CPU miner for Monero. The miner provides:
- Statistics API for real-time monitoring
- Lightweight process suitable for Raspberry Pi
- Support for GPU acceleration (if available)

To enable the API for stats collection, start cpuminer-ulti with the `--api-bind` parameter:
```bash
cpuminer-ulti --cpu-threads=1 --api-bind=127.0.0.1:4048
```

**To enable cpuminer-ulti API:**
```bash
# Basic setup with API enabled on localhost:4048
cpuminer-ulti --cpu-threads=1 --api-bind=127.0.0.1:4048

# With pool configuration
cpuminer-ulti --cpu-threads=1 -o stratum+tcp://pool.moneroocean.stream:10128 \
  -u YOUR_MONERO_ADDRESS --api-bind=127.0.0.1:4048
```

**Test API compatibility:**
```bash
python3 test_miner_compatibility.py
```
Tests connection to cpuminer-ulti API and parses mining statistics.

## Usage

1. **Access the dashboard** at `http://<raspberry-pi-ip>:5000`
2. **Chat with EVA** - Use the AI assistant interface for questions and help
3. **Monitor system stats** - View real-time CPU, memory, temperature, and uptime
4. **Track mining** - Monitor hashrate, total mined XMR, miner uptime, and daily yield estimates

## Management

The dashboard can be managed using the provided management script:

```bash
# Start the service
sudo ./manage.py start

# Stop the service
sudo ./manage.py stop

# Restart the service
sudo ./manage.py restart

# Check service status
sudo ./manage.py status

# View logs
sudo ./manage.py logs

# View last 100 lines of logs
sudo ./manage.py logs -n 100
```

## Updating

To pull the latest changes from the repository:

```bash
git pull origin main
pip install -r requirements.txt
sudo systemctl restart rpi-dashboard.service
```

## Utilities

The following utility scripts are included to help with deployment and testing:

- **`verify_optimization.py`** - Verify performance optimizations and resource usage
- **`test_miner_compatibility.py`** - Test cpuminer-ulti API compatibility
- **`miner_quick_ref.py`** - Quick reference for cpuminer-ulti command-line configuration
- **`DEPLOYMENT_CHECKLIST.py`** - Automated deployment verification checklist
- **`monitor_mining.py`** - Monitor mining with automatic CPU throttling

## Testing & Verification

**Test miner API compatibility:**
```bash
python3 test_miner_compatibility.py
```
Tests connection to cpuminer-ulti API and validates response parsing.

**Verify performance optimizations:**
```bash
python3 verify_optimization.py
```

**Run deployment checklist:**
```bash
python3 DEPLOYMENT_CHECKLIST.py
```

## Performance Optimizations

Minerva is optimized for low-power devices like Raspberry Pi Zero:

- **Non-blocking API calls** with connection pooling
- **Lightweight polling** (3-second updates) instead of WebSockets
- **Minimal logging** (WARNING level only) to reduce I/O overhead
- **Production Flask configuration** with debug disabled
- **Efficient codebase** (~27.8 KB core)
- **Low memory footprint** (40-50 MB runtime)
- **Single-core optimized** for Raspberry Pi Zero

## Monitoring & Management

**Monitor mining with automatic CPU throttling:**
```bash
# Run the mining monitor (default 50% CPU threshold)
python3 monitor_mining.py

# With custom CPU threshold
python3 monitor_mining.py --threshold 65
```

**View service logs:**
```bash
sudo journalctl -u rpi-dashboard.service -f
```

**Manage the service:**
```bash
# Start/stop/restart
sudo systemctl start rpi-dashboard.service
sudo systemctl stop rpi-dashboard.service
sudo systemctl restart rpi-dashboard.service

# Check status
sudo systemctl status rpi-dashboard.service
```

## Documentation

- [API Documentation](docs/api.md) - API endpoints and responses
- [Deployment Guide](docs/deployment.md) - Production deployment instructions
- [Module Documentation](docs/modules.md) - Internal module reference

## Contributing

Contributions are welcome! Please ensure all changes maintain the performance optimizations and low resource usage requirements.

## License

See [LICENSE](LICENSE) file for details.