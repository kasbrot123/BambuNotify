# BambuNotify

Leichtgewichtiges Python-Skript (optional als Docker-Container), das den lokalen MQTT-Status eines Bambu Lab 3D-Druckers überwacht und bei abgeschlossenem oder fehlgeschlagenem Druck eine Benachrichtigung per Telegram sendet.

## Features

- Lokale Überwachung über Bambu Lab MQTT (Port `8883`, TLS)
- Telegram-Benachrichtigung bei Wechsel von `RUNNING`/`PAUSE` auf `FINISH` oder `FAILED`
- Konfigurierbar über Umgebungsvariablen / `.env`-Datei
- Lauffähig direkt per Python oder als Docker-Container

## Voraussetzungen

- **Bambu Lab Drucker** im lokalen Netzwerk (IP-Adresse, 15-stellige Seriennummer und 8-stelliger Access Code)
- **Telegram Bot Token** (über [@BotFather](https://t.me/BotFather) mit `/newbot`)
- **Telegram Chat-ID** (z. B. über `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates` nach der ersten Nachricht an den Bot)

## Projektstruktur

```text
BambuNotify/
├── bambu_notify.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## Einrichtung & Start

### Variante A: Mit Docker (empfohlen für Dauerbetrieb)

1. Repository klonen und in den Ordner wechseln:
   ```bash
   git clone <URL-ZU-DEINEM-REPO>/BambuNotify.git
   cd BambuNotify
   ```
2. `.env`-Datei aus der Vorlage erstellen und ausfüllen:
   ```bash
   cp .env.example .env
   ```
3. Container bauen und im Hintergrund starten:
   ```bash
   docker compose up -d --build
   ```
4. Logs prüfen:
   ```bash
   docker compose logs -f
   ```

### Variante B: Direkt mit Python

1. Abhängigkeit installieren:
   ```bash
   pip install paho-mqtt
   ```
2. Umgebungsvariablen setzen (bzw. `.env` laden) und Skript starten:
   ```bash
   python -u bambu_notify.py
   ```

## Hinweise

- **Access Code:** Wird der LAN Access Code am Druckerdisplay neu generiert, muss er in der `.env`-Datei aktualisiert und der Dienst neu gestartet werden.
- **Sicherheit:** Die `.env`-Datei enthält Zugangsdaten und ist über `.gitignore` von Git ausgeschlossen.
