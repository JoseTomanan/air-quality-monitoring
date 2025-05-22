from typing import Sequence
from sqlmodel import SQLModel, create_engine, Session, select
from models import *
from statistics import mean

from datetime import timedelta, datetime

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables():
    """
    Docs: https://fastapi.tiangolo.com/az/advanced/events/#lifespan-function
    """
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully")


def add_new_point(point: ObservationPoint):
    """
    DB-facing function on pushing new point
    """
    with Session(engine) as session:
        session.add(point)
        session.commit()
    print("New point successfully added.")


def get_all_device_ids():
    """
    DB-facing function on getting all device_id from observation points
    """
    with Session(engine) as session:
        query = select(ObservationPoint.device_id)
        all_device_ids = session.exec(query).all()
        return all_device_ids


def get_point_info(device_id: int):
    """
    DB-facing function on retrieving all point information, given device ID
    """
    with Session(engine) as session:
        query = select(ObservationPoint).where(ObservationPoint.device_id == device_id)
        existing = session.exec(query).first()
        return existing if existing else None


def delete_point_in_db(device_id: int):
    """
    DB-facing function on deleting observation points inside DB
    """
    with Session(engine) as session:
        query = select(ObservationPoint).where(ObservationPoint.device_id == device_id)
        deletable_point = session.exec(query).first()
        
        if deletable_point:
            session.delete(deletable_point)
            session.commit()
            print(f"Device {device_id} successfully deleted.")
            return True
        
        else:
            print(f"Device {device_id} not found.")
            return False


def update_air_data(data: AirData) -> bool:
    """
    DB-facing function for receiving air data information
    """
    print(f"Inserting: device_id={data.device_id}, sequence={data.sequence} at time {data.timestamp}")

    with Session(engine) as session:
        existing = session.get(AirData, (data.device_id, data.sequence, data.timestamp))
        if existing:
            print("Duplicate data detected, skipping insert.")
            return False
        session.add(data)
        session.commit()
    print("New air data received.")
    return True


def compute_gas_conc(device_id: int) -> float:
    """
    Fetch last 10 values of gas_value from AirData;
    Compute for mean of gas concentration and return
    """
    ten_rows = ten_recent(device_id)

    gas_values = [row.gas_value for row in ten_rows]
    mean_gas_conc = mean(gas_values) if gas_values else 0.0

    return mean_gas_conc


def compute_particle_conc(device_id: int) -> tuple[float, float, float]:
    """
    Fetch last 10 values of PM1.0, PM2.5, and PM10.0 from AirData;
    Compute for mean of each one then return as a tuple.
    The tuple that will be returned contain, in order: (PM1.0, PM2.5, PM10.0).
    """
    ten_rows = ten_recent(device_id)

    pm1_0_values = [row.pm1_0 for row in ten_rows]
    pm2_5_values = [row.pm2_5 for row in ten_rows]
    pm10_0_values = [row.pm10_0 for row in ten_rows]

    mean_pm1_0 = mean(pm1_0_values) if pm1_0_values else 0.0
    mean_pm2_5 = mean(pm2_5_values) if pm2_5_values else 0.0
    mean_pm10_0 = mean(pm10_0_values) if pm10_0_values else 0.0

    return (mean_pm1_0, mean_pm2_5, mean_pm10_0)


def ten_recent(device_id: int):
    """
    Helper function to fetch last 10 entries of a given device_id.
    """
    print("Accessing database.")

    with Session(engine) as session:
        query = select(AirData).where(AirData.device_id == device_id) \
            .order_by(AirData.timestamp.desc()).limit(10)  # type: ignore
        ten_rows = session.exec(query).all()

        print("--> ten rows:", [
                (str(row.timestamp), row.gas_value, row.pm1_0, row.pm2_5, row.pm10_0)
                for row in ten_rows
            ]
            )
        
    return ten_rows


def get_most_recent_air_data(device_id: int) -> AirData:
    """
    Return the most recent instance of air data for a given device_id
    """
    with Session(engine) as session:
        query = select(AirData).where(AirData.device_id == device_id) \
            .order_by(AirData.timestamp.desc())  # type: ignore
        most_recent = session.exec(query).first()

        if most_recent is None:
            return AirData(
                device_id=device_id,
                sequence=0,
                timestamp=datetime.now(),
                gas_value=0,
                pm1_0=0,
                pm2_5=0,
                pm10_0=0,
            )
        
        print("--> MOST RECENT:", str(most_recent.timestamp), most_recent)

        return most_recent


def get_ten_latest_values(device_id: int) -> tuple[list, list, list, list, list]:
    ten_rows = ten_recent(device_id)

    isotime_all_recent = [row.timestamp.isoformat() for row in ten_rows]
    gas_value_10_recent = [row.gas_value for row in ten_rows]
    pm1_0_10_recent = [row.pm1_0 for row in ten_rows]
    pm2_5_10_recent = [row.pm2_5 for row in ten_rows]
    pm10_0_10_recent = [row.pm10_0 for row in ten_rows]

    return (isotime_all_recent, gas_value_10_recent, pm1_0_10_recent, pm2_5_10_recent, pm10_0_10_recent)


def get_all_values_from_data(device_id: int) -> tuple[list, list, list, list, list]:
    """
    Get all values from db.
    """

    with Session(engine) as session:
        query = select(AirData).where(AirData.device_id == device_id).order_by(AirData.timestamp)
        all_rows: Sequence[AirData] = session.exec(query).all()

    # Convert to UTC+8 and format
    isotime_all = [
        (row.timestamp + timedelta(hours=8)).strftime("%m/%d, %H:%M")
        for row in all_rows
    ]

    gas_value_all = [row.gas_value for row in all_rows]
    pm1_0_all = [row.pm1_0 for row in all_rows]
    pm2_5_all = [row.pm2_5 for row in all_rows]
    pm10_0_all = [row.pm10_0 for row in all_rows]

    return (isotime_all, gas_value_all, pm1_0_all, pm2_5_all, pm10_0_all)
    
    
def generate_intervals_between(start: datetime, end: datetime, interval_minutes: int = 5):
    if start > end:
        raise ValueError("Start time must be before end time")
    
    interval = timedelta(minutes=interval_minutes)

    # Round start DOWN to nearest interval
    rounded_start = start - timedelta(
        minutes=start.minute % interval_minutes,
        seconds=start.second,
        microseconds=start.microsecond
    )

    # Round end UP to nearest interval
    minute_remainder = end.minute % interval_minutes
    if minute_remainder == 0 and end.second == 0 and end.microsecond == 0:
        rounded_end = end
    else:
        rounded_end = end + timedelta(
            minutes=interval_minutes - minute_remainder,
            seconds=-end.second,
            microseconds=-end.microsecond
        )

    # Generate intervals
    current = rounded_start
    result = []
    while current <= rounded_end:
        result.append(current)
        current += interval

    return result