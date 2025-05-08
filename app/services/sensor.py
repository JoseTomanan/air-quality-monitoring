from sqlmodel import Session, select
from models import AirData


def compute_air_status():
    """
    Take x most recent entries and compute for air quality;
    Done every time a user makes a request
    """
    ...