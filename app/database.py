from sqlmodel import SQLModel, create_engine, Session, select
from models import *


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)

SQLModel.metadata.create_all(engine)
print("Database tables created successfully")

def add_new_point(point: ObservationPoint):
    with Session(engine) as session:
        session.add(point)
        session.commit()
    print("New point successfully added.")

def get_all_device_ids():
    with Session(engine) as session:
        query = select(ObservationPoint.device_id)
        all_device_ids = session.exec(query).all()
        return all_device_ids


def get_all_points_from_db():
    """
    Get all observation points
    """
    with Session(engine) as session:
        query = select(ObservationPoint)
        all_points = session.exec(query).all()
        return all_points