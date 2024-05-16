from flask import Blueprint, request, jsonify
import json
from datetime import datetime

temperature_api = Blueprint('temperature_api', __name__)

def get_current_timestamp():
    return datetime.now().strftime("%H:%M")

@temperature_api.route('/add', methods=['POST'])
def add_temperature():
    new_temp = request.json.get('temperature')
    new_reading = {"timestamp": get_current_timestamp(), "temperature": new_temp}
    
    with open('temperatures.json', 'r+') as f:
        data = json.load(f)
        data.append(new_reading)
        f.seek(0)
        json.dump(data, f)
    
    return jsonify(new_reading), 201

@temperature_api.route('/newest', methods=['GET'])
def get_newest_reading():
    with open('temperatures.json', 'r') as f:
        data = json.load(f)
    return jsonify(data[-1])

@temperature_api.route('/newest/<int:x>', methods=['GET'])
def get_newest_x_readings(x):
    with open('temperatures.json', 'r') as f:
        data = json.load(f)
    return jsonify(data[-x:])

@temperature_api.route('/delete_oldest/<int:y>', methods=['DELETE'])
def delete_oldest_y_readings(y):
    with open('temperatures.json', 'r') as f:
        data = json.load(f)
        del data[:y]

    with open('temperatures.json', 'w') as f:  # Open the file in write mode to truncate the file
        json.dump(data, f)
    
    return jsonify({"message": f"Deleted {y} oldest readings"}), 200

@temperature_api.route('/count', methods=['GET'])
def get_reading_count():
    with open('temperatures.json', 'r') as f:
        data = json.load(f)
    return jsonify({"count": len(data)})