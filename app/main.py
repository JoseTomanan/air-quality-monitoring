from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from pydantic import BaseModel

from models import *
from schemas import *
from database import *
from enums import *
from services.admin import *
from services.sensor import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Docs: https://fastapi.tiangolo.com/az/advanced/events/#lifespan-function
    """
    create_db_and_tables()
    yield

# Define the Pydantic model for the request
class DeviceIdRequest(BaseModel):
    device_id: int

app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")


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
    point = get_point_info(device_id)

    if point is None:
        return templates.TemplateResponse(request=request, name="404.html", status_code=404)

    conc_values: tuple[float, float] = compute_conc_values()
    status: AirStatus = compute_air_status(*conc_values)

    return templates.TemplateResponse(
        name="getAirData.html",
        context={
            "request": request,
            "device_id": device_id,
            "location_name": point.location_name,
            "latitude": point.latitude,
            "longitude": point.longitude,
            "status": status,
            "gas_conc": conc_values[0],
            "particle_conc": conc_values[1],
            }
        )


@app.get("/points")
def get_all_points():
    """
    Get all observation points
    """
    all_device_id = get_all_device_ids()
    return [get_point_info(device_id) for device_id in all_device_id]


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

    # Return the new point with device_id included
    return {
        "device_id": new_device_id,
        "location_name": location_name,
        "latitude": latitude,
        "longitude": longitude
    }


@app.post("/delete_point")
async def delete_point(request: DeviceIdRequest):
    """
    Deletes a point by device_id.
    """
    device_id = request.device_id
    success = delete_point_in_db(device_id)

    if success:
        return {"message": "Point successfully deleted."}
    else:
        raise HTTPException(status_code=404, detail="Point not found.")


@app.post("/send_data")
def send_air_data(data: AirDataSend) -> AirData:
    """
    For sensors; Send (a tick of) air data information to server
    """
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

    update_air_data(appendable_data)

    return appendable_data