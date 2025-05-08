from enum import StrEnum


class AirStatus(StrEnum):
    good = "good"
    unhealthy = "UNHEALTHY"
    very_unhealthy = "VERY UNHEALTHY"
    hazardous = "HAZARDOUS"