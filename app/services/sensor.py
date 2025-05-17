from sqlmodel import Session, select
from models import AirData
from enums import AirStatus


def compute_air_status(gas_conc: float, pm1_0: float, pm2_5: float, pm10_0: float) -> dict[str, AirStatus]:
    """
    Take 10 most recent entries and compute for air quality;
    Done every time a user makes a request
    """
    statuses: dict[str, AirStatus] = {}

    GAS_CONC_STATUS = [
        (50.0, AirStatus.good),
        (100.0, AirStatus.moderate),
        (200.0, AirStatus.unhealthy),
        (300.0, AirStatus.very_unhealthy),
        (float('inf'), AirStatus.hazardous),
        ]

    PM1_0_2_5_STATUS = [
        (12.0, AirStatus.good),
        (35.4, AirStatus.moderate),
        (150.4, AirStatus.unhealthy),
        (250.4, AirStatus.very_unhealthy),
        (float('inf'), AirStatus.hazardous),
        ]
    
    PM10_0_STATUS = [
        (54.0, AirStatus.good),
        (150.4, AirStatus.moderate),
        (650.4, AirStatus.unhealthy),
        (1050.4, AirStatus.very_unhealthy),
        (float('inf'), AirStatus.hazardous),
        ]

    for threshold, status in GAS_CONC_STATUS:
        if gas_conc <= threshold:
            statuses["gas_conc"] = status
            break

    for threshold, status in PM1_0_2_5_STATUS:
        if pm1_0 <= threshold:
            statuses["pm1_0"] = status
            break

    for threshold, status in PM1_0_2_5_STATUS:
        if pm2_5 <= threshold:
            statuses["pm2_5"] = status
            break

    for threshold, status in PM10_0_STATUS:
        if pm10_0 <= threshold:
            statuses["pm10_0"] = status
            break

    return statuses


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