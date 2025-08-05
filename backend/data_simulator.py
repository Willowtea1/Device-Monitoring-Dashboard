# backend/data_simulator.py #
import pandas as pd
import time
import random
from models import Device
from datetime import datetime


# Load the Excel file (update path if needed)
df = pd.read_excel("iot_sensors.xlsx")

# Optional: Add image URL based on Machine_Type
import os

import os

# Manual map of Machine_Type → filename
image_map = {
    "3D_Printer": "3dprinter.png",
    "AGV": "agv.png",
    "Conveyor_Belt": "belt.png",
    "Boiler": "boiler.png",
    "Press_Brake": "brake.png",
    "Industrial_Chiller": "chiller.png",
    "CMM": "cmm.png",
    "CNC_Mill": "mill.png",
    "CNC_Lathe": "lathe.png",
    "Compressor": "compressor.png",
    "Crane": "crane.png",
    "Dryer": "dryer.png",
    "Furnace": "furnace.png",
    "Forklift_Electric": "evforklift.png",
    "Carton_Former": "former.png",
    "Grinder": "grinder.png",
    "Heat_Exchanger": "heat.png",
    "Hydraulic_Press": "hydraulic.png",
    "Labeler": "labeler.png",
    "Laser_Cutter": "laser_cutter.png",
    "Mixer": "mixer.png",
    "Injection_Molder": "moulder.png",
    "Vacuum_Packer": "packer.png",
    "Palletizer": "palletizer.png",
    "Pick_and_Place": "pick.png",
    "Pump": "pump.png",
    "Robot_Arm": "robot_arm.png",
    "Automated_Screwdriver": "screwdriver.png",
    "Shuttle_System": "shuttle.png",
    "Valve_Controller": "valve.png",
    "Vision_System": "vision.png",
    "Shrink_Wrapper": "wrapper.png",
    "XRay_Inspector": "xray.png",
}



def get_image_url(machine_type):
    filename = image_map.get(machine_type)
    if not filename:
        print(f"[WARN] No mapping for: {machine_type}")
        return "http://localhost:8000/static/placeholder.png"

    path = os.path.join("static", filename)
    if os.path.exists(path):
        return f"http://localhost:8000/static/{filename}"
    else:
        print(f"[WARN] File not found: {path}")
        return "http://localhost:8000/static/placeholder.png"


df["image_url"] = df["Machine_Type"].apply(get_image_url)

# Store latest history by Machine_ID
history_data = {}

def generate_device_data(simulate=False):
    result = []

    for _, row in df.iterrows():
        machine_id = row["Machine_ID"]
        ts = time.strftime("%H:%M:%S")

        # Base values from Excel
        temp = row["Temperature_C"]
        power = row["Power_Consumption_kW"]
        vibration = row["Vibration_mms"]
        sound = row["Sound_dB"] 

        # If simulate = True, apply random fluctuation
        if simulate:
            temp += round(random.uniform(-1.5, 1.5), 2)
            power += round(random.uniform(-0.5, 0.5), 2)
            vibration += round(random.uniform(-0.3, 0.3), 2)
            sound += round(random.uniform(-2.0, 2.0), 2)

        # History tracking
        history_data.setdefault(machine_id, []).append({
            "timestamp": ts,
            "temperature": temp
        })
        if len(history_data[machine_id]) > 10:
            history_data[machine_id] = history_data[machine_id][-10:]

        device_data = {
            "id": machine_id,
            "type": row["Machine_Type"].replace("_", " "),
            "installation_year": row["Installation_Year"],
            "operational_hours": row["Operational_Hours"],
            "temperature": round(temp, 2),
            "vibration": round(vibration, 2),
            "sound": round(sound, 2), 
            "oil_level": round(row["Oil_Level_pct"], 2),
            "coolant_level": round(row["Coolant_Level_pct"], 2),
            "power": round(power, 2),
            "last_maintenance_days": int(row["Last_Maintenance_Days_Ago"]),
            "maintenance_count": int(row["Maintenance_History_Count"]),
            "failure_count": int(row["Failure_History_Count"]),
            "ai_supervision": row["AI_Supervision"],
            "error_codes_last_30": row["Error_Codes_Last_30_Days"],
            "remaining_rul_days": int(row["Remaining_Useful_Life_days"]),
            "will_fail_7_days": bool(row["Failure_Within_7_Days"]),
            "status": row["Status"].strip().capitalize(),
            "image_url": row["image_url"],
            "initial_timestamp": datetime.utcnow()
        }


        result.append(Device(**device_data)) 

    return result


def get_device_history(device_id):
    return history_data.get(device_id, [])
