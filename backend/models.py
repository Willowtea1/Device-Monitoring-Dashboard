# backend/models.py #
from pydantic import BaseModel
from typing import List, Union

class Device(BaseModel):
    id: str
    type: str
    installation_year: int
    operational_hours: int
    temperature: float
    vibration: float
    sound: float
    oil_level: float
    coolant_level: float
    power: float
    last_maintenance_days: int
    maintenance_count: int
    failure_count: int
    ai_supervision: Union[bool, str] 
    error_codes_last_30: int
    remaining_rul_days: int
    will_fail_7_days: Union[bool, str]
    status: str
    image_url: str

class HistoryItem(BaseModel):
    timestamp: str
    temperature: float

class DeviceDetail(Device):
    history: List[HistoryItem]
