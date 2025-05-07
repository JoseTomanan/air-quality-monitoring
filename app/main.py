from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models import *
from database import *


app = FastAPI()
app.mount("/static", StaticFiles(directory="../static"), name="static")

templates = Jinja2Templates(directory="../templates")

fake_db_points: list[ObservationPoint] = []
fake_db_messages: list[Message] = []


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Render homepage
    """
    return templates.TemplateResponse(
        request=request,
        name="index.html"
        )


@app.post("/add_point")
def add_point(point: ObservationPoint):
    """
    For adding new observation points
    """
    ...


@app.post("/delete_point")
def delete_point(point_id: int):
    """
    For deleting observation points
    """
    ...


@app.get("/points/{device_id}")
def get_point(device_id: int):
    """
    Given location ID, return corresponding observation point 
    Should include air quality related details
    """
    ...

    return templates.TemplateResponse(
        name="index.html",
        context={"device_id": device_id, }
        )

@app.post("send_data")
def send_data(message: Message):
    """
    For sensors; Send tick of data to server
    """
    ...

    return True