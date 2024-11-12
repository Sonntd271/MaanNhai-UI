import threading
import queue
from modules.maannhai import MaanNhai
from modules.subscriber import Subscriber

class DeviceController:
    def __init__(self):
        self.maannhai = MaanNhai(init_status="close")
        self.request_queue = queue.Queue()
        self.mqtt_subscriber = Subscriber(topic="maannhai-mqtt", callback=self.handle_mqtt_message)

    def handle_mqtt_message(self, message):
        """
        Callback function to handle MQTT messages.
        """
        self.request_queue.put(message)

    def device_loop(self):
        while True:
            if not self.request_queue.empty():
                action = self.request_queue.get()
                if action == "OPEN":
                    self.maannhai.open_curtain()
                elif action == "CLOSE":
                    self.maannhai.close_curtain()

    def start(self):
        # Start the device loop thread
        device_thread = threading.Thread(target=self.device_loop)
        device_thread.daemon = True
        device_thread.start()

        # Start the MQTT subscriber in the main thread
        self.mqtt_subscriber.run()
