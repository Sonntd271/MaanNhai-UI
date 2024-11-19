import time
from paho.mqtt import client as mqtt_client

class Publisher:
    def __init__(self, broker='broker.emqx.io', port=1883, topic="maannhai-mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'python-mqtt-{int(time.time())}'
        self.client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

        # Set up callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(self, client, userdata, flags, rc, properties=None):
        """Callback when the client connects to the broker"""
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_disconnect(self, client, userdata, flags, rc, properties=None):
        """Callback when the client disconnects"""
        if rc != 0:
            print(f"Unexpected disconnection (rc={rc}). Reconnecting...")
            self.reconnect()

    def connect(self):
        """Initiate an asynchronous connection"""
        self.client.connect_async(self.broker, self.port)
        self.client.loop_start()

    def reconnect(self):
        """Reconnect with exponential backoff"""
        delay = 1 
        while not self.client.is_connected():
            try:
                print(f"Reconnecting in {delay} seconds...")
                time.sleep(delay)
                self.client.reconnect()
                delay = min(delay * 2, 30)
            except Exception as e:
                print(f"Reconnect failed: {e}")

    def publish(self, message):
        """Publish a message to the MQTT topic"""
        result = self.client.publish(self.topic, message)
        status = result[0]
        
        return status

    def disconnect(self):
        """Disconnect the client"""
        self.client.loop_stop()
        self.client.disconnect()

if __name__ == "__main__":
    mqtt_publisher = Publisher()
    mqtt_publisher.connect()

    try:
        while True:
            mqtt_publisher.publish("TESTING")
            time.sleep(5)  # Publish messages every 5 seconds
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        mqtt_publisher.disconnect()
