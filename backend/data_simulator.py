import random
import time

devices = [
    {"id": "device-1", "name": "Sensor A"}, 
    {"id": "device-2", "name": "Sensor B"}, 
    {"id": "device-3", "name": "Sensor C"}, 
]

history_data = {}

def generate_device_data():
    result = []
    for device in devices:
        cpu = round(random.uniform(5, 90), 2)
        temp = round(random.uniform(40, 90), 2)
        status = random.choice(["online", "offline"])
        device_data = {
            "id": device["id"],
            "name": device["name"],
            "status": status,
            "cpu": cpu,
            "temperature": temp,
        }

        # Save history for detail view
        ts = time.strftime("%H:%M:%S")
        history_data.setdefault(device["id"], []).append({
            "timestamp": ts,
            "cpu": cpu,
            "temperature": temp
        })
        if len(history_data[device["id"]]) > 10:
            history_data[device["id"]] = history_data[device["id"]][-10:]

        result.append(device_data)
    return result

def get_device_history(device_id):
    return history_data.get(device_id, [])