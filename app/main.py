from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import *
from schemas import *
from database import *
from enums import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")

fake_db_points: list[ObservationPoint] = []
fake_db_messages: list[AirData] = []


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Render homepage
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html"
        )


@app.get("/map", response_class=HTMLResponse)
async def open_map(request: Request):
    """
    Open map interface
    """
    return templates.TemplateResponse(
        request=request,
        name="map.html"
        )


@app.get("/points/{device_id}")
def get_air_data(request: Request, device_id: int):
    """
    Given location ID, return corresponding observation point 
    Should include air quality related details
    """
    ...

    # TODO
    # :get from database, then substitute parameters to template with actual data

    latitude: float = 6.0
    longitude: float = 9.0
    location_name: str = "Melchor Hall, UP Diliman"
    status: AirStatus = AirStatus.good

    return templates.TemplateResponse(
        name="getAirData.html",
        context={
            "request": request,
            "device_id": device_id,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "status": status
            }
        )


@app.post("/add_point")
def add_point(point: ObservationPointAdd):
    """
    For adding new observation points
    """
    # TODO: replace with something more elegant; 
    #   (open SQLModel docs to see if meron doon)

    new_device_id = max((point.device_id for point in fake_db_points), default=-1) + 1

    appendable_point: ObservationPoint = ObservationPoint(
        device_id=new_device_id,
        location_name=point.location_name,
        latitude=point.latitude,
        longitude=point.longitude,
        )
    
    global fake_db_points
    fake_db_points.append(appendable_point)

    return point


@app.post("/delete_point")
def delete_point(device_id: int):
    """
    For deleting observation points
    """
    global fake_db_points
    # TODO: replace when SQLModel is working
    fake_db_points = [point for point in fake_db_points if (point.device_id != device_id)]

    return fake_db_points


@app.post("/send_data")
def send_air_data(data: AirDataSend):
    """
    For sensors; Send (a tick of) air data information to server
    """
    # TODO: replace with something more elegant; 
    #   (open SQLModel docs to see if meron doon)
    
    appendable_data: AirData = AirData(
        device_id=data.device_id,
        sequence=data.sequence,
        timestamp=data.timestamp,
        gas_value=data.gas_value,
        pm1_0=data.pm1_0,
        pm2_5=data.pm2_5,
        pm10_0=data.pm10_0,
        )

    global fake_db_messages
    fake_db_messages.append(appendable_data)

    return data