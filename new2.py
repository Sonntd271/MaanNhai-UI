from flask import Flask, render_template, jsonify
import threading
import time
import queue
import RPi.GPIO as GPIO

from MaanNaai2 import *

app = Flask(__name__)

# Shared states
button_state = None  # None indicates no recent button press
waiting = True
request_queue = queue.Queue()

def print_waiting():
    global waiting, button_state
    while True:
        if button_state is None:  # Only print waiting if no button has been pressed recently
            print("[SERVER] Waiting")
        time.sleep(1)  # Print every second

@app.route('/')
def index():
    global waiting, button_state
    waiting = True
    button_state = None  # Reset button state when loading the page
    return render_template('index.html')

@app.route('/open')
def open_button():
    request_queue.put(True)
    return jsonify(status="success")

@app.route('/close')
def close_button():
    request_queue.put(False)
    return jsonify(status="success")

STATUS = "close"
def device_loop():
    global button_state, waiting
    status = STATUS
    while True:
        if not request_queue.empty():
            button_state = request_queue.get()
        
        if button_state is not None:  # There has been a button press
            if not button_state and status == "close":
                moveUntilMotor()
                status = "open"
                print("[SERVER] Curtains are OPENED")
            elif button_state and status == "open":
                moveUntilPulley()
                status = "close"
                print("[SERVER] Curtains are CLOSED")
            button_state = None  # Reset button state after processing
            waiting = True  # Resume waiting after action

        ledGreen()
        

        if not lmPulley.is_active:
            # print("lmpulley active")
            stopPulley()
            status = "close"
        if not lmMotor.is_active:
            # print("lmmotor active")
            stopMotor()
            status = "open"
            
        if button1.is_pressed:
            print("b1 pressed")
            if status == "close":
                ledCyan()
                moveToMotor()
                time.sleep(0.005)
            else:
                ledYellow()
                moveToPulley()
                time.sleep(0.005)

        if button2.is_pressed:
            print("b2 pressed")
            if button1.is_pressed:
                moveHome()
                break

            if status == "close":
                moveUntilMotor()
                time.sleep(0.01)
                status = "open"
            else:
                moveUntilPulley()
                time.sleep(0.01)
                status = "close"

if __name__ == '__main__':
    waiting_thread = threading.Thread(target=print_waiting)
    waiting_thread.daemon = True 
    waiting_thread.start()

    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8000})
    flask_thread.daemon = True
    flask_thread.start()

    # Start the device loop
    device_thread = threading.Thread(target=device_loop)
    device_thread.daemon = True
    device_thread.start()

    # Join threads to prevent main thread from exiting
    flask_thread.join()
    device_thread.join()
