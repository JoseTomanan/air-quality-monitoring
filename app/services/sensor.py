from sqlmodel import Session, select
from models import AirData
from enums import AirStatus


def compute_air_status(gas_conc: float, pm1_0: float, pm2_5: float, pm10_0: float) -> AirStatus:
    """
    Take 10 most recent entries and compute for air quality;
    Done every time a user makes a request
    """
    # TODO : find research for actual interpretation of concentration values

    some_fake_metric = gas_conc + (pm1_0 * pm2_5 * pm10_0)

    if some_fake_metric > 10:
        return AirStatus.hazardous
    if some_fake_metric > 7:
        return AirStatus.very_unhealthy
    if some_fake_metric > 5:
        return AirStatus.unhealthy
    if some_fake_metric > 3:
        return AirStatus.moderate
    
    return AirStatus.good


def compute_gas_conc() -> float:
    """
    Fetch last 10 values of gas_value from AirData;
    Compute for mean of gas concentration and return
    """
    # TODO : define fetching logic; import database-related modules/libraries
    # (or alternatively, dyt it would be more elegant to move this to databases.py ???)
    ...
    return 0.6


def compute_particle_conc() -> tuple[float, float, float]:
    """
    Fetch last 10 values of PM1.0, PM2.5, and PM10.0 from AirData;
    Compute for mean of each one then return as a tuple.
    The tuple that will be returned contain, in order: (PM1.0, PM2.5, PM10.0).
    """
    # TODO : define fetching logic; import database-related modules/libraries
    # (or alternatively, dyt it would be more elegant to move this to databases.py ???)
    ...
    return (0.1, 0.2, 0.3)