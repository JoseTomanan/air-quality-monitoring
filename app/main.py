from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from models import *
from schemas import *
from database import *
from enums import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Docs: https://fastapi.tiangolo.com/az/advanced/events/#lifespan-function
    """
    create_db_and_tables()
    yield


app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")

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

    gas_conc: float = 66.99
    particle_conc: float = 69.69

    return templates.TemplateResponse(
        name="getAirData.html",
        context={
            "request": request,
            "device_id": device_id,
            "location_name": location_name,
            "latitude": latitude,
            "longitude": longitude,
            "status": status,
            "gas_conc": gas_conc,
            "particle_conc": particle_conc,
            }
        )


@app.post("/add_point")
def add_point(location_name: str=Form(...), latitude: float=Form(...), longitude: float=Form(...)):
    """
    For adding new observation points
    """
    new_device_id = max((*get_all_device_ids(), 0)) + 1

    appendable_point: ObservationPoint = ObservationPoint(
        device_id=new_device_id,
        location_name=location_name,
        latitude=latitude,
        longitude=longitude,
        )
    
    print(f"NEW POINT:{appendable_point}")
    add_new_point(appendable_point)

    return appendable_point


@app.post("/delete_point")
def delete_point(device_id: int):
    """
    For deleting observation points
    """
    result = delete_point_in_db(device_id)

    return result


@app.post("/send_data")
def send_air_data(data: AirDataSend) -> AirData:
    """
    For sensors; Send (a tick of) air data information to server
    """
    # TODO: replace with something more elegant; 
    #   (open SQLModel docs to see if meron doon)

    new_timestamp: datetime = datetime.now()

    appendable_data: AirData = AirData(
        device_id=data.device_id,
        sequence=data.sequence,
        timestamp=new_timestamp,
        gas_value=data.gas_value,
        pm1_0=data.pm1_0,
        pm2_5=data.pm2_5,
        pm10_0=data.pm10_0,
        )

    global fake_db_messages
    fake_db_messages.append(appendable_data)

    return appendable_data