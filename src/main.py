from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from project_types import ObservationPoint


app = FastAPI()

templates = Jinja2Templates(directory="../templates")

observation_points: list[ObservationPoint] = []


@app.get("/") 
def root():
    """
    Result when accessing root of site
    """
    return templates.TemplateResponse("root.html")


@app.post("/add_point")
def add_point(point: ObservationPoint):
    """
    For adding new observation points
    """
    observation_points.append(point)
    return point


@app.post("/delete_point")
def delete_point(point: ObservationPoint):
    """
    For deleting observation points
    """
    observation_points.remove(point)
    return observation_points


@app.post("/points/{device_id}")
def get_point(device_id: int):
    """
    Given location ID, return corresponding observation point 
    Should include air quality related details
    """
    ...

    returnable = templates.TemplateResponse(
        "index.html",
        {"device_id": device_id, }
        )

    return returnable