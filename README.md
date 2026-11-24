# BambuNotify

Lightweight Python script (optionally packaged as a Docker container) that monitors the local MQTT status of a Bambu Lab 3D printer and sends a Telegram notification when a print finishes or fails.

## Features

- Local monitoring via Bambu Lab MQTT (port `8883`, TLS)
- Telegram notifications on status changes from `RUNNING`/`PAUSE` to `FINISH` or `FAILED`
- Configurable via environment variables / `.env` file
- Runs directly with Python or inside a Docker container

## Prerequisites

- **Bambu Lab printer** on your local network (IP address, 15-character serial number, and 8-character access code)
- **Telegram Bot Token** (created via [@BotFather](https://t.me/BotFather) using `/newbot`)
- **Telegram Chat ID** (available via `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` after sending a first message to your bot)

## Project Structure

```text
BambuNotify/
├── bambu_notify.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Setup & Usage

### Option A: With Docker (Recommended for Continuous Operation)

1. Clone the repository and navigate into the project directory:
   ```bash
   git clone https://github.com/kasbrot123/BambuNotify.git
   cd BambuNotify
   ```
2. Create a `.env` file from the template and fill in your credentials:
   ```bash
   cp .env.example .env
   ```
3. Build and start the container in the background:
   ```bash
   docker compose up -d --build
   ```
4. View the logs:
   ```bash
   docker compose logs -f
   ```

### Option B: Run Directly with Python

1. Install the required dependency:
   ```bash
   pip install paho-mqtt
   ```
2. Export your environment variables (or load `.env`) and start the script:
   ```bash
   python -u bambu_notify.py
   ```

## Notes

- **Access Code:** If the LAN access code is regenerated on the printer's display, update `ACCESS_CODE` in your `.env` file and restart the service.
- **Security:** Your `.env` file contains sensitive credentials and is excluded from version control via `.gitignore`.
