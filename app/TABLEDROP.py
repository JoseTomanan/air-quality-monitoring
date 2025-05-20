from sqlmodel import SQLModel, Session, create_engine
from models import AirData  # adjust this import

engine = create_engine("sqlite:///database.db", echo=True)

# DROP the table manually
SQLModel.metadata.drop_all(bind=engine)

# Recreate with the new schema
SQLModel.metadata.create_all(bind=engine)
