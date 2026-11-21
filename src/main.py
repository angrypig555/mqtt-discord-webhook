import paho.mqtt.client as mqtt
from paho.mqtt import subscribe
import os
from dotenv import load_dotenv

load_dotenv()

ip = os.environ["MQTT_BROKER_IP"]
topic = os.environ["MQTT_TOPIC"]
webhook = os.environ["MQTT_DC_WEBHOOK"]
username = os.environ["MQTT_USER"]
password = os.environ["MQTT_PASS"]

print("mqtt discord webhook")
print("using topic ", topic, " and broker ", ip)

auth = {"username": username, "password": password} if username else None

m = subscribe.simple(topic, hostname=ip, retained=False, msg_count=2, auth=auth)
for a in m:
    print(a.topic)
    print(a.payload)
