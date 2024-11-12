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
    client: paho.mqtt.client.Client
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
        self.client_id = f'python-mqtt-{time.time()}'
        self.client = mqtt_client.Client(client_id=self.client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    def connect(self):
        """Connects the client to the MQTT broker.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

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

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)
        self.client.loop_start()

    def publish(self, message):
        """Publishes a message to the MQTT broker.

        Parameters
        ----------
        message : str
            The MQTT message that will be published.

        Returns
        -------
        None
        """
                
        result = self.client.publish(self.topic, message)
        status = result[0]
        if status == 0:
            print(f"Sent `{message}` to topic `{self.topic}`")
        else:
            print(f"Failed to send message to topic {self.topic}")

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
    mqtt_publisher.publish("TESTING")
    mqtt_publisher.disconnect()
