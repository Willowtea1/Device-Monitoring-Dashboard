# models.py #
from pydantic import BaseModel
from typing import List

class Device(BaseModel):
    id: str
    name: str
    status: str
    cpu: float
    temperature: float
    image_url: str

class DeviceDetail(Device):
    history: List[dict]