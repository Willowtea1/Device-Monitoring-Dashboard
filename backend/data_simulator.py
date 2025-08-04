# data_simulator.py

import random
import time

devices = [
    {"id": "device-1", "name": "Device A"},
    {"id": "device-2", "name": "Device B"},
    {"id": "device-3", "name": "Device C"},
]

history_data = {}

image_map = {
    "Device A": "device_a.png",
    "Device B": "device_b.png",
    "Device C": "device_c.png",
}

def generate_device_data():
    result = []

    for device in devices:
        cpu = round(random.uniform(5, 90), 2)
        temp = round(random.uniform(40, 90), 2)
        status = random.choice(["online", "offline"])

        # Lookup image
        image_filename = image_map.get(device["name"], "default.jpg")
        image_url = f"http://localhost:8000/static/{image_filename}"

        device_data = {
            "id": device["id"],
            "name": device["name"],
            "status": status,
            "cpu": cpu,
            "temperature": temp,
            "image_url": image_url,
        }

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
