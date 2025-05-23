from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import PrimaryKeyConstraint
from typing import Optional
from enums import *


class ObservationPoint(SQLModel, table=True):
    """
    Table for sensor/microcontroller instances
    """
    device_id: int = Field(primary_key=True)
    location_name: str = Field(index=True, nullable=True)
    latitude: float = Field()
    longitude: float = Field()

class AirData(SQLModel, table=True):
    """
    Table for stored air data ticks
    """
    device_id: int = Field()
    sequence: int = Field()
    timestamp: datetime = Field()
    gas_value: int = Field()
    pm1_0: int = Field()
    pm2_5: int = Field()
    pm10_0: int = Field()

    __table_args__ = (
        PrimaryKeyConstraint("device_id", "sequence", "timestamp"),
    )