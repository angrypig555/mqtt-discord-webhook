# mqtt-discord-webhook
small python script to send you a discord webhook for MQTT events
Environment variables:

- `MQTT_BROKER_IP` IP for MQTT broker
- `MQTT_PORT` Port for the MQTT broker
- `MQTT_TOPIC` MQTT topic to listen for
- `MQTT_DC_WEBHOOK` URL for the discord webhook
- `MQTT_DC_MESSAGE` Message to send when webhook is triggered
- `MQTT_PASS` Password for MQTT broker (highly reccomended to set up)
- `MQTT_USER` Username for MQTT broker (highly reccomended to set up)

A `.env` file can be used or the environment variables can be passed.
If running in a swarm cluster, it is reccomended to use secrets for the password instead of env variables.

The built container is available at https://hub.docker.com/r/angrypig555/mqtt-discord-webhook?tag=latest but it is not required to use a container.
Example compose.yaml file for swarm deployment:
``` yaml
services:
  webhook:
    image: angrypig555/mqtt-discord-webhook
    restart: unless-stopped
    environment:
      - MQTT_BROKER_IP=BROKER_IP_HERE
      - MQTT_TOPIC=TOPIC_HERE
      - MQTT_DC_WEBHOOK=/run/secrets/dc_webhook
      - MQTT_USER=USER_HERE
      - MQTT_PASS=/run/secrets/mqtt_pass
      - MQTT_DC_MESSAGE=MESSAGE_TO_SEND_HERE
      - MQTT_PORT=PORT_HERE # usually 1883

secrets:
  mqtt_pass:
    external: true
  dc_webhook:
    external: true
```