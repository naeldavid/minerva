# Minerva — AI chat dashboard (Pi Zero W optimized)

Minerva is a lightweight, Pi Zero W–friendly web dashboard that provides a simple AI chat interface powered by a Hugging Face cloud model and a small system-status panel. This trimmed-down edition focuses on minimal resource usage and reliable behavior on low-memory devices.

Highlights:
- AI chat powered by a Hugging Face hosted model (cloud inference)
- Lightweight system stats: CPU, memory, temperature, uptime
- Minimal dependencies and low polling frequency for Pi Zero W

## Features

- AI Chat: send messages to your Hugging Face model and receive responses
- System Monitoring: lightweight periodic stats (cached on server)
- Small footprint: tuned for Raspberry Pi Zero W (reduced polling, single-threaded server)

## Project Structure

```
minerva/
├── app.py                   # Main Flask application (single-threaded run for Pi Zero)
├── requirements.txt         # Python dependencies
├── LICENSE                  # Project license
├── api/
│   ├── ai_client.py         # Hugging Face client (router.huggingface.co default)
│   └── system_stats.py      # Lightweight system statistics with caching
├── config/
│   └── settings.env         # Environment configuration file
├── templates/
│   └── dashboard.html       # Main dashboard template (AI chat + system widget)
├── static/
│   ├── style.css            # Dashboard styling
│   └── app.js               # Frontend JavaScript (reduced polling)
└── services/
    └── rpi-dashboard.service # Optional systemd service file
```

## Quick Start (Raspberry Pi Zero W)

1. Clone the repo and install dependencies:

```bash
git clone https://github.com/nae1/minerva.git
cd minerva
python3 -m pip install -r requirements.txt
```

2. Configure `config/settings.env` (required):

Open the file and set at minimum:

```ini
# Flask
SECRET_KEY=generate-with-python3-c-import-secrets-print-secrets-token-hex-32

# Hugging Face (default uses router endpoint)
AI_API_URL=https://router.huggingface.co/models/nae1/eva
AI_API_KEY=hf_your_token_here
AI_MODEL=nae1/eva

# Logging
LOG_LEVEL=WARNING
```

Notes:
- Obtain `AI_API_KEY` from https://huggingface.co/settings/tokens
- `AI_API_URL` defaults to the router endpoint (`router.huggingface.co`) which is recommended by Hugging Face.

3. Run the app (recommended for Pi Zero W):

```bash
python3 app.py
```

This runs Flask single-threaded and without the reloader (lower memory use). The dashboard is available at `http://<pi-ip>:5000`.

Optional: create a systemd service using `services/rpi-dashboard.service` to run on boot.

## Usage

- Open the dashboard in a browser on the same network and use the chat box to talk to your model.
- AI requests are proxied to Hugging Face — the first request may take longer while the model loads.

## Configuration Reference

- `AI_API_URL` — Full URL to the Hugging Face inference endpoint. Default: `https://router.huggingface.co/models/nae1/eva`
- `AI_API_KEY` — Your Hugging Face token (required for private models or higher rate limits)
- `AI_MODEL` — Model identifier (e.g., `nae1/eva`)
- `LOG_LEVEL` — Logging verbosity; use `WARNING` or `ERROR` on Pi Zero

Security note: Keep `AI_API_KEY` secret. This project is intended for local networks; if exposing publicly, use a reverse proxy with authentication.

## Performance Optimizations for Pi Zero W

- Server: single-threaded Flask (`threaded=False`, `use_reloader=False`) to reduce memory overhead.
- Polling: frontend polls system stats every 10 seconds (reduced from 3s).
- Caching: `api/system_stats.py` caches stats for 10s to avoid repeated work.
- Lightweight temp read: reads `/sys/class/thermal/thermal_zone0/temp` first (fast), falls back to `vcgencmd` only if necessary.
- Minimal logging: default `LOG_LEVEL=WARNING`.

Recommended tuning:
- Lower polling frequency further if you don't need frequent updates.
- Run behind a small reverse proxy (nginx) if exposing externally.

## Health & Troubleshooting

- Health endpoint: `GET /health` returns module availability and timestamp.
- If AI calls return errors, confirm `AI_API_KEY` and `AI_API_URL` are correct.
- If the model takes a long time to respond, it's normal on first load; subsequent calls are faster.

## Development & Contributing

Contributions welcome. Keep changes lightweight and Pi-Zero-friendly. If adding features that consume CPU or memory, include a configuration option to disable them on low-end devices.

## License

See [LICENSE](LICENSE) for license details.
