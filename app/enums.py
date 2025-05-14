from enum import StrEnum


class AirStatus(StrEnum):
    good = "GOOD"
    moderate = "MODERATE"
    unhealthy = "UNHEALTHY"
    very_unhealthy = "VERY UNHEALTHY"
    hazardous = "HAZARDOUS"