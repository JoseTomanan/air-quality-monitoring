from sqlmodel import SQLModel, create_engine, Session, select
from models import *


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)
print("Database tables created successfully")

def add_new_point(new_device_id, new_location_name, new_latitude, new_longitude):
    with Session(engine) as session:
        add_this = ObservationPoint(device_id = new_device_id,
                                    location_name = new_location_name,
                                    latitude = new_latitude,
                                    longitude = new_longitude)
        session.add(add_this)
        session.commit()
    print("New point successfully added.")

def get_all_device_ids():
    with Session(engine) as session:
        query = select(ObservationPoint.device_id)
        all_device_ids = session.exec(query).all()
        return all_device_ids