from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest = {"gas": 0.0, "temp": 25.0, "hum": 60.0}

@app.route('/data', methods=['POST'])
def receive():
    global latest
    data = request.get_json(force=True, silent=True)
    if data:
        latest = data
        print(f"Received → Gas: {data['gas']} | Temp: {data['temp']} | Hum: {data['hum']}")
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/latest', methods=['GET'])
def send():
    return jsonify(latest)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "MineGuard server running", "data": latest})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)