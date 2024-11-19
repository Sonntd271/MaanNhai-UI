import time
from paho.mqtt import client as mqtt_client

class Publisher:
    """
    A class used to represent a publisher of a MQTT server.

    ...

    Attributes
    ----------
    broker : str
        The MQTT broker - ('broker.emqx.io') by default.
    port : int
        The MQTT server port - (1883) by default.
    topic : str
        The topic name - ('maannhai-mqtt') by default.
    client_id : str
        The client id, e.g. - [python-mqtt-XXXX].
    client : paho.mqtt.client.Client
        The client object.


    Methods
    -------
    connect()
        Connects the client to the MQTT broker.
    publish(message)
        Subcribe messages from the MQTT broker.
    disconnect()
        Runs the main program flow.
    """

    def __init__(self, broker='broker.emqx.io', port=1883, topic="maannhai-mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client_id = f'python-mqtt-{int(time.time())}'
        self.client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

        # Setup callbacks
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect

    def on_connect(client, userdata, flags, rc, properties):
        """Checks connecting status of the client.

        Parameters
        ----------
        client : str
            The client name.
        userdata : str
            The userdata.
        flags : str
            The flags.
        rc : int
            The return code.
        properties : str
            The properties.

        Returns
        -------
        None
        """
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
        """Initiate an asynchronous connection from the client to the MQTT broker.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
        """Publishes a message to the MQTT broker.

        Parameters
        ----------
        message : str
            The MQTT message that will be published.

        Returns
        -------
        status : int
        """
        result = self.client.publish(self.topic, message)
        status = result[0]
        
        return status

    def disconnect(self):
        """Disconnects main programs including the client loop and client's connection with the broker.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
