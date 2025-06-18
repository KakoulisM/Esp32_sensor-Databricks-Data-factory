from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "sensor_log.json"

# Initialize the log file if it doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

@app.route('/data', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid or missing JSON"}), 400

        humidity = data.get("humidity")
        temperature = data.get("temperature_c")

        if humidity is None or temperature is None:
            return jsonify({"error": "Missing humidity or temperature"}), 400

        # Timestamp the data
        timestamp = datetime.utcnow().isoformat() + "Z"
        entry = {
            "timestamp": timestamp,
            "humidity": humidity,
            "temperature_c": temperature
        }

        # Read current log
        with open(LOG_FILE, "r") as f:
            log_data = json.load(f)

        # Append new entry
        log_data.append(entry)

        # Save updated log
        with open(LOG_FILE, "w") as f:
            json.dump(log_data, f, indent=2)

        print(f"Logged data at {timestamp}: {entry}")
        return jsonify({"message": "Data received and logged"}), 200

    except Exception as e:
        print(f"Server error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
