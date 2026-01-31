# Raspberry Pi Server Dashboard

A lightweight web-based control panel for Raspberry Pi Zero that provides:
- AI study assistant via external free AI API
- Real-time system performance monitoring
- Live crypto mining statistics
- Continuous operation with minimal resource usage

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
server/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── api/
│   ├── ai_client.py       # AI API client
│   ├── system_stats.py    # System statistics collection
│   └── miner_stats.py     # Mining statistics collection
├── templates/
│   └── dashboard.html     # Main dashboard template
├── static/
│   ├── style.css          # Styling
│   └── app.js             # Frontend JavaScript
├── config/
│   └── settings.env       # Environment configuration
└── services/
    └── startup.sh         # Startup script
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rpi_server/server
```

2. Run the installation script:
```bash
./install.sh
```

Or manually install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp config/settings.env config/settings.env.local
# Edit config/settings.env.local with your settings
```

4. Start the server:
```bash
python app.py
```

Or use the systemd service:
```bash
sudo ./manage.py setup
sudo systemctl start rpi-dashboard.service
```

## Configuration

Edit `config/settings.env` to configure:

- Flask settings
- AI API settings (URL, key, model)
- XMRig API settings
- Logging preferences

### XMRig Compatibility

This dashboard is compatible with **XMRig 2.8.3 and newer** versions, including:
- **XMRig 2.8.3** (older versions)
- **rPi-xmrig-gcc7.3.0** (Raspberry Pi optimized builds)
- **XMRig 5.x+** (newer versions)

The API handler automatically detects and parses response formats from both old and new XMRig versions.

**To enable XMRig API:**
```bash
# For XMRig 2.8.3
xmrig -o pool.moneroocean.stream:10128 -u YOUR_ADDRESS --api-host 127.0.0.1 --api-port 18080

# For newer versions
xmrig -o pool.moneroocean.stream:10128 -u YOUR_ADDRESS --api-host 0.0.0.0 --api-port 18080
```

**Test API compatibility:**
```bash
python3 test_xmrig_compatibility.py
```

This will verify both old (2.8.3) and new format parsing and test against your live XMRig instance.

## Usage

1. Access the dashboard at `http://<raspberry-pi-ip>:5000`
2. Use the chat interface to interact with the AI assistant
3. Monitor system and mining statistics in real-time

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

## Development Phases

1. **Core UI + Server** - Dashboard layout, live stats
2. **AI Integration** - Chat interface with AI API
3. **Mining Widget** - Live XMRig statistics
4. **Optimization** - Lightweight polling, minimal logging, production config
5. **Compatibility** - Support for XMRig 2.8.3+ versions

## Testing

Test XMRig API compatibility:

```bash
# Test with your XMRig version
python3 test_xmrig_compatibility.py
```

This tests parsing of both XMRig 2.8.3 and newer formats.

## Performance Rules

- Non-blocking API calls with connection pooling
- Lightweight polling (3-second updates) instead of WebSockets
- Minimal logging (WARNING level only) to reduce I/O
- Production Flask configuration (debug disabled)
- ~27.8 KB core codebase, 40-50 MB runtime memory
- CPU-friendly for Raspberry Pi Zero single-core processor

## Monitoring

Monitor mining with automatic CPU throttling:

```bash
# Run the mining monitor
python3 monitor_mining.py

# With custom CPU threshold (default 50%)
python3 monitor_mining.py --threshold 65
```

View service logs:
```bash
sudo journalctl -u rpi-dashboard.service -f
```

## Future Expansion

- Simple user authentication (username + password)