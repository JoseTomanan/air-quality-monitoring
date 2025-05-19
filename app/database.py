from sqlmodel import SQLModel, create_engine, Session, select
from models import *
from statistics import mean


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


def update_air_data(data: AirData):
    """
    DB-facing function for receiving air data information
    """
    print(f"Inserting: device_id={data.device_id}, sequence={data.sequence}")
    with Session(engine) as session:
        existing = session.get(AirData, (data.device_id, data.sequence))
        if existing:
            print("Duplicate data detected, skipping insert.")
            return
        session.add(data)
        session.commit()
    print("New air data received.")


def compute_gas_conc(device_id: int) -> float:
    """
    Fetch last 10 values of gas_value from AirData;
    Compute for mean of gas concentration and return
    """
    ten_rows = ten_recent(device_id)
    gas_values = [row.gas_value for row in ten_rows]
    mean_gas_conc = mean(gas_values)

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

    mean_pm1_0 = mean(pm1_0_values)
    mean_pm2_5 = mean(pm2_5_values)
    mean_pm10_0 = mean(pm10_0_values)

    return (mean_pm1_0, mean_pm2_5, mean_pm10_0)


def ten_recent(device_id: int):
    """
    Helper function to fetch last 10 entries of a given device_id.
    """
    print("Accessing database.")

    with Session(engine) as session:
        query = select(AirData).where(AirData.device_id == device_id).order_by(AirData.timestamp.desc()).limit(10) # type: ignore
        ten_rows = session.exec(query).all()
        print(f"Ten most recent rows of device {device_id} extracted.")
        
    return ten_rows