from flask import Flask, render_template, jsonify
import threading
import time

app = Flask(__name__)

# Shared states
button_state = None  # None indicates no recent button press
waiting = True

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
    global button_state, waiting
    button_state = True
    waiting = False
    print("Received CLOSE request from client")
    return jsonify(status="success")

@app.route('/close')
def close_button():
    global button_state, waiting
    button_state = False
    waiting = False
    print("Received OPEN request from client")
    return jsonify(status="success")

def device_loop():
    global button_state, waiting
    while True:
        time.sleep(1)  # Check button state every second
        if button_state is not None:  # There has been a button press
            if button_state:
                print("[SERVER] Curtains are CLOSED")
            else:
                print("[SERVER] Curtains are OPEN")
            button_state = None  # Reset button state after processing
            waiting = True  # Resume waiting after action

if __name__ == '__main__':
    waiting_thread = threading.Thread(target=print_waiting)
    waiting_thread.daemon = True 
    waiting_thread.start()

    device_thread = threading.Thread(target=device_loop)
    device_thread.daemon = True
    device_thread.start()

    # Start the Flask application
    app.run(host='0.0.0.0', port=8000)
