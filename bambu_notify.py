import json
import os
import ssl
import time
import urllib.request
import urllib.parse
import paho.mqtt.client as mqtt

PRINTER_IP = os.environ["PRINTER_IP"]
ACCESS_CODE = os.environ["ACCESS_CODE"]
SERIAL = os.environ["SERIAL"]
BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

last_state = None


def send_your_messenger(text: str):
    pass


def send_telegram(text: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": text}).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()

def send_notification(text: str):
    send_telegram(text)
    send_your_messenger(text)

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Verbunden mit Drucker (Code: {reason_code})")
    client.subscribe(f"device/{SERIAL}/report")

def on_message(client, userdata, msg):
    global last_state
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        print_data = payload.get("print", {})
        state = print_data.get("gcode_state")

        if state and state != last_state:
            print(f"Statuswechsel: {last_state} -> {state}")
            if state == "FINISH" and last_state in ("RUNNING", "PAUSE"):
                job_name = print_data.get("subtask_name") or "Unbekanntes Modell"
                send_telegram(f"3D-Druck fertig: {job_name}")
            elif state == "FAILED" and last_state in ("RUNNING", "PAUSE"):
                job_name = print_data.get("subtask_name") or "Unbekanntes Modell"
                send_telegram(f"3D-Druck fehlgeschlagen/abgebrochen: {job_name}")
            last_state = state
    except Exception as e:
        print(f"Fehler beim Verarbeiten: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set("bblp", ACCESS_CODE)

# Bambu-Drucker nutzen ein selbstsigniertes Zertifikat auf Port 8883
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
client.tls_set_context(context)

client.on_connect = on_connect
client.on_message = on_message

while True:
    try:
        client.connect(PRINTER_IP, 8883, 60)
        client.loop_forever()
    except Exception as e:
        print(f"Verbindung verloren ({e}), neuer Versuch in 10 Sekunden...")
        time.sleep(10)
