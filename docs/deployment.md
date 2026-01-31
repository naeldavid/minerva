
# Deployment Guide

## Prerequisites
- Raspberry Pi Zero/Zero W/Zero 2 W
- Python 3.7+
- Internet connection

## Installation Steps

1. Clone the repository:
```bash
git clone <repository-url>
cd rpi_server/server
```

2. Run the installation script:
```bash
./install.sh
```

3. Configure environment variables:
```bash
nano config/settings.env
```

4. Start the service:
```bash
sudo ./manage.py setup
sudo systemctl start rpi-dashboard.service
```

## Configuration

### AI API Settings
- `AI_API_URL`: URL to your AI API endpoint
- `AI_API_KEY`: API key for authentication (if required)
- `AI_MODEL`: Model to use for requests

### XMRig Settings
- `XMRIG_API_URL`: URL to XMRig API endpoint

### Flask Settings
- `SECRET_KEY`: Secret key for Flask sessions
- `FLASK_ENV`: Environment (development/production)
- `FLASK_DEBUG`: Debug mode (True/False)

## Systemd Service

The dashboard runs as a systemd service for automatic startup and recovery.

To check service status:
```bash
sudo systemctl status rpi-dashboard.service
```

To view logs:
```bash
journalctl -u rpi-dashboard.service -f
```
