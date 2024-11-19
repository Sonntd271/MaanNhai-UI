import logging
from flask import Flask, render_template, jsonify
from modules.publisher import Publisher

TOPIC = "maannhai-mqtt"

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Redirect Flask logs to the same file
app.logger.addHandler(logging.FileHandler("app.log"))
app.logger.setLevel(logging.INFO)

mqtt_publisher = Publisher(topic=TOPIC)
mqtt_publisher.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open')
def open_button():
    message = "OPEN"
    status = mqtt_publisher.publish(message)
    if status == 0:
        app.logger.info(f"Successfully sent {message} to topic {TOPIC}")
    else:
        app.logger.warning(f"Failed to send a message to {TOPIC}")
    
    return jsonify(status="success")

@app.route('/close')
def close_button():
    message = "CLOSE"
    status = mqtt_publisher.publish(message)
    if status == 0:
        app.logger.info(f"Successfully sent {message} to topic {TOPIC}")
    else:
        app.logger.warning(f"Failed to send a message to {TOPIC}")

    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
