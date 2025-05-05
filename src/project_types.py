from dataclasses import dataclass
from typing import Protocol
from enum import Enum, StrEnum, auto
from pydantic import BaseModel


class ObservationPoint(BaseModel):
    """
    Construct for image being passed
    """
    device_id: int
    name: str
    latitude: float
    longitude: float

class Message(BaseModel):
    """
    Data type of message passed by microcontroller
    """
    device_id: int
    sequence: int
    gas_value: int
    pm1_0: int
    pm2_5: int
    pm10_0: int