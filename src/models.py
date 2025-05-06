from datetime import datetime
from sqlmodel import SQLModel


class ObservationPoint(SQLModel):
    """
    Construct for image being passed
    """
    device_id: int
    name: str
    latitude: float
    longitude: float

class Message(SQLModel):
    """
    Data type of message passed by microcontroller
    """
    device_id: int
    sequence: int
    timestamp: datetime
    gas_value: int
    pm1_0: int
    pm2_5: int
    pm10_0: int