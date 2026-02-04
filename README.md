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
├── app.py                   # Main Flask application
├── manage.py                # Service management script
├── monitor_mining.py        # Mining monitoring with CPU throttling
├── requirements.txt         # Python dependencies
├── LICENSE                  # Project license
├── install.sh               # Installation script
├── README.md                # This file
├── .gitignore               # Git ignore rules
├── api/
│   ├── ai_client.py         # AI API client for EVA assistant
│   ├── system_stats.py      # System statistics collection
│   └── miner_stats.py       # Duino-Coin statistics reader
├── config/
│   └── settings.env         # Environment configuration file
├── templates/
│   └── dashboard.html       # Main dashboard template
├── static/
│   ├── style.css            # Dashboard styling
│   └── app.js               # Frontend JavaScript
└── services/
    ├── rpi-dashboard.service # systemd service file
    └── startup.sh            # Service startup script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/naeldavid/minerva.git
cd minerva
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

3. Configure environment variables:
```bash
nano config/settings.env
```

**Required configuration:**
```bash
# Generate a strong secret key
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# Configure AI API (Ollama)
AI_API_URL=http://localhost:11434/api/generate
AI_MODEL=llama2

# Configure Duino-Coin
DUINO_COIN_PATH=/home/pi/duino-coin
DUINO_COIN_USERNAME=your-username
```

4. Start the server:

**Direct mode:**
```bash
python3 app.py
# Access at http://<raspberry-pi-ip>:5000
```

**Production with systemd:**
```bash
sudo python3 manage.py setup
sudo systemctl start rpi-dashboard.service
```

## Configuration

Edit `config/settings.env`:

```bash
# Flask Settings
SECRET_KEY=your-secret-key-here  # Generate with: python3 -c "import secrets; print(secrets.token_hex(32))"
FLASK_ENV=production
FLASK_DEBUG=False

# AI API Settings (Ollama)
AI_API_URL=http://localhost:11434/api/generate
AI_API_KEY=
AI_MODEL=llama2

# Miner Settings (Duino-Coin)
DUINO_COIN_PATH=/home/pi/duino-coin
DUINO_COIN_USERNAME=your-username

# Logging
LOG_LEVEL=WARNING
```

### Duino-Coin Integration

Minerva reads mining statistics from Duino-Coin configuration files.

**Setup:**
```bash
# 1. Install Duino-Coin
cd ~
git clone https://github.com/revoxhere/duino-coin.git
cd duino-coin
python3 PC_Miner.py  # Configure username and settings

# 2. Update Minerva config
nano ~/minerva/config/settings.env
# Set: DUINO_COIN_PATH=/home/pi/duino-coin
# Set: DUINO_COIN_USERNAME=your-username

# 3. Start both
python3 ~/duino-coin/PC_Miner.py &  # Start miner
python3 ~/minerva/app.py             # Start dashboard
```

## Usage

**Access:** `http://<raspberry-pi-ip>:5000` (accessible on local network)

**Features:**
- **AI Chat** - Ask EVA questions via Ollama
- **System Stats** - Real-time CPU, RAM, temperature, uptime
- **Mining Stats** - Hashrate, DUCO mined, thread count

## Management

```bash
# Service control
sudo python3 manage.py start|stop|restart|status

# View logs
sudo journalctl -u rpi-dashboard.service -f

# Monitor mining with CPU throttling
python3 monitor_mining.py --threshold 50
```

## Updating

```bash
cd ~/minerva
git pull
pip3 install -r requirements.txt
sudo systemctl restart rpi-dashboard.service
```

## Security

- **Local network only** - Binds to 0.0.0.0 (accessible on LAN)
- **Input validation** - All user inputs sanitized
- **XSS protection** - Content Security Policy headers
- **Updated dependencies** - Flask >=3.0.0, requests >=2.32.0
- **No default keys** - Auto-generates secure SECRET_KEY

**Note:** Only use on trusted local networks. For internet exposure, add firewall rules or reverse proxy with authentication.

## Performance

**Optimized for Raspberry Pi Zero W:**
- **Memory:** 20-30MB (dashboard) + 30-50MB (Duino-Coin) = ~55-75MB total
- **CPU:** <5% idle, 50-70% when mining
- **Codebase:** ~25KB Python
- **Polling:** 3-second updates (stops when page hidden)
- **No WebSockets:** Simple HTTP polling
- **Minimal logging:** WARNING level only

**Expected performance:**
- Dashboard load: 2-3 seconds
- Update latency: <500ms
- Duino-Coin hashrate: 1-3 kH/s (1 thread)

## Contributing

Contributions are welcome! Please ensure all changes maintain the performance optimizations and low resource usage requirements.

## License

See [LICENSE](LICENSE) file for details.