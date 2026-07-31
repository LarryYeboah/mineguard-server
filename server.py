from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")

latest = {"gas": 0.0, "temp": 25.0, "hum": 60.0}

@app.route('/data', methods=['POST', 'OPTIONS'])
def receive():
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"})
    global latest
    data = request.get_json(force=True, silent=True)
    if data:
        latest["gas"]  = float(data.get("gas",  latest["gas"]))
        latest["temp"] = float(data.get("temp", latest["temp"]))
        latest["hum"]  = float(data.get("hum",  latest["hum"]))
        print(f"Data: gas={latest['gas']} temp={latest['temp']} hum={latest['hum']}")
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/latest', methods=['GET'])
def send():
    return jsonify(latest)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "MineGuard running", "data": latest})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
