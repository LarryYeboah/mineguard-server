from flask import Flask, request, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)

# Allow requests from your Vercel dashboard specifically
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://miningsafetydashboard.vercel.app",
            "https://miningsafetydashboard-*.vercel.app",
            "*"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Accept", "User-Agent",
                          "ngrok-skip-browser-warning"]
    }
})

latest = {"gas": 0.0, "temp": 25.0, "hum": 60.0}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Accept,User-Agent')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,POST,OPTIONS')
    return response

@app.route('/data', methods=['POST', 'OPTIONS'])
def receive():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    global latest
    data = request.get_json(force=True, silent=True)
    if data:
        latest["gas"]  = float(data.get("gas",  latest["gas"]))
        latest["temp"] = float(data.get("temp", latest["temp"]))
        latest["hum"]  = float(data.get("hum",  latest["hum"]))
        print(f"Data: gas={latest['gas']} "
              f"temp={latest['temp']} hum={latest['hum']}")
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"}), 400

@app.route('/latest', methods=['GET', 'OPTIONS'])
def send():
    if request.method == 'OPTIONS':
        return make_response('', 204)
    return jsonify(latest)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "MineGuard running", "data": latest})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
