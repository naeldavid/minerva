# Minerva

**Minerva** (Miner + EVA) is a lightweight web-based control panel for Raspberry Pi Zero that combines cryptocurrency mining management with an integrated AI assistant. It provides:
- AI study assistant (EVA) via external free AI API
- Real-time system performance monitoring
- Live crypto mining statistics with XMRig integration
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
├── test_xmrig_compatibility.py     # XMRig version compatibility tester
├── xmrig_quick_ref.py              # XMRig configuration reference
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
│  minerva
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

   **Production with systemd:**.txt
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
**Flask settings** - Port, debug mode, host
- **AI API settings** - API URL, authentication key, model configuration
- **XMRig API settings** - Host and port for mining API
- **Logging preferences** - Log level and output configuration
- **Mining thresholds** - CPU usage limits for throttling

### XMRig Compatibility

Minerva is compatible with **XMRig 2.8.3 and newer** versions, including:
- **XMRig 2.8.3** (legacy versions)
- **Raspberry Pi optimized builds** (rPi-xmrig)
- **XMRig 5.x+** (modern versions)

The API handler automatically detects and parses response formats from both old and new XMRig versions. Test your specific version with `test_xmrig_compatibility.py`
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

Thi**Access the dashboard** at `http://<raspberry-pi-ip>:5000`
2. **Chat with EVA** - Use the AI assistant interface for questions and help
3. **Monitor system stats** - View real-time CPU, memory, temperature, and uptime
4. **Track mining** - Monitor hashrate, total mined XMR, miner uptime, and daily yield estimates

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
gitUtilities

The following utility scripts are included to help with deployment and testing:

- **`verify_optimization.py`** - Verify performance optimizations and resource usage
- **`test_xmrig_compatibility.py`** - Test XMRig API compatibility with your miner version
- **`xmrig_quick_ref.py`** - Quick reference for XMRig command-line configuration
- **`DEPLOYMENT_CHECKLIST.py`** - Automated deployment verification checklist
- **`monitor_mining.py`** - Monitor mining with automatic CPU throttling
1. **Core UI + Server** - Dashboard layout, live stats
2. **AI Integration** - Chat interface with AI API
3. **Minin & Verification

**Test XMRig API compatibility:**
```bash
python3 test_xmrig_compatibility.py
```
Tests parsing of both XMRig 2.8.3 and newer format responses with your live miner.

**Verify performance optimizations:**
```bash
python3 verify_optimization.py
```
Optimizations

Minerva is optimized for low-power devices like Raspberry Pi Zero:

- **Non-blocking API calls** with connection pooling
- **Lightweight polling** (3-second updates) instead of WebSockets
- **Minimal logging** (WARNING level only) to reduce I/O overhead
- **Production Flask configuration** with debug disabled
- **Efficient codebase** (~27.8 KB core)
- **Low memory footprint** (40-50 MB runtime)
- **Single-co & Management

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
# With custom CPU threshold (default 50%)
python3 monitor_mining.py --threshold 65
```

View service logs:
```bash
sudo journalctl -u rpi-dashboard.service -f
```

## Future Expansion

- Simple user authentication (username + password)