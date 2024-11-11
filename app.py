from flask import Flask, render_template, jsonify
from modules.publisher import Publisher

app = Flask(__name__)

mqtt_publisher = Publisher()
mqtt_publisher.connect()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open')
def open_button():
    mqtt_publisher.publish("OPEN")
    return jsonify(status="success")

@app.route('/close')
def close_button():
    mqtt_publisher.publish("CLOSE")
    return jsonify(status="success")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
