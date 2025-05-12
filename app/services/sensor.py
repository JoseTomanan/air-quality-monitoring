from sqlmodel import Session, select
from models import AirData
from enums import AirStatus


def compute_air_status(gas_conc: float, particle_conc: float) -> AirStatus:
    """
    Take x most recent entries and compute for air quality;
    Done every time a user makes a request
    """
    ...

    # TODO: DEFINE