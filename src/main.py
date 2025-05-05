from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from project_types import ObservationPoint


app = FastAPI()

templates = Jinja2Templates(directory="../templates")

observation_points: list[ObservationPoint] = []

"""
Result when accessing root of site
"""
@app.get("/") 
def root():
    return templates.TemplateResponse("root.html")


"""
For adding new observation points
"""
@app.post("/add_point")
def add_point(point: ObservationPoint):
    observation_points.append(point)
    return point


"""
For deleting observation points
"""
@app.post("/delete_point")
def delete_point(point: ObservationPoint):
    observation_points.remove(point)
    return observation_points


"""
Given location ID, return corresponding observation point 
Should include air quality related details
"""
@app.post("/points/{device_id}")
def get_point(device_id: int):
    ...

    returnable = templates.TemplateResponse(
        "index.html",
        {"device_id": device_id, }
        )

    return returnable