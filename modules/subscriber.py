import random
from paho.mqtt import client as mqtt_client

ELIGIBLE_MESSAGES = ["OPEN", "CLOSE"]

class Subscriber:
    """
    A class used to represent a subscriber of a MQTT server.

    ...

    Attributes
    ----------
    broker : str
        The MQTT broker - ('broker.emqx.io') by default.
    port : int
        The MQTT server port - (1883) by default.
    topic : str
        The topic name - ('maannhai-mqtt') by default.
    callback : int
        The callback function.
    client_id : str
        The client id, e.g. - [subscribe-XXXX].
    client: paho.mqtt.client.Client
        The client object.


    Methods
    -------
    connect()
        Connects the client to the MQTT broker.
    subscribe()
        Subcribe messages from the MQTT broker.
    run()
        Runs the main program flow.
    """

    def __init__(self, callback, broker='broker.emqx.io', port=1883, topic="maannhai-mqtt"):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.callback = callback
        self.client_id = f'subscribe-{random.randint(0, 1000)}'
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
                print(f"Failed to connect, return code {rc}\n")

        self.client.on_connect = on_connect
        self.client.connect(self.broker, self.port)

    def subscribe(self):
        """Subcribes messages from the MQTT broker.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        def on_message(client, userdata, msg):
            """Decodes message from MQTT broker.

            Parameters
            ----------
            client : str
                The client name.
            userdata : str
                The userdata.
            msg : str
                The message.

            Returns
            -------
            None
            """

            message = msg.payload.decode()
            print(f"Received `{message}` from `{msg.topic}` topic")

            if message in ELIGIBLE_MESSAGES:
                self.callback(message)
            else:
                print(f"[MQTT] Unknown message: {message}")

        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def run(self):
        """Runs main programs including the connect function, the subscribe function, and client loop.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        
        self.connect()
        self.subscribe()
        self.client.loop_forever()


if __name__ == "__main__":
    def callback(msg):
        print(f"Correct message format: {msg}")
    mqtt_subscriber = Subscriber(callback=callback)
    mqtt_subscriber.run()
