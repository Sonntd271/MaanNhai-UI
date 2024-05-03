from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return open('index.html').read()

@app.route('/open')
def open_button():
    print("Received Open request from client")
    return {"status": "success"}

@app.route('/close')
def close_button():
    print("Received Close request from client")
    return {"status": "success"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
