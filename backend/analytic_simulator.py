# backend/analytic_simulator.py

from data_simulator import generate_device_data
from collections import defaultdict
from typing import Dict, List
from models import Device
import pandas as pd


# Storage for analytics
average_temperature: Dict[str, float] = {}
alerts: Dict[str, List[str]] = defaultdict(list)

def simulate_data():
    from datetime import datetime, timedelta

    records = []
    now = datetime.utcnow()
    for _ in range(10):  # 10 time steps
        devices = generate_device_data(simulate=True)
        for device in devices:
            records.append({
                "device_id": device.id,
                "timestamp": now,
                "temperature": device.temperature,
                "vibration": device.vibration,
                "sound": device.sound,
                "power": device.power,
                "status": device.status
            })
        now += timedelta(minutes=1)  # simulate data every 1 minute

    df = pd.DataFrame(records)
    df.to_excel("simulated_iot_data.xlsx", index=False)
