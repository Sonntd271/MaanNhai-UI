import time
from paho.mqtt import client as mqtt_client

class Publisher:
    def __init__(self, broker='broker.emqx.io', port=1883, topic="maannhai-mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'python-mqtt-{time.time()}'
        self.client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    def connect(self):
        def on_connect(client, userdata, flags, rc, properties):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print(f"Failed to connect, return code {rc}")

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, message):
        result = self.client.publish(self.topic, message)
        status = result[0]
        if status == 0:
            print(f"Sent `{message}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    mqtt_publisher = Publisher()
    mqtt_publisher.connect()
    mqtt_publisher.publish("TESTING")
    mqtt_publisher.disconnect()
