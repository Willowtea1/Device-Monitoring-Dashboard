from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import Device, DeviceDetail
from data_simulator import generate_device_data, get_device_history

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/devices", response_model=list[Device])
def get_devices():
    return generate_device_data()

@app.get("/api/devices/{device_id}", response_model=DeviceDetail)
def get_device_detail(device_id: str):
    devices = generate_device_data()
    device = next((d for d in devices if d.id == device_id), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    device_detail = device.dict()
    device_detail["history"] = get_device_history(device_id)
    return device_detail
