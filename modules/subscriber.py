import random
from paho.mqtt import client as mqtt_client

ELIGIBLE_MESSAGES = ["OPEN", "CLOSE"]

class Subscriber:
    def __init__(self, callback, broker='broker.emqx.io', port=1883, topic="maannhai-mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.callback = callback
        self.client_id = f'subscribe-{random.randint(0, 1000)}'
        self.client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    def connect(self):
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}\n")

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def subscribe(self):
        def on_message(client, userdata, msg):
            message = msg.payload.decode()
            print(f"Received `{message}` from `{msg.topic}` topic")

            if message in ELIGIBLE_MESSAGES:
                self.callback(message)
            else:
                print(f"[MQTT] Unknown message: {message}")

        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def run(self):
        self.connect()
        self.subscribe()
        self.client.loop_forever()


if __name__ == "__main__":
    def callback(msg):
        print(f"Correct message format: {msg}")
    mqtt_subscriber = Subscriber(callback=callback)
    mqtt_subscriber.run()
