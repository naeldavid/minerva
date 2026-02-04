# Minerva

**Minerva** (Miner + EVA) is a lightweight web-based control panel for Raspberry Pi Zero that combines cryptocurrency mining management with an integrated AI assistant. It provides:
- AI study assistant (EVA) via external free AI API
- Real-time system performance monitoring
- Live crypto mining statistics with Duino-Coin integration
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
- Total DUCO mined
- Current hashrate estimate
- Miner configuration
- Thread count

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
- **Duino-Coin settings** - Path to duino-coin directory, username
- **Logging preferences** - Log level and output configuration

**IMPORTANT SECURITY:** Generate a strong secret key before deployment:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Duino-Coin Integration

Minerva is designed to work with **Duino-Coin**, a cryptocurrency that can be mined on low-power devices like Raspberry Pi.

**Setup:**
1. Install Duino-Coin miner in `/Dev/duino-coin` (or configure path in settings.env)
2. Configure your Duino-Coin username in `config/settings.env`
3. Start the Duino-Coin miner separately
4. Minerva will read mining statistics from the Duino-Coin configuration

**Configuration:**
```bash
# In config/settings.env
DUINO_COIN_PATH=/Users/nae1/Dev/duino-coin
DUINO_COIN_USERNAME=your-username
```

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

The following utility scripts are included:

- **`monitor_mining.py`** - Monitor mining with automatic CPU throttling

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