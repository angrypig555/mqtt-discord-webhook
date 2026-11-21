# note: this is meant to be used with frigate so it parses the json for frigate stuff but it can be modified
# TODO: grab screenshot from http://<frigate-host>:5000/api/events/<event_id>/snapshot.jpg
import json
import os
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
import requests

def load_secret_or_env(env_name: str, default: str | None = None) -> str | None:
    val = os.getenv(env_name, default)
    if val and os.path.isfile(val):
        with open(val, "r", encoding="utf-8") as f:
            return f.read().strip()
    return val

load_dotenv()

ip = os.environ["MQTT_BROKER_IP"]
port = int(os.getenv("MQTT_PORT", "1883"))
topic = os.getenv("MQTT_TOPIC", "frigate/events")
username = os.getenv("MQTT_USER")
password = load_secret_or_env("MQTT_PASS")
webhook_url = load_secret_or_env("MQTT_DC_WEBHOOK")
webhook_msg = os.getenv("MQTT_DC_MESSAGE")

payload = {"content": webhook_msg}

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic, qos=1)
    else:
        print(f"Connect failed: {reason_code}")


def on_message(client, userdata, msg):
    raw = msg.payload.decode("utf-8", errors="replace")
    print(f"Topic: {msg.topic}")
    try:
        data = json.loads(raw)
        event_type = data.get("type")
        after = data.get("after", {})
        print(
            f"type={event_type} | id={after.get('id')} | "
            f"camera={after.get('camera')} | label={after.get('label')}"
        )
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200 and response.status_code != 204:
            print("WEBHOOK FAILED! status code: ", response.status_code)
        else:
            print("webhook sent succesfully with response", response.status_code)
    except json.JSONDecodeError:
        print(raw)


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
if username:
    client.username_pw_set(username, password)

client.on_connect = on_connect
client.on_message = on_message

while True:
    try:
        client.connect(ip, port, keepalive=60)
        # Blocks and processes incoming messages continuously until disconnected
        client.loop_forever(retry_first_connection=True)
    except Exception as exc:
        print(f"MQTT loop error: {exc} — retrying in 5s...")
        time.sleep(5)