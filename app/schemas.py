from datetime import datetime
from sqlmodel import SQLModel

from enums import *


class ObservationPointAdd(SQLModel):
    """
    Request format for add_point
    """
    location_name: str
    latitude: float
    longitude: float

class ObservationPointDelete(SQLModel):
    """
    Request format for delete_point()
    """
    device_id: int

class AirDataSend(SQLModel):
    """
    Request format for send_air_data()
    """
    device_id: int
    sequence: int
    timestamp: datetime
    gas_value: int
    pm1_0: int
    pm2_5: int
    pm10_0: int
