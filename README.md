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
