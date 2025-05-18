from sqlmodel import SQLModel, create_engine, Session, select
from models import *


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