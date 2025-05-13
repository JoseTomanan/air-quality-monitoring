from sqlmodel import Session, select
from models import AirData
from enums import AirStatus


def compute_air_status(gas_conc: float, particle_conc: float) -> AirStatus:
    """
    Take x most recent entries and compute for air quality;
    Done every time a user makes a request
    """
    # TODO : find research for actual interpretation of concentration values

    some_fake_metric = gas_conc * particle_conc

    if some_fake_metric > 10:
        return AirStatus.hazardous
    if some_fake_metric > 7:
        return AirStatus.very_unhealthy
    if some_fake_metric > 5:
        return AirStatus.unhealthy
    return AirStatus.good


def compute_conc_values() -> tuple[float, float]:
    """
    Fetch last 10 values from AirData;
    Compute for mean of gas concentration, particle concentration
    """
    # TODO : define fetching logic; import database-related modules/libraries
    # (or alternatively, dyt it would be more elegant to move this to databases.py ???)
    ...