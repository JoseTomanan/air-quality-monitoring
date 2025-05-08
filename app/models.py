from datetime import datetime
from sqlmodel import SQLModel, Field
from typing import Optional


class ObservationPoint(SQLModel, table=True):
    """
    Construct for image being passed
    """
    device_id: Optional[int] = Field(primary_key=True)
    name: str = Field(index=True, nullable=True)
    latitude: float = Field()
    longitude: float = Field()

class Message(SQLModel, table=True):
    """
    Data type of message passed by microcontroller
    """
    device_id: Optional[int] = Field(primary_key=True)
    sequence: int = Field()
    timestamp: datetime = Field()
    gas_value: int = Field()
    pm1_0: int = Field()
    pm2_5: int = Field()
    pm10_0: int = Field()