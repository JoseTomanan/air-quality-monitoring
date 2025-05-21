from sqlmodel import Session, select
from models import ObservationPoint
from datetime import datetime, timezone, timedelta


def to_ph_time(dt: datetime):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone(timedelta(hours=8)))