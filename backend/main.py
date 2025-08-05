# backend/main.py #
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from typing import List
from models import Device, DeviceDetail
from data_simulator import generate_device_data, get_device_history
from analytic_simulator import simulate_data  

import pandas as pd
import os
    
app = FastAPI() 

# Serve static images
app.mount("/static", StaticFiles(directory="static", html=False), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/devices", response_model=List[Device])
def get_devices(simulate: bool = False):
    return generate_device_data(simulate=simulate)

@app.get("/api/devices/{device_id}", response_model=DeviceDetail)
def get_device_detail(device_id: str):
    devices = generate_device_data()
    device = next((d for d in devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device_detail = device.dict()
    device_detail["history"] = get_device_history(device_id)
    return device_detail

@app.get("/api/summary")
def get_summary():
    devices = generate_device_data()
    online = sum(1 for d in devices if d.status.lower() == "online")
    offline = sum(1 for d in devices if d.status.lower() != "online")
    avg_temp = round(sum(d.temperature for d in devices) / len(devices), 2)
    featured_device = devices[0]
    return {
        "online": online,
        "offline": offline,
        "avg_temp": avg_temp,
        "featured_device": featured_device.dict(),  # Convert model to dict for JSON response
    }

# Analytics Page #

@app.get("/api/devices/{device_id}/chart")
def get_device_chart_data(device_id: str):
    try:
        # Always regenerate the Excel file
        simulate_data()

        # Load newly generated data
        df = pd.read_excel("simulated_iot_data.xlsx")

        # Filter data for the specific device_id
        device_data = df[df["device_id"] == device_id]

        if device_data.empty:
            raise HTTPException(status_code=404, detail=f"No simulated data found for device '{device_id}'")

        return device_data.to_dict(orient="records")

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Simulated data file not found")
