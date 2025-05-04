from fastapi import FastAPI, HTTPException
from project_types import ObservationPoint, Location


app = FastAPI()

observation_points: list[ObservationPoint] = []

@app.get("/") 
def root():
    return {"air": "bad"}


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
@app.post("/points/{loc_id}")
def get_point(id: int):
    if ...:
        ...
        
    else:
        raise HTTPException(status_code=404, detail="Observation point does not exist")

